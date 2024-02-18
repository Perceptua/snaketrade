# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template
from auth import Auth


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/authorize/<env>')
def authorize(env):
    authorize_url = Auth(env).get_authorize_url()
    
    return redirect(authorize_url)
    
        