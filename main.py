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
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=2)
    root.rowconfigure(0, weight=1)
    return root


# Login/Register
def layout() :
    # left = Frame(master,bg='#AB886D')
    top.grid(row=0,sticky='news')
    top.rowconfigure(0,weight=1)
    top.columnconfigure(0,weight=1)
    # right = Frame(master,bg='#D6C0B3')
    center.grid(row=1,sticky='news')
    center.rowconfigure((0,1,2,3,4),weight=1)
    center.columnconfigure((0,1),weight=1)

def loginlayout():
    global userentry, pwdentry
    loginFrame.rowconfigure((0,1,2,3),weight=1)
    loginFrame.columnconfigure((0,1),weight=1)
    loginFrame.grid(row=0,column=0,columnspan=2,sticky='news')
    Label(loginFrame, text="Account Login", font="Garamond 26 bold", bg='#8fd9a8', fg='white').grid(row=0,columnspan=2)
    Label(loginFrame, text="Username: ", bg='#8fd9a8', fg='white').grid(row=1, column=0, sticky='e')
    userentry = Entry(loginFrame, bg='white', width=20)
    userentry.grid(row=1, column=1, sticky='w')
    Label(loginFrame, text="Password: ", bg='#8fd9a8', fg='white').grid(row=2, column=0, sticky='e')
    pwdentry = Entry(loginFrame, bg='white', width=20, show='*')
    pwdentry.grid(row=2, column=1, sticky='w')
    Button(loginFrame, text="Login", command=lambda: loginclick(userentry.get(), pwdentry.get())).grid(row=3, column=1, pady=20)
    Button(loginFrame, text="Register", command=register_layout).grid(row=3, column=0, pady=20)

def loginclick(user, pwd):
    if user == "" or pwd == "":
        messagebox.showwarning("Warning", "Please enter username and password")
        return

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
    result = cursor.fetchone()
    if result:
        global current_user
        current_user = user
        messagebox.showinfo("Success", "Login successful")
        loginFrame.grid_forget()
        menu() 
    else:
        messagebox.showerror("Error", "Invalid credentials")
    
def register_layout():
    register.rowconfigure((0,1,2,3,4),weight=1)
    register.columnconfigure((0,1),weight=1)
    register.grid_forget()
    register.grid(row=0,column=0,columnspan=2,sticky='news')
    global reg_user, reg_pwd, reg_name
    reg_user = Entry(register, width=20)
    reg_pwd = Entry(register, width=20, show='*')
    reg_name = Entry(register, width=20)

    reg_user = Entry(register, width=20)
    reg_pwd = Entry(register, width=20, show='*')
    reg_name = Entry(register, width=20)
    Label(register, text="Register Account").grid(row=0, columnspan=2)
    Label(register,text="Name").grid(row=1,column=0)
    reg_name.grid(row=1,column=1)
    Label(register, text="Username:").grid(row=2, column=0)
    reg_user.grid(row=2, column=1)
    Label(register, text="Password:").grid(row=3, column=0)
    reg_pwd.grid(row=3, column=1)
    Button(register, text="Create Account", command=register_account).grid(row=4,column=1, pady=10)
    Button(register, text="Back", command=go_back_to_login).grid(row=4,column=0)

def register_account():
    username = reg_user.get()
    password = reg_pwd.get()
    name = reg_name.get()

    if username == "" or password == "" or name == "":
        messagebox.showwarning("Warning", "Please fill in all fields")
        return

    try:
        cursor.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", (username, password, name))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully")
        go_back_to_login()
    except:
        messagebox.showerror("Error", "Username already exists")

def go_back_to_login():
    register.grid_forget()
    loginFrame.grid(sticky='news')

