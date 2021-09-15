from flask import Flask, request, render_template, flash,  redirect, url_for, send_from_directory, send_file, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from Passenger import views as passengerUrl
from HotelStaf import views as hotelStafUrl
from Admin import views as adminUrl
from oracleCon import get_db, close_db

app = Flask('app')
app.debug = True
app.secret_key = "mysecretkey"


# Admin Urls 
app.add_url_rule('/admin/Home', view_func = adminUrl.AdminHome)
app.add_url_rule('/admin/Home', view_func = adminUrl.AdminContact)



# Hotel Staff Urls
app.add_url_rule('/hotelstaf/Home', view_func = hotelStafUrl.HotelStafHome)


#Passenger Urls
app.add_url_rule('/Home', view_func = passengerUrl.PassengerHome)
app.add_url_rule('/Home/details', view_func= passengerUrl.LocationDetails)


def check_user(page):
    if session.get("email"):
        return page
    else:
        return 'login.html'
        
@app.route('/', methods=['GET', 'POST'])
def Home():  
   return render_template('base.html')
   

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try :
            conn = get_db()
            cursor = conn.cursor()
            email = str(request.form['email'])
            password = str(request.form["password"])
            mydoc = cursor.execute("SELECT * from USERDETAILS WHERE U_EMAIL = :email AND U_PASSWORD = :password", email=email, password= password)
            myresult = mydoc.fetchone()
            cursor.close()
            if myresult:
                session['email'] = str(myresult[1])
                session['user_role'] = str(myresult[12])
                session['fname'] = str(myresult[4])
                if myresult[12].strip() == "P":
                    # code for passenger
                    return redirect('/Home')
                elif myresult[12].strip() == "A":
                    # code for admin
                    return redirect('/admin/Home')
                else:
                    return redirect('/Home')
            else:
                return render_template('login.html', msg='email id or password is not matching')

        except Exception as e:
            return render_template('login.html', msg=e)
    else:
        return render_template('login.html')


@app.route("/sign", methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        try:
            conn = get_db()
            cursor = conn.cursor()
            fname = str(request.form["fname"])
            mname = str(request.form['mname'])
            lname = str(request.form["lname"])
            password = str(request.form["password"])
            email = str(request.form['email'])
            phone = str(request.form['phoneNo'])
            state = str(request.form['state'])
            district = str(request.form['district'])
            addrline1 = str(request.form['addrline1'])
            city = str(request.form['city'])
            pincode = request.form['pincode']
            cursor.execute("SELECT * from USERDETAILS WHERE U_EMAIL = :email", email = str(email))
            if cursor.fetchall():
                return render_template("sign.html", msg="Email Already Exist Try Different")
            else:
               userdata = dict(U_EMAIL = email, U_PASSWORD = password, U_PHONE = phone, U_F_NAME = fname, U_M_NAME = mname, U_L_NAME = lname, STATE = state, DISTRICT = district, CITY = city, PINCODE = pincode, LINE1 = addrline1, U_ROLE = 'P')
               cursor.execute('insert into USERDETAILS (U_EMAIL,U_PASSWORD,U_PHONE,U_F_NAME,U_M_NAME,U_L_NAME,STATE,DISTRICT,CITY,PINCODE,LINE1,U_ROLE) values (:U_EMAIL, :U_PASSWORD, :U_PHONE, :U_F_NAME, :U_M_NAME, :U_L_NAME, :STATE, :DISTRICT, :CITY, :PINCODE, :LINE1, :U_ROLE)', userdata)

               mydoc = cursor.execute("SELECT * from USERDETAILS WHERE U_EMAIL = :email" , email = str(email))
               myresult = mydoc.fetchone()
               conn.commit()

                # print('Singin User :', myresult)
                # session['username'] = str(fname)+" "+str(lname)
                # session['email'] = str(email)
                # session['user_id'] = myresult[0]
                # session['user_role'] = str(myresult[4])
            cursor.close()
            # conn.close()
            return render_template('login.html', msg = 'Successfully Registered')

        except Exception as e:
            return render_template('sign.html', msg=e)
    else:
        return render_template('sign.html')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":   
    app.run(host='0.0.0.0', port=3000, debug=True ) # localhost
    # app.run(host='192.168.0.106', port=8080 )  #Router