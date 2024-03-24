"""
Snaketrade app.

Minimal Flask app for authenticating to the E-Trade API & viewing snaketrade
data.

"""
from flask import Flask, redirect, render_template, request
from snaketrade.auth import Auth


app = Flask(__name__)
auth = Auth('sandbox')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/authorize/<env>')
def authorize(env):
    auth.env = env
    auth.set_auth_components()

    return redirect(auth.authorize_url)


@app.route('/verify', methods=['POST'])
def verify():
    verification_code = None

    if request.method == 'POST':
        verification_code = request.form['verification_code']
        auth.make_session(verification_code)

    return {'verification_code': verification_code}
