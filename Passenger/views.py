from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, session
import os
from oracleCon import get_db, close_db

def checkDuplicate(locationResult, row):
    point = -1
    for elem in range(len(locationResult)): 
        if locationResult[elem][0] == row[0]:
            point = elem
    return point   

def PassengerHome():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT lo.l_id,lo.l_lname, lo.state, lo.CITY, li.img FROM LOCATION lo INNER JOIN loc_images li ON lo.L_ID = li.l_id")
    resultData = cursor.fetchall()
    locationResult = []
    for row in resultData:
        if len(locationResult) > 0:
            point = checkDuplicate(locationResult, row)
            if point < 0:
                locationResult.append(list(row))
            else:
                locationResult[point][4] = [locationResult[point][4], row[4]]
        else:
            locationResult.append(list(row))
        
    print(locationResult)
    cursor.close()
    return render_template('/PassengerSite/PassengerHome.html', fname=session['fname'], location= locationResult)

def PassengerSignUp():
    connection = get_db()
    if request.method == 'POST':
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        state = request.form['state']
        district = request.form['district']
        pincode = request.form['pincode']
        addrline1 = request.form['addrline1']
        city = request.form['city']
        phone_no = request.form['phoneno']
        cursor = connection.cursor()
        userdata = dict(U_EMAIL = email, U_PASSWORD = password, U_PHONE = phone_no, U_F_NAME = fname, U_M_NAME = mname, U_L_NAME = lname, STATE = state, DISTRICT = district, CITY = city, PINCODE = pincode, LINE1 = addrline1, U_ROLE = 'P')
        cursor.execute('insert into USERDETAILS (U_EMAIL,U_PASSWORD,U_PHONE,U_F_NAME,U_M_NAME,U_L_NAME,STATE,DISTRICT,CITY,PINCODE,LINE1,U_ROLE) values (:U_EMAIL, :U_PASSWORD, :U_PHONE, :U_F_NAME, :U_M_NAME, :U_L_NAME, :STATE, :DISTRICT, :CITY, :PINCODE, :LINE1, :U_ROLE)', userdata)
        cursor.close()
    
    return 'sign up'

def LocationDetails():
    if request.method == 'GET':
        conn = get_db()
        cursor = conn.cursor()
        id = request.args.get("id")
        query = "SELECT l.*, h.*, t.TRAIN_ID, t.COST_PER_SEAT AS train_cost, c.CAB_ID, c.COST_PER_SEAT AS cab_cost ,b.bus_id, b.COST_PER_SEAT AS bus_cost FROM travelpackg to1 INNER JOIN LOCATION l ON to1.L_ID = l.L_ID INNER JOIN hotel h ON h.H_ID = to1.hotel_id LEFT JOIN train t ON t.TRAIN_ID = to1.train_id LEFT JOIN cab c ON c.CAB_ID = to1.CAB_ID LEFT JOIN bus b ON b.bus_id = to1.bus_id WHERE l.L_ID = :id"
        cursor.execute(query, dict(id = id))
        packDetails = cursor.fetchone()
        cursor.execute("SELECT * FROM LOC_IMAGES li where L_ID=:id", dict(id = id))
        imgDetails = cursor.fetchall()
        print(packDetails)
        print(imgDetails)
        cursor.close()
    return render_template("/PassengerSite/locationdetails.html", imgDetails=imgDetails, packDetails=packDetails)