from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, session
import os

def AdminHome():
    return render_template('/AdminSite/AdminHome.html')

def AdminContact():
    return render_template('/AdminSite/AdminHome.html')