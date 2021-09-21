from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, session
import os

from werkzeug.datastructures import Headers
from oracleCon import get_db, close_db
import config
# import requests
import json
import time
from requests_cache import CachedSession
from flask_caching import Cache

requests = CachedSession(expire_after=-1)


def checkDuplicate(locationResult, row):
    point = -1
    for elem in range(len(locationResult)): 
        if locationResult[elem][0] == row[0]:
            point = elem
    return point   

@cache.cached(timeout=86400)
def callDistanceMatrix(data, headers):
    getDistanceMatrix = requests.post(config.ROUTEURL + "/v2/matrix/driving-car", data=json.dumps(data), headers=headers)
    now = time.ctime(int(time.time()))
    getDistanceMatrix = getDistanceMatrix.json()
    return getDistanceMatrix


def calKmDistance(sloc, dloc):
    dloc = dloc.lower() + " india"
    sloc = sloc.lower() + " india"
    getSCor = requests.get(config.ROUTEURL + "/geocode/search", params={"text":sloc , "api_key":config.API_KEY})
    getSCor = getSCor.json()
    getDCor = requests.get(config.ROUTEURL + "/geocode/search", params={"text":dloc , "api_key":config.API_KEY})
    now = time.ctime(int(time.time()))
    print ("Time: {0} / Used Cache: {1}".format(now, getDCor.from_cache))
    getDCor = getDCor.json()
    headers = {"Content-Type":"application/json", "Authorization": config.API_KEY}
    data = {
        'locations':[getSCor["features"][0]["geometry"]["coordinates"],getDCor["features"][0]["geometry"]["coordinates"]],
        'metrics':["distance"]
    }
    print(data)
    getDistanceMatrix = callDistanceMatrix(data,headers)
    # getDistanceMatrix = requests.post(config.ROUTEURL + "/v2/matrix/driving-car", data=json.dumps(data), headers=headers)
    # now = time.ctime(int(time.time()))
    # print ("Time: {0} / Used Cache: {1}".format(now, getDistanceMatrix.from_cache))
    # getDistanceMatrix = getDistanceMatrix.json()
    # print(getDistanceMatrix["distances"][0][1]) 
    # print(getDCor)

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
        print("id:", id)
        query = "SELECT l.*, h.*, t.TRAIN_ID, t.COST_PER_SEAT AS train_cost, c.CAB_ID, c.COST_PER_SEAT AS cab_cost ,b.bus_id, b.COST_PER_SEAT AS bus_cost FROM travelpackg to1 INNER JOIN LOCATION l ON to1.L_ID = l.L_ID INNER JOIN hotel h ON h.H_ID = to1.hotel_id LEFT JOIN train t ON t.TRAIN_ID = to1.train_id LEFT JOIN cab c ON c.CAB_ID = to1.CAB_ID LEFT JOIN bus b ON b.bus_id = to1.bus_id WHERE l.L_ID = :id"
        cursor.execute(query, dict(id = id))
        packDetails = cursor.fetchone()
        cursor.execute("SELECT * FROM LOC_IMAGES li where L_ID=:id", dict(id = id))
        imgDetails = cursor.fetchall()
        print(packDetails)
        print(imgDetails)
        calKmDistance("Delhi",packDetails[4])
        mode = [[], []]
        if packDetails[15][0] == "T":
            mode[0].append("Train")
            mode[1].append(packDetails[16])
        if packDetails[15][0] == "B":
            mode[0].append("Train")
            mode[1].append(packDetails[16])
        if packDetails[15][0] == "C":
            mode[0].append("Cab")
            mode[1].append(packDetails[16])
        print(mode)
    return render_template("/PassengerSite/locationdetails.html", imgDetails=imgDetails, packDetails=packDetails, travelMode=mode)