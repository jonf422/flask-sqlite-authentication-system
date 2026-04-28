from db import Db

db = Db()
db.init_db()
db.populate_users()
print("Database initialized and seeded.")