# Profile
def view_profile(username):
    cursor.execute("SELECT * FROM profiles WHERE username=?", (username,))
    profile_data = cursor.fetchone()
    conn.close()
    if not profile_data:
        messagebox.showerror("Error", "Profile no found")
        return
    menuFrame.grid_forget()
    profileFrame.grid(row=0,column=0,columnspan=2,sticky='news')
    Label(profileFrame, text="Profile", font=("Garamond", 26, "bold"), bg="#ECEFCA").pack(pady=20)
    Label(profileFrame, text=f"Username: {profile_data[1]}", bg="#ECEFCA", anchor="w").pack(pady=10)
    Label(profileFrame, text=f"Bio: {profile_data[2]}", bg="#ECEFCA", anchor="w", wraplength=600, justify="left").pack(pady=10)
    Button(profileFrame, text="Back to menu").pack(pady=20)

# Note
def notePage():
    global listNoteFrame, title
    loginFrame.grid_forget()
    profileFrame.grid_forget()
    todolistFrame.grid_forget()
    curNoteFrame.grid_forget()
    addNoteFrame.grid_forget()
    editNoteFrame.grid_forget()
    result = getNotes()
    noteFrame.rowconfigure(0, weight=1)
    noteFrame.rowconfigure((1,2,3), weight=2)
    noteFrame.columnconfigure(0, weight=1)
    noteFrame.grid(row=0, column=1, sticky="news")
    
    # Title must be defind at first frame
    title = Label(noteFrame, bg="#547792", fg="black", text="Note", font="Garamond 26 bold")
    title.grid(row=0, column=0, columnspan=2, sticky="news")

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
    Button(listNoteFrame, bg="white", fg="black", text="Edit note", width=10, command=lambda: editNote(spy.get())).grid(row=2, column=1, pady=20, sticky="n", ipady=10)


def showNote(id):
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
    addNoteFrame.columnconfigure((0,1), weight=1)
    addNoteFrame.grid(row=1, rowspan=3, column=0, sticky="news")

    title["text"] = "Add Note"

    # Local content frame
    formFrame = Frame(addNoteFrame, bg="white")
    formFrame.rowconfigure((0,1), weight=1)
    formFrame.columnconfigure((0,1), weight=1)
    formFrame.grid(row=0, rowspan=2, column=0, columnspan=2, sticky="news", padx=20, pady=20)

    Label(formFrame, bg="white", fg="black", text="Title:").grid(row=0, column=0, sticky="es", padx=20, pady=20)
    titleEntry = Entry(formFrame, bg="white", fg="black", width=20)
    titleEntry.grid(row=0, column=1, sticky="ws", padx=20, pady=20)
    Label(formFrame, bg="white", fg="black", text="Content:").grid(row=1, column=0, sticky="en", padx=20, pady=20)
    contentEntry = Text(formFrame, bg="white", fg="black", width=20, height=10)
    contentEntry.grid(row=1, column=1, sticky="wn", padx=20, pady=20)

    Button(addNoteFrame, bg="white", fg="black", text="Back", width=20, command=notePage).grid(row=2, column=0, padx=20, pady=25, ipadx=20, ipady=10, sticky="e")
    Button(addNoteFrame, bg="white", fg="black", text="Add", width=20, 
            command=lambda: addNoteClick([titleEntry.get(), contentEntry.get("1.0", "end-1c")])
            ).grid(row=2, column=1, padx=20, pady=25, ipadx=20, ipady=10, sticky="w")
    

def addNoteClick(data):
    if data[0] == "" or data[1] == "":
        messagebox.showwarning("Admin", "Please fill in all the data first")
    else:
        title = data[0].strip()
        content = data[1].strip()
        sql = f"INSERT INTO notes VALUES (null, ?, ?, ?)"
        cursor.execute(sql, [USER, title, content])
        conn.commit()
        messagebox.showinfo("Admin", "Add note successfully")
        notePage()


