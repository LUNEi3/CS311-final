from sqlite3 import *
from tkinter import *
import textwrap

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
    global listNoteFrame
    loginFrame.grid_forget()
    profileFrame.grid_forget()
    todolistFrame.grid_forget()
    curNoteFrame.grid_forget()
    addNoteFrame.grid_forget()
    editNoteFrame.grid_forget()
    result = getNote()
    noteFrame.rowconfigure(0, weight=1)
    noteFrame.rowconfigure((1,2,3), weight=2)
    noteFrame.columnconfigure(0, weight=1)
    noteFrame.grid(row=0, column=1, sticky="news")
    Label(noteFrame, bg="#547792", fg="black", text="Note", font="Garamond 26 bold").grid(row=0, column=0, columnspan=2, sticky="news")

    # Local content frame
    listNoteFrame.rowconfigure((0,1,2), weight=1)
    listNoteFrame.columnconfigure(0, weight=5)
    listNoteFrame.columnconfigure(1, weight=1)
    listNoteFrame.grid(row=1, rowspan=3, column=0, sticky="news")
    
    foundFrame = Frame(listNoteFrame, bg="white")
    notFoundFrame = Frame(listNoteFrame, bg="white")
    spy = IntVar()
    if result == 0:
        foundFrame.grid_forget()
        Label(notFoundFrame, bg="white", fg="black", text="No note here").pack(expand=TRUE)
        notFoundFrame.grid(row=0, rowspan=3, column=0, sticky="news")
    else:
        notFoundFrame.grid_forget()
        foundFrame.rowconfigure(0, weight=1)
        foundFrame.columnconfigure((0,1), weight=1)
        foundFrame.grid(row=0, rowspan=3, column=0, sticky="news", padx=20, pady=20)
        for item in result:
            Radiobutton(foundFrame, bg="white", fg="black", text=f"{item[2]}", font="Garamond 18", variable=spy, value=item[0], justify="left").pack(anchor="w", padx=10)

    Button(listNoteFrame, bg="white", fg="black", text="Show note", width=10, command=lambda: showNote(spy.get())).grid(row=0, column=1, pady=20, sticky="s", ipady=10)
    Button(listNoteFrame, bg="white", fg="black", text="Add note", width=10, command=addNote).grid(row=1, column=1, pady=20, ipady=10)
    Button(listNoteFrame, bg="white", fg="black", text="Edit note", width=10).grid(row=2, column=1, pady=20, sticky="n", ipady=10)


def showNote(id):
    print(f"ID: {id}")
    listNoteFrame.grid_forget()
    addNoteFrame.grid_forget()
    editNoteFrame.grid_forget()
    curNoteFrame.rowconfigure((0,1,2), weight=1)
    curNoteFrame.columnconfigure((0), weight=5)
    curNoteFrame.columnconfigure((1), weight=1)
    curNoteFrame.grid(row=1, rowspan=3, column=0, sticky="news")

    contentFrame = Frame(curNoteFrame, bg="white")
    contentFrame.rowconfigure(0, weight=1)
    contentFrame.rowconfigure(1, weight=5)
    contentFrame.columnconfigure(0, weight=1)
    contentFrame.grid(row=0, rowspan=3, column=0, sticky="news", padx=20, pady=20)

    # Fetch content
    sql = "SELECT * FROM notes WHERE id=?"
    cursor.execute(sql, [id])
    result = cursor.fetchone()
    if result:
        Label(contentFrame, bg="white", fg="black", text=f"Title: {result[2]}", font="Garamond 26 bold").grid(row=0, column=0, sticky="news")
        Label(contentFrame, bg="white", fg="black", text=f"{result[3]}").grid(row=1, column=0, sticky="nw", padx=20, pady=20)
    else:
        Label(contentFrame, bg="white", fg="black", text=f"Please select note.", font="Garamond 26 bold").grid(row=0, column=0, sticky="news")

    Button(curNoteFrame, bg="white", fg="black", text="Back", command=notePage).grid(row=0, column=1, pady=25, ipadx=20, ipady=10)


def addNote():
    listNoteFrame.grid_forget()
    curNoteFrame.grid_forget()
    editNoteFrame.grid_forget()
    addNoteFrame.rowconfigure((0,1,2), weight=1)
    addNoteFrame.columnconfigure(0, weight=1)
    addNoteFrame.columnconfigure(1, weight=1)
    addNoteFrame.grid(row=1, rowspan=3, column=0, sticky="news")

    formFrame = Frame(addNoteFrame, bg="white")
    formFrame.rowconfigure((0,1), weight=1)
    formFrame.columnconfigure((0,1), weight=1)
    formFrame.grid(row=0, rowspan=2, column=0, columnspan=2, sticky="news", padx=20, pady=20)

    Label(formFrame, bg="white", fg="black", text="Title:").grid(row=0, column=0, sticky="es", padx=20, pady=20)
    titleEntry = Entry(formFrame, bg="white", fg="black", width=20)
    titleEntry.grid(row=0, column=1, sticky="ws", padx=20, pady=20)
    Label(formFrame, bg="white", fg="black", text="Content:").grid(row=1, column=0, sticky="en", padx=20, pady=20)
    contentEntry = Entry(formFrame, bg="white", fg="black", width=20)
    contentEntry.grid(row=1, column=1, sticky="wn", padx=20, pady=20)

    Button(addNoteFrame, bg="white", fg="black", text="Back", width=20, command=notePage).grid(row=2, column=0, padx=20, pady=25, ipadx=20, ipady=10, sticky="e")
    Button(addNoteFrame, bg="white", fg="black", text="Add", width=20).grid(row=2, column=1, padx=20, pady=25, ipadx=20, ipady=10, sticky="w")


def editNote():
    ...


def getNote():
    sql = "SELECT * FROM notes WHERE username=?"
    cursor.execute(sql, [USER])
    result = cursor.fetchall()
    if result:
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
curNoteFrame = Frame(noteFrame, bg="#94B4C1")
listNoteFrame = Frame(noteFrame, bg="#94B4C1")
addNoteFrame = Frame(noteFrame, bg="#94B4C1")
editNoteFrame = Frame(noteFrame, bg="#94B4C1")
todolistFrame = Frame(root, bg="black")

# Config menuFrame 
menuFrame.rowconfigure((0,1,2,3,4), weight=1)
menuFrame.columnconfigure(0, weight=1)
Label(menuFrame, bg="#ECEFCA", fg="black", text="Personal Dashboard", font="Garamond 26 bold").grid(row=0, column=0, ipady=15)
Button(menuFrame, bg="white", fg="black", text="Profile", width=20).grid(row=1, column=0, ipady=15)
Button(menuFrame, bg="white", fg="black", text="Note", width=20).grid(row=2, column=0, ipady=15)
Button(menuFrame, bg="white", fg="black", text="To Do List", width=20).grid(row=3, column=0, ipady=15)
Button(menuFrame, bg="white", fg="black", text="Exit Program", width=20, command=exit).grid(row=4, column=0, ipady=15)

# Images

USER = ""
root.mainloop()