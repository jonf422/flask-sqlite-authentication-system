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

    #TODO: authenticate user
    print(f'User logged in with username: {uname}, pass: {psw}')

    return redirect(url_for('home'))

@app.route('/signup', methods=['POST'])
def signup():
    uname = request.form.get('uname')
    psw = request.form.get('psw')

    success, message = db.reg_user(uname, psw)
    print(message)
    if success:
        return redirect(url_for('loggedIn'))
    return render_template('home.html', error=message)

@app.route('/loggedIn')
def loggedIn():
    return(render_template('loggedIn.html'))

if __name__ == '__main__':
    app.run()