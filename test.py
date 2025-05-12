from sqlite3 import *
from tkinter import *
from tkinter import messagebox
import textwrap

def connection():
    global conn, cursor
    conn = connect("database/project.db")
    cursor = conn.cursor()

def mainwindow():
    root = Tk()
    w = 1500
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


def frame():
    global checkBtns
    result = getData()
    left.grid(row=0, column=0, padx=20, pady=20, sticky="news")
    right.grid(row=0, column=1, padx=20, pady=20, sticky="news")
    checkBtns = []
    
    spy = [IntVar() for item in result]
    for i,item in enumerate(result):
        if item[3] == 0:
            checkBtns.append(Checkbutton(left, text=item[2], variable=spy[i], onvalue=1, command=lambda var=spy[i], id=item[0] : click(var, id)))
        else:
            checkBtns.append(Checkbutton(right, text=item[2], variable=spy[i], onvalue=0, command=lambda var=spy[i], id=item[0]: click(var, id)))
    
    for item in checkBtns:
        item.pack()
       

   
def click(spy, id):
    value = spy.get()
    print(value)
    sql = "UPDATE to_do_list SET is_done=? WHERE id=?"
    cursor.execute(sql, [value, id])
    conn.commit()

    for item in checkBtns:
        item.destroy()

    frame()
            



def getData():
    sql = "SELECT * FROM to_do_list WHERE username=?"
    cursor.execute(sql, ["test1"])
    result = cursor.fetchall()
    return result


connection()
root = mainwindow()
right = Frame(root, bg="white")
left = Frame(root, bg="white")

frame()
root.mainloop()