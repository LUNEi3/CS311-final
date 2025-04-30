# For insert, delete, or update data in database
from sqlite3 import *

conn = connect("database/project.db")
cursor = conn.cursor()

sql = "INSERT INTO notes (username, title, content) VALUES (?,?,?)"
cursor.execute(sql, ["test1", "Study", "I have to submit the CS project before 17th May 2025."])

conn.commit()