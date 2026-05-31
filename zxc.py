import os
import sqlite3
db_name = 'quiz.sqlite'
conn = None
cursor = None

folder = os.getcwd()

items = [
    ('Паспорт, False'),
    ('Зубная щётка, False'),
    ('Зарядка, False'),
    ('Деньги, False'),
    ('Аптечка, False'),]

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
 
def show():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    response = cursor.execute("SELECT * FROM checklist")
    items = []
    for id, name, checked in response:
        items.append({'id': id, 'name': name, 'checked': checked}) 
    return items

def append(new_item):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO checklist VALUES (?, ?)", new_item)

def close():
    conn.commit()
    cursor.close()
    conn.close()
 
def do(query):
    cursor.execute(query)
    conn.commit()

def add(name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = f"INSERT INTO checklist (name, checked) VALUES (?, ?)"
    cursor.execute(query, (name, 0))
    conn.commit()

def clear_db():
    open()
    query = '''DROP TABLE IF EXISTS checklist'''
    do(query)
    close()
 
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    do('''CREATE TABLE IF NOT EXISTS checklist (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name VARCHAR,
               checked INTEGER DEFAULT 0)''')
    close()

def delete(item_id):
    open()
    do(f"DELETE FROM checklist WHERE id = {item_id}")
    close()

def delete_all():
    open()
    do("DELETE FROM checklist WHERE id > 0")
    close()

def checked(item_id):
    open()
    cursor.execute(f"SELECT checked FROM checklist WHERE id = {item_id}")
    result = cursor.fetchone() 
    cursor.execute(f"""
    UPDATE checklist 
    SET checked = 1
    WHERE id = {item_id}""")
    close()