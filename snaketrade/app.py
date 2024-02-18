# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, request
from snaketrade.auth import Auth


app = Flask(__name__)
auth = None


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/authorize/<env>')
def authorize(env):
    auth = Auth(env)
    authorize_url = auth.get_authorize_url()
    
    return redirect(authorize_url)

@app.route('/verify', methods=['POST'])
def verify():
    verification_code = None
    
    if request.method == 'POST':
        verification_code = request.form['verification_code']
        
    return {'verification_code': verification_code}
    
        