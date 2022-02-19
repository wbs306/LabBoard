import sqlite3

from flask import current_app, g

def get_db():
    db = sqlite3.connect(current_app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    db = get_db()
    cursor = db.execute(query, args)
    db.commit()
    result = cursor.fetchall()
    db.close()
    return (result[0] if (result) else None) if (one) else result