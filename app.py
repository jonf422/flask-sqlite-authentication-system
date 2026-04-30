from flask import Flask, render_template, request, redirect, url_for
from db import Db, ACCESS_LVL_ADMIN, ACCESS_LVL_STANDARD, ACCESS_LVL_LIMIED

#flask/db setup
app = Flask(__name__)
db = Db()


@app.route('/')
def home():
    return render_template('home.html')

#login/signup

@app.route('/login', methods=['POST'])
def login():
    uname = request.form.get('uname')
    psw = request.form.get('psw')

    success, message = db.verify_user(uname, psw)
    if success:
        return render_template('home.html', error=message, loggedIn=success, user=uname)
    return render_template('home.html', error=message)

@app.route('/signup', methods=['POST'])
def signup():
    uname = request.form.get('uname')
    psw = request.form.get('psw')

    success, message = db.reg_user(uname, psw)
    print(message)
    if success:
        return render_template('home.html', error=message, loggedIn=success, user=uname)
    return render_template('home.html', error=message)

#strong pw generator
@app.route('/gen_pw')
def gen_pw():
    pw = db.gen_strong_pw()
    return render_template('home.html', strong_pw = pw)


#Nav links

@app.route('/accounting')
def accounting():
    uname = request.args.get('uname')
    user = db.get_user(uname)
    if not user or user[3] < ACCESS_LVL_STANDARD:
        return render_template('home.html', error='Access denied', user=uname)
    return render_template('accounting.html', loggedIn=True, user=uname)

@app.route('/admin')
def admin():
    uname = request.args.get('uname')
    print(uname)
    user = db.get_user(uname)
    print(user)
    if not user or user[3] < ACCESS_LVL_ADMIN:
        return render_template('home.html', error='Access denied', user=uname)
    return render_template('admin_panel.html', loggedIn=True, user=uname)

@app.route('/time_reporting')
def time_reporting():
    uname = request.args.get('uname')
    user = db.get_user(uname)
    if not user:
        return render_template('home.html', error='Access denied', user=uname)
    return render_template('time_reporting.html', loggedIn=True, user=uname)

@app.route('/engineering')
def engineering():
    uname = request.args.get('uname')
    user = db.get_user(uname)
    if not user or user[3] < ACCESS_LVL_STANDARD:
        return render_template('home.html', error='Access denied', user=uname)
    return render_template('engineering.html', loggedIn=True, user=uname)

@app.route('/it_help')
def it_help():
    uname = request.args.get('uname')
    user = db.get_user(uname)
    if not user:
        return render_template('home.html', error='Access denied', user=uname)
    return render_template('it_help.html', loggedIn=True, user=uname)

@app.route('/dashboard')
def dashboard():
    uname = request.args.get('uname')
    user = db.get_user(uname)
    if not user:
        return render_template('home.html', error='Access denied', user=uname)
    return render_template('home.html', loggedIn=True, user=uname)

if __name__ == '__main__':
    app.run()