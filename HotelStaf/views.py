from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, session
import os

def HotelStafHome():
    return render_template('/HotelStafSite/HotelStafHome.html')