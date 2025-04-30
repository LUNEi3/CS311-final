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
loginFrame = Frame(root, bg="black")
menuFrame = Frame(root, bg="black")
profileFrame = Frame(root, bg="black")
noteFrame = Frame(root, bg="black")
todolistFrame = Frame(root, bg="black")

# Config menuFrame 
menuFrame.rowconfigure((0,1,2,3,4), weight=1)
menuFrame.columnconfigure(0, weight=1)
Label(menuFrame, bg="white", fg="black", text="Logo").grid(row=0, column=0)
Button(menuFrame, bg="white", fg="black", text="Profile", width=20).grid(row=1, column=0)
Button(menuFrame, bg="white", fg="black", text="Note", width=20).grid(row=2, column=0)
Button(menuFrame, bg="white", fg="black", text="To Do List", width=20).grid(row=3, column=0)
Button(menuFrame, bg="white", fg="black", text="Exit Program", width=20).grid(row=4, column=0)

# Images


root.mainloop()