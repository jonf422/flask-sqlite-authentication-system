import os
import sqlite3
import re
import hashlib

DB_PATH = 'users.db'

SALT_BYTES = 20
HASH_ALGORITHM = 'sha1'

PASSWORD_MIN = 8
PASSWORD_MAX = 25
STRONG_PW_LEN = 16

ACCESS_LVL_LIMIED = 1
ACCESS_LVL_STANDARD = 2
ACCESS_LVL_ADMIN = 3



class Db:
    def get_connection(self):
        #get connection to db
        try:
            return sqlite3.connect(DB_PATH)
        except sqlite3.Error:
            print("Could not connect to database")
            return False

    def init_db(self):
        #db table schema
        sql = '''
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                username        TEXT    NOT NULL UNIQUE,
                password_hash   TEXT    NOT NULL,
                access_level    INTEGER NOT NULL DEFAULT 1,
                failed_attempts INTEGER NOT NULL DEFAULT 0,
                locked          INTEGER NOT NULL DEFAULT 0
            );
        '''
        #get connection to db
        conn = self.get_connection()
        if not conn:
            return False
        try:
            conn.execute(sql)
            conn.commit()
        finally:
            conn.close()

    
    def hash_pw(self, plain_pw):
        #gen salt for pw
        salt = os.urandom(SALT_BYTES).hex()

        #hash digest
        digest = hashlib.new(HASH_ALGORITHM, bytes.fromhex(salt) + plain_pw.encode("utf-8"),
        ).hexdigest()

        #salted pw hash
        return salt+digest

    def verify_pw(self, plain_pw, stored_hash):
        #separate salt from hash
        salt_len = SALT_BYTES*2
        salt = stored_hash[:salt_len]
        expected = stored_hash[salt_len:]
        #verify
        digest = hashlib.new(HASH_ALGORITHM, bytes.fromhex(salt) + plain_pw.encode()).hexdigest()
        return digest == expected
        
    def reg_user(self, uname, plain_pw):

        #validate username and pw
        if not uname:
            return False, 'Username can\'t be empty'
        elif (len(plain_pw) < PASSWORD_MIN or len(plain_pw) > PASSWORD_MAX):
            return False, 'Password must be 8-25 characters'
        elif not re.search(r"[A-Z]", plain_pw):
            return False, "Password must contain at least one uppercase letter"
        elif not re.search(r"[a-z]", plain_pw):
            return False, "Password must contain at least one lowercase letter"
        elif not re.search(r"\d", plain_pw):
            return False, "Password must contain at least one number"
        elif not re.search(r"[!@#$%^&*()\-_=+\[\]{}|;:',.<>?/`~\"\\]", plain_pw):
            return False, "Password must contain at least one special character"
    
        #hash plain pw
        pw_hash = self.hash_pw(plain_pw)

        sql = '''INSERT INTO users (username, password_hash, access_level) VALUES (?, ?, ?);'''

        #execute sql
        conn = self.get_connection()
        if not conn:
            return False
        try:
            conn.execute(sql, (uname, pw_hash, ACCESS_LVL_STANDARD))
            conn.commit()
            return True, ''
        except sqlite3.Error:
            return False, 'Database Error Occurred'
        finally:
            conn.close()

    def verify_user(self, uname, plain_pw):
        #TODO: user verification given username and plaintext password
        # should add to log in attempts/lock account
        

    def populate_users(self):
        users = (['userA', 'userApass3!', ACCESS_LVL_ADMIN],
                 ['userB', 'userBpass2!', ACCESS_LVL_STANDARD],
                 ['userC', 'userCpass1!', ACCESS_LVL_LIMIED])
        
        sql = '''INSERT INTO users (username, password_hash, access_level) values (?,?,?)'''
        conn = self.get_connection()
        if not conn:
            return False
        try:
            for uname, pw, access in users:
                pw_hash = self.hash_pw(pw)
                conn.execute(sql, (uname, pw_hash, access))
            conn.commit()
            return True, ''
        except sqlite3.Error:
            return False, 'Database Error Occurred'
        finally:
            conn.close()