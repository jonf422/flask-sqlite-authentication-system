# CS2660 Lab 9 - Flask/SQlite Web Authentication System
Jonathan Freed | University of Vermont | CS2660 - Cybersecurity Principles

4/31/2026

## Description
This lab expanded on the authentication system from Lab 1. It is a flask-based web app with a secure user authentication system.

Users can create an account or log in with existing test credentials. The authentication is handled by an SQlite based db class which initializes the database and populates with test accounts. It also handles password hashing (40 char salt), and account locking after 3 failed attempts. A strong password generator is also present.

Authenticated users can access a nav bar which has links to various pages with differing account level requirements. For example, Engineering is only accessable to users with ACCESS_LEVEL_STANDARD, or ACCESS_LEVEL_ADMIN, while pages such as IT Help are available to all authenticated users.

## Setup

### Requirements
- Python 3.10+
- Flask

### Database Initialiation
Run the initialization script (init_db.py) once before starting the app. This creates the SQLite database and seeds it with three default users:

| Username | Password | Access Level |
|---|---|---|
| userA | UserApass3! | Admin (3) |
| userB | UserBpass2! | Standard (2) |
| userC | UserCpass1! | Limited (1) |

## Testing
After initializing the database, runn app.py to start the Flask app and navigate to the web app

## References
- https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
- https://www.geeksforgeeks.org/javascripthow-to-generate-a-random-password-using-javascript/
- https://en.fmyly.com/article/where-does-nav-go-in-html/
- https://flask.palletsprojects.com/en/stable/quickstart/
- https://docs.python.org/3/library/hashlib.html
- Code from cs-2660-catamount-community-bank - Professor Jim Eddy
