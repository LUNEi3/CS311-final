from sqlite3 import *
from tkinter import *

def connection():
    global conn, cursor
    conn = connect("database/project.db")
    cursor = conn.cursor()


def mainwindow():
    root = Tk()
    w = 1100
    h = 800
    x = root.winfo_screenwidth()/2 - w/2
    y = root.winfo_screenheight()/2 - h/2
    root.geometry("%dx%d+%d+%d"%(w,h,x,y))
    root.config(bg='#94B4C1')
    root.title("CS311 Final Project: ")
    root.columnconfigure((0,1), weight=1)
    root.rowconfigure(0, weight=1)
    return root


connection()
root = mainwindow()

# Frames


# Images


root.mainloop()