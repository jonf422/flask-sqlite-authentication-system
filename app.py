from flask import Flask, render_template, request, redirect, url_for
from db import Db

app = Flask(__name__)
db = Db()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    uname = request.form.get('uname')
    psw = request.form.get('psw')

    success, message = db.verify_user(uname, psw)
    if success:
        return render_template('home.html', error=message, loggedIn=success)
    return render_template('home.html', error=message)

@app.route('/signup', methods=['POST'])
def signup():
    uname = request.form.get('uname')
    psw = request.form.get('psw')

    success, message = db.reg_user(uname, psw)
    print(message)
    if success:
        return render_template('home.html', error=message, loggedIn=success)
    return render_template('home.html', error=message)

@app.route('/gen_pw')
def gen_pw():
    pw = db.gen_strong_pw()
    return render_template('home.html', strong_pw = pw)


if __name__ == '__main__':
    app.run()