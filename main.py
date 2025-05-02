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
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=2)
    root.rowconfigure(0, weight=1)
    return root


# Login/Register


# Profile


# Note
def notePage():
    loginFrame.grid_forget()
    profileFrame.grid_forget()
    todolistFrame.grid_forget()
    result = getNote()
    noteFrame.rowconfigure(0, weight=1)
    noteFrame.rowconfigure((1,2,3), weight=2)
    noteFrame.columnconfigure((0), weight=3)
    noteFrame.columnconfigure((1), weight=1)
    noteFrame.grid(row=0, column=1, sticky="news")
    Label(noteFrame, bg="#547792", fg="black", text="Note", font="Garamond 26 bold").grid(row=0, column=0, columnspan=2, sticky="news")

    foundFrame = Frame(noteFrame, bg="white")
    notFoundFrame = Frame(noteFrame, bg="white")
    spy = IntVar()
    if result == 0:
        foundFrame.grid_forget()
        Label(notFoundFrame, bg="#94B4C1", fg="black", text="No note here").pack(expand=TRUE)
        notFoundFrame.grid(row=1, rowspan=3, column=0, sticky="news")
    else:
        notFoundFrame.grid_forget()
        foundFrame.rowconfigure(0, weight=1)
        foundFrame.columnconfigure((0,1), weight=1)
        foundFrame.grid(row=1, rowspan=3, column=0, sticky="news", padx=20, pady=20)
        for item in result:
            Radiobutton(foundFrame, bg="white", fg="black", text=f"{item[2]}", font="Garamond 18", variable=spy, value=item[0], justify="left").pack(anchor="w", padx=10)

    Button(noteFrame, bg="#94B4C1", fg="black", text="Show note", width=10).grid(row=1, column=1, pady=20, sticky="s", ipady=10)
    Button(noteFrame, bg="#94B4C1", fg="black", text="Add note", width=10).grid(row=2, column=1, pady=20, ipady=10)
    Button(noteFrame, bg="#94B4C1", fg="black", text="Edit note", width=10).grid(row=3, column=1, pady=20, sticky="n", ipady=10)


def getNote():
    sql = "SELECT * FROM notes WHERE username=?"
    cursor.execute(sql, [USER])
    result = cursor.fetchall()
    if result:
        print(result)
        return result
    else:
        print("No result")
        return 0

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