def editNote(id):
    if id == 0:
        messagebox.showwarning("Admin", "Please select note.")
        notePage()
        return
    else:
        sql = "SELECT * FROM notes WHERE id=?"
        cursor.execute(sql, [id])
        result = cursor.fetchone()
        if result:
            formFrame = Frame(editNoteFrame, bg="white")
            titleEntry = Entry(formFrame, bg="white", fg="black", width=20)
            contentEntry = Text(formFrame, bg="white", fg="black", width=20, height=10)
            titleEntry.insert(0, result[2])
            contentEntry.insert("1.0", result[3])
        else:
            messagebox.showwarning("Admin", "Something went wrong on fetching data from editNote()")
            print(f"ERROR on editNote(): ID is {id}. Is that exist in notes table?")
            notePage()
            return

    listNoteFrame.grid_forget()
    curNoteFrame.grid_forget()
    addNoteFrame.grid_forget()
    editNoteFrame.rowconfigure((0,1,2), weight=1)
    editNoteFrame.columnconfigure((0,1,2), weight=1)
    editNoteFrame.grid(row=1, rowspan=3, column=0, sticky="news")
    
    title["text"] = "Edit Note"

    # Local content frame
    formFrame.rowconfigure((0,1), weight=1)
    formFrame.columnconfigure((0,1), weight=1)
    formFrame.grid(row=0, rowspan=2, column=0, columnspan=3, sticky="news", padx=20, pady=20)

    Label(formFrame, bg="white", fg="black", text="Title:").grid(row=0, column=0, sticky="es", padx=20, pady=20)
    titleEntry.grid(row=0, column=1, sticky="ws", padx=20, pady=20)
    Label(formFrame, bg="white", fg="black", text="Content:").grid(row=1, column=0, sticky="en", padx=20, pady=20)
    contentEntry.grid(row=1, column=1, sticky="wn", padx=20, pady=20)

    Button(editNoteFrame, bg="white", fg="black", text="Back", width=15, command=notePage).grid(row=2, column=0, padx=5, pady=25, ipadx=15, ipady=10)
    Button(editNoteFrame, bg="white", fg="black", text="Update", width=15, 
           command=lambda: updateNote(id, [titleEntry.get(), contentEntry.get("1.0", "end-1c")])
           ).grid(row=2, column=1, padx=5, pady=25, ipadx=15, ipady=10)
    Button(editNoteFrame, bg="white", fg="black", text="Delete", width=15, command=lambda: deletNote(id)).grid(row=2, column=2, padx=5, pady=25, ipadx=15, ipady=10)


def updateNote(id, data):
    isUpdate =  messagebox.askyesno("Admin", "Are you really want to update?")
    if isUpdate:
        sql = "UPDATE notes SET title=?, content=? WHERE id=?"
        cursor.execute(sql, [data[0], data[1], id])
        conn.commit()
        messagebox.showinfo("Admin", "Update successfully")
        notePage()


def deletNote(id):
    isDelete =  messagebox.askyesno("Admin", "Are you really want to delete?")
    if isDelete:
        sql = "DELETE FROM notes WHERE id=?"
        cursor.execute(sql, [id])
        conn.commit()
        messagebox.showinfo("Admin", "Delete successfully")
        notePage()


def getNotes():
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
top = Frame(root,bg='#493628')
top2 = Frame(root,bg='#493628')
center = Frame(root,bg='#D6C0B3')
welcome = Frame(root,bg='#D6C0B3')
register = Frame(root,bg='#D6C0B3')
update = Frame(root,bg='#D6C0B3')
left = Frame(update,bg='#F5EFE7')
right = Frame(update,bg='#D8C4B6')
pwdinfo = StringVar()
cfinfo = StringVar()
nameinfo = StringVar()

# Config menuFrame 
menuFrame.rowconfigure((0,1,2,3,4), weight=1)
menuFrame.columnconfigure(0, weight=1)
Label(menuFrame, bg="#ECEFCA", fg="black", text="Personal Dashboard", font="Garamond 26 bold").grid(row=0, column=0, ipady=15)
Button(menuFrame, bg="white", fg="black", text="Profile", width=20).grid(row=1, column=0, ipady=15)
Button(menuFrame, bg="white", fg="black", text="Note", width=20).grid(row=2, column=0, ipady=15)
Button(menuFrame, bg="white", fg="black", text="To Do List", width=20).grid(row=3, column=0, ipady=15)
Button(menuFrame, bg="white", fg="black", text="Exit Program", width=20, command=exit).grid(row=4, column=0, ipady=15)
menuFrame.grid(row=0, column=0, sticky="news")

# Images

root.mainloop()