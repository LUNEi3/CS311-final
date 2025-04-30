from sqlite3 import *

def connection():
    global conn, cursor
    conn = connect("database/project.db")
    cursor = conn.cursor()

connection()