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
    root.title("CS311 Final Project: Personal Dashboard")
    root.option_add("*font", "Garamond 20")
    root.columnconfigure((0,1), weight=1)
    root.rowconfigure(0, weight=1)
    return root


# Login/Register


# Profile


# Note
def notePage():
    loginFrame.grid_forget()
    profileFrame.grid_forget()
    todolistFrame.grid_forget()
    noteFrame.rowconfigure((0,1,2), weight=1)
    noteFrame.columnconfigure((0,1), weight=1)
    noteFrame.grid(row=0, column=1, sticky="news")
    Label(noteFrame, bg="#547792", fg="black", text="Note", font="Garamond 26 bold").grid(row=0, column=0, columnspan=2, sticky="news")

# To-do List


connection()
root = mainwindow()

# Frames
loginFrame = Frame(root, bg="black")
menuFrame = Frame(root, bg="#ECEFCA")
profileFrame = Frame(root, bg="black")
noteFrame = Frame(root, bg="#94B4C1")
todolistFrame = Frame(root, bg="black")

# Config menuFrame 
menuFrame.rowconfigure((0,1,2,3,4), weight=1)
menuFrame.columnconfigure(0, weight=1)
Label(menuFrame, bg="#ECEFCA", fg="black", text="Personal Dashboard", font="Garamond 26 bold").grid(row=0, column=0, ipady=15)
Button(menuFrame, bg="#ECEFCA", fg="black", text="Profile", width=20).grid(row=1, column=0, ipady=15)
Button(menuFrame, bg="#ECEFCA", fg="black", text="Note", width=20).grid(row=2, column=0, ipady=15)
Button(menuFrame, bg="#ECEFCA", fg="black", text="To Do List", width=20).grid(row=3, column=0, ipady=15)
Button(menuFrame, bg="#ECEFCA", fg="black", text="Exit Program", width=20, command=exit).grid(row=4, column=0, ipady=15)
menuFrame.grid(row=0, column=0, sticky="news")

# Images


# Testing sage
USER = "test1"
menuFrame.grid(row=0, column=0, sticky="news")
notePage()

root.mainloop()