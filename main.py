from sqlite3 import *
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import textwrap

def connection():
    global conn, cursor
    conn = connect("database/project.db")
    cursor = conn.cursor()


def mainwindow():
    root = Tk()
    w = 1300
    h = 800
    x = root.winfo_screenwidth()/2 - w/2
    y = root.winfo_screenheight()/2 - h/2
    root.geometry("%dx%d+%d+%d"%(w,h,x,y))
    root.config(bg='#94B4C1')
    root.title("CS311 Final Project: Personal Dashboard")
    root.option_add("*font", "Garamond 20")
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=5)
    root.rowconfigure(0, weight=1)
    return root


# Login/Register
def loginPage():
    global userentry, pwdentry
    register.grid_forget()
    menuFrame.grid_forget()
    profileFrame.grid_forget()
    noteFrame.grid_forget()
    TDLFrame.grid_forget()
    loginFrame.rowconfigure((0,1,2,3),weight=1)
    loginFrame.columnconfigure((0,1),weight=1)
    loginFrame.grid(row=0,column=0,columnspan=2,sticky='news')
    Label(loginFrame, text="Personal Dashboard", font="Garamond 26 bold", bg='#94B4C1', fg='black').grid(row=0,columnspan=2, sticky="news")
    Label(loginFrame, text="Username: ", bg='#ECEFCA', fg='black').grid(row=1, column=0, sticky='es', pady=20)
    userentry = Entry(loginFrame, bg='white', width=20)
    userentry.grid(row=1, column=1, sticky='ws', pady=20)
    Label(loginFrame, text="Password: ", bg='#ECEFCA', fg='black').grid(row=2, column=0, sticky='en', pady=20)
    pwdentry = Entry(loginFrame, bg='white', width=20, show='*')
    pwdentry.grid(row=2, column=1, sticky='wn', pady=20)
    Button(loginFrame, text="Login ", image=loginIcon, compound="right", command=lambda: loginclick(userentry.get(), pwdentry.get())).grid(row=3, column=1, pady=20, ipady=10, ipadx=50)
    Button(loginFrame, text="Register ", image=editIcon, compound="right", command=registerPage).grid(row=3, column=0, pady=20, ipady=10, ipadx=40)

def loginclick(user, pwd):
    global USER, NAME
    if user == "" or pwd == "":
        messagebox.showwarning("Admin", "Please enter username and password")
        return

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
    result = cursor.fetchone()
    if result:
        USER = result[0]
        NAME = result[2]
        messagebox.showinfo("Admin", "Login successful")
        loginFrame.grid_forget()
        profilePage()
    else:
        messagebox.showerror("Admin", "Invalid credentials")
    
def registerPage():
    global userEntry, pwdEntry, cmpwdEntry, nameEntry
    register.rowconfigure((0,5),weight=3)
    register.rowconfigure((1,2,3,4), weight=1)
    register.columnconfigure((0,1),weight=1)
    loginFrame.grid_forget()
    register.grid(row=0,column=0,columnspan=2,sticky='news')
    userEntry = Entry(register, width=20)
    pwdEntry = Entry(register, width=20, show='*')
    cmpwdEntry = Entry(register, width=20, show='*')
    nameEntry = Entry(register, width=20)

    Label(register, text="Register Account", bg="#94B4C1", fg="black", font="Garamond 26 bold").grid(row=0, columnspan=2, sticky="news")
    Label(register,text="Name:", bg="#ECEFCA").grid(row=1,column=0, sticky="e")
    nameEntry.grid(row=1,column=1, sticky="w")
    Label(register, text="Username:", bg="#ECEFCA").grid(row=2, column=0, sticky="e")
    userEntry.grid(row=2, column=1, sticky="w")
    Label(register, text="Password:", bg="#ECEFCA").grid(row=3, column=0, sticky="e")
    pwdEntry.grid(row=3, column=1, sticky="w")
    Label(register, text="Confirm Password:", bg="#ECEFCA").grid(row=4, column=0, sticky="e")
    cmpwdEntry.grid(row=4, column=1, sticky="w")
    Button(register, text="Create Account", width=20, command=registerClick).grid(row=5,column=1, ipady=10, pady=10)
    Button(register, text="Back", width=20, command=loginPage).grid(row=5,column=0, ipady=10)

def registerClick():
    if userEntry.get() == "" or cmpwdEntry.get() == "" or pwdEntry.get() == "" or nameEntry.get() == "":
        messagebox.showwarning("Admin", "Please fill in all fields")
        userEntry.focus_force()
    else:
        if cmpwdEntry.get() != pwdEntry.get():
            messagebox.showerror("Admin", "Password and Confirm Password are not match")
            cmpwdEntry.focus_force()
        else:
            cursor.execute("SELECT * FROM users WHERE username=?", [userEntry.get()])
            isExist = cursor.fetchone()
            if isExist:
                messagebox.showerror("Admin", "Username already exists")
            else:
                cursor.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", [userEntry.get(), pwdEntry.get(), nameEntry.get()])
                cursor.execute("INSERT INTO profiles VALUES (null, ?, ?)", [userEntry.get(), ""])
                messagebox.showinfo("Admin", "Account created successfully")
                loginPage()


# Profile
def profilePage():
    loginFrame.grid_forget()
    noteFrame.grid_forget()
    TDLFrame.grid_forget()
    editBioFrame.grid_forget()
    cursor.execute("SELECT * FROM profiles WHERE username=?", [USER])
    result = cursor.fetchone()
    if not result:
        messagebox.showerror("Admin", "Profile no found")
        return
    menuFrame.grid(row=0, column=0, sticky="news")
    profileFrame.rowconfigure(0, weight=1)
    profileFrame.rowconfigure((1,2,3), weight=3)
    profileFrame.columnconfigure(0, weight=1)
    profileFrame.grid(row=0, column=1, sticky='news')

    title = Label(profileFrame, bg="#547792", fg="black", text="Profile", font="Garamond 26 bold")
    title.grid(row=0, column=0, sticky="news")

    
    profileDataFrame.rowconfigure((0,1,2,3), weight=1)
    profileDataFrame.columnconfigure(0, weight=1)
    profileDataFrame.grid(row=1, rowspan=3, column=0, sticky="news")

    contentFrame = Frame(profileDataFrame, bg="white")
    contentFrame.rowconfigure((0,1,2), weight=1)
    contentFrame.columnconfigure(0, weight=1)
    contentFrame.grid(row=0, rowspan=3, column=0, sticky="news", padx=20, pady=20)

    Label(contentFrame, image=avatarIcon, bg="white").grid(row=0, column=0)
    Label(contentFrame, text=f"{NAME}", bg="white", font="Garamond 24 bold").grid(row=1, column=0, pady=20, sticky="s")
    Label(contentFrame, text=f"{result[2]}", bg="white", anchor="w", wraplength=600, justify="left").grid(row=2, column=0, pady=20, sticky="n")

    Button(profileDataFrame, bg="white", fg="black", image=editIcon, compound="right", text="Edit BIO ", command=editBio).grid(row=3, column=0, pady=20, ipadx=40, ipady=10)

def editBio():
    loginFrame.grid_forget()
    noteFrame.grid_forget()
    TDLFrame.grid_forget()
    profileDataFrame.grid_forget()
    cursor.execute("SELECT * FROM profiles WHERE username=?", [USER])
    result = cursor.fetchone()
    if result:
        formFrame = Frame(editBioFrame, bg="white")
        bioEntry = Text(formFrame, bg="white", fg="black", width=35, height=15)
        bioEntry.insert("1.0", result[2])
    else:
        messagebox.showerror("Admin", "Someting went wrong on fetching data in editBio()")
        profilePage()
        return
    
    editBioFrame.rowconfigure((0,1,2,3), weight=1)
    editBioFrame.columnconfigure((0,1), weight=1)
    editBioFrame.grid(row=1, rowspan=3, column=0, sticky="news")

    formFrame.rowconfigure((0,1), weight=1)
    formFrame.columnconfigure((0,1), weight=1)
    formFrame.grid(row=0, rowspan=3, column=0, columnspan=2, sticky="news", padx=20, pady=20)

    Label(formFrame, bg="white", fg="black", text="Bio:").grid(row=1, column=0, sticky="ne", padx=10, pady=20)
    bioEntry.grid(row=1, column=1, sticky="nw", padx=10, pady=20)

    Button(editBioFrame, bg="white", fg="black", text="Update Bio", width=15, command=lambda : updateBio(bioEntry.get("1.0", "end-1c"))).grid(row=3, column=1, padx=20, pady=20)
    Button(editBioFrame, bg="white", fg="black", text="Back", width=15, command=profilePage).grid(row=3, column=0, padx=20, pady=20)

def updateBio(bio):
    if len(bio) > 200:
        messagebox.showinfo("Admin", "Sorry, text must have fewer than 200 characters")
        return
    bio = bio.strip()
    isUpdate = messagebox.askyesno("Admin", "Are you sure to change Bio?")
    if isUpdate:
        cursor.execute("UPDATE profiles SET bio=? WHERE username=?", [bio, USER]) 
        conn.commit()
        messagebox.showinfo("Admin", "Update successfully")
        profilePage()


# Note
def notePage():
    global title, foundNoteFrame
    loginFrame.grid_forget()
    profileFrame.grid_forget()
    TDLFrame.grid_forget()
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
    
    foundNoteFrame = Frame(listNoteFrame, bg="white")
    spy = IntVar()
    if result == 0:
        foundNoteFrame.grid_forget()
        notFoundNoteFrame.grid(row=0, rowspan=3, column=0, sticky="news")
    else:
        notFoundNoteFrame.grid_forget()
        foundNoteFrame.rowconfigure(0, weight=1)
        foundNoteFrame.columnconfigure((0,1), weight=1)
        foundNoteFrame.grid(row=0, rowspan=3, column=0, sticky="news", padx=20, pady=20)
        for item in result:
            Radiobutton(foundNoteFrame, bg="white", fg="black", text=f"{item[2]}", font="Garamond 18", variable=spy, value=item[0], justify="left").pack(anchor="w", padx=10)

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
        wrapper = textwrap.TextWrapper(width=50) 
        texts = result[3].splitlines()
        content = []
        for item in texts:
            content.append(wrapper.fill(text=item))
        content = "\n".join(content)
        Label(contentFrame, bg="white", fg="black", text=f"Title: {result[2]}", font="Garamond 26 bold").grid(row=0, column=0, sticky="news")
        Label(contentFrame, bg="white", fg="black", text=f"{content}", justify="left").grid(row=1, column=0, sticky="nw", padx=20, pady=20)
    else:
        Label(contentFrame, bg="white", fg="black", text=f"Please select note.", font="Garamond 26 bold").grid(row=0, column=0, sticky="news")

    Button(curNoteFrame, bg="white", fg="black", text="Back", command=notePage).grid(row=0, column=1, pady=25, ipadx=20, ipady=10)
    foundNoteFrame.destroy()

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
    contentEntry = Text(formFrame, bg="white", fg="black", width=30, height=10)
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
        foundNoteFrame.destroy()
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
            contentEntry = Text(formFrame, bg="white", fg="black", width=30, height=10)
            titleEntry.insert(0, result[2])
            contentEntry.insert("1.0", result[3])
        else:
            messagebox.showwarning("Admin", "Something went wrong on fetching data in editNote()")
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
        foundNoteFrame.destroy()
        notePage()

def deletNote(id):
    isDelete =  messagebox.askyesno("Admin", "Are you really want to delete?")
    if isDelete:
        sql = "DELETE FROM notes WHERE id=?"
        cursor.execute(sql, [id])
        conn.commit()
        messagebox.showinfo("Admin", "Delete successfully")
        foundNoteFrame.destroy()
        notePage()

def getNotes():
    sql = "SELECT * FROM notes WHERE username=?"
    cursor.execute(sql, [USER])
    result = cursor.fetchall()
    if result:
        return result
    else:
        return 0


# To-do List
def TDLPage():
    global checkBtns
    loginFrame.grid_forget()
    profileFrame.grid_forget()
    noteFrame.grid_forget()
    result = getTDL()
    TDLFrame.rowconfigure((0,4), weight=1)
    TDLFrame.rowconfigure((1,2,3), weight=2)
    TDLFrame.columnconfigure((0,2), weight=3)
    TDLFrame.columnconfigure(1, weight=1)
    TDLFrame.grid(row=0, column=1, sticky="news")

    # Title
    title = Label(TDLFrame, bg="#547792", fg="black", text="To Do List", font="Garamond 26 bold")
    title.grid(row=0, column=0, columnspan=3, sticky="news")
    left = Frame(TDLFrame, bg="white")
    right = Frame(TDLFrame, bg="white")
    if result == 0:
        left.grid_forget()
        right.grid_forget()
        notFoundTDL.grid(row=1, rowspan=3, column=0, columnspan=3, sticky="news")
        notFoundTDL.lift()
    else:
        notFoundTDL.grid_forget()
        left.grid(row=1, rowspan=3, column=0, sticky="news", padx=20, pady=20)
        right.grid(row=1, rowspan=3, column=2, sticky="news", padx=20, pady=20)

        checkBtns = []
        spy = [IntVar() for item in result]
        for i,item in enumerate(result):
            if item[3] == 0:
                checkBtns.append(Checkbutton(left, bg="white", fg="black", text=item[2], variable=spy[i], onvalue=1, command=lambda var=spy[i], id=item[0]: taskToggle(var, id)))
            else:
                checkBtns.append(Checkbutton(right, bg="white", fg="black",text=item[2], variable=spy[i], onvalue=0, command=lambda var=spy[i], id=item[0]: taskToggle(var, id)))

        for item in checkBtns:
            item.pack(padx=10, pady=5, anchor="w")

    Button(TDLFrame, bg="white", fg="black", text="Add Task", width=10, command=addTask).grid(row=4, column=0, pady=20, ipady=10, ipadx=20)
    Button(TDLFrame, bg="white", fg="black", text="Clear Task", width=10, command=clearTask).grid(row=4, column=2, pady=20, ipady=10, ipadx=20)

def taskToggle(spy, id):
    value = spy.get()
    sql = "UPDATE to_do_list SET is_done=? WHERE id=?"
    cursor.execute(sql, [value, id])
    conn.commit()

    for item in checkBtns:
        item.destroy()
    TDLPage()

def addTask():
    newTask = simpledialog.askstring("Add Task", "Task:")
    newTask = newTask.strip()
    if newTask != "":
        sql = "INSERT INTO to_do_list VALUES (null, ?, ?, 0)"
        cursor.execute(sql, [USER, newTask])
        conn.commit()
        messagebox.showinfo("Admin", "Add new task successfully")
        TDLPage()

def clearTask():
    response = messagebox.askyesno("Admin", "This will clear all task that done")
    if response:
        sql = "DELETE FROM to_do_list WHERE is_done=1 AND username=?"
        cursor.execute(sql, [USER])
        conn.commit()
        messagebox.showinfo("Admin", "Clear successfully")
        TDLPage()

def getTDL():
    sql = "SELECT * FROM to_do_list WHERE username=?"
    cursor.execute(sql, [USER])
    result = cursor.fetchall()
    if result:
        return result
    else:
        return 0


connection()
root = mainwindow()

# Login and Register Frames
loginFrame = Frame(root, bg="#ECEFCA")
menuFrame = Frame(root, bg="#ECEFCA")
register = Frame(root,bg='#ECEFCA')

# Profile Frames
profileFrame = Frame(root, bg="#94B4C1")
profileDataFrame = Frame(profileFrame, bg="#94B4C1")
editBioFrame = Frame(profileFrame, bg="#94B4C1")

# Note Frames
noteFrame = Frame(root, bg="#94B4C1")
listNoteFrame = Frame(noteFrame, bg="#94B4C1")
curNoteFrame = Frame(noteFrame, bg="#94B4C1")
addNoteFrame = Frame(noteFrame, bg="#94B4C1")
editNoteFrame = Frame(noteFrame, bg="#94B4C1")
notFoundNoteFrame = Frame(listNoteFrame, bg="white")
Label(notFoundNoteFrame, bg="white", fg="black", text="No note here").pack(expand=TRUE)

# To-do List Frames
TDLFrame = Frame(root, bg="#94B4C1")
notFoundTDL = Frame(TDLFrame, bg="white")
Label(notFoundTDL, bg="white", fg="black", text="No task left to do").pack(expand=TRUE)

# Images
avatarIcon = PhotoImage(file="images/profile.png").subsample(2,2)
profileIcon = PhotoImage(file="images/user.png").subsample(10,10)
loginIcon = PhotoImage(file="images/enter.png").subsample(12,12)
logoutIcon = PhotoImage(file="images/logout.png").subsample(10,10)
noteIcon = PhotoImage(file="images/notes.png").subsample(10,10)
TDLIcon = PhotoImage(file="images/checklist.png").subsample(10,10)
editIcon = PhotoImage(file="images/edit.png").subsample(10, 10)

# Config menuFrame 
menuFrame.rowconfigure((0,1,2,3,4), weight=1)
menuFrame.columnconfigure(0, weight=1)
Label(menuFrame, bg="#ECEFCA", fg="black",text="Personal Dashboard", font="Garamond 26 bold").grid(row=0, column=0, ipady=15)
Button(menuFrame, bg="white", fg="black", image=profileIcon, compound="right", text="Profile  ", command=profilePage).grid(row=1, column=0, sticky="news", padx=20, pady=20)
Button(menuFrame, bg="white", fg="black", image=noteIcon, compound="right", text="Note  ", width=15, command=notePage).grid(row=2, column=0, sticky="news", padx=20, pady=20)
Button(menuFrame, bg="white", fg="black", image=TDLIcon, compound="right", text="To Do List  ", width=15, command=TDLPage).grid(row=3, column=0, sticky="news", padx=20, pady=20)
Button(menuFrame, bg="white", fg="black", image=logoutIcon, compound="right", text="Log out  ", width=15, command=loginPage).grid(row=4, column=0, sticky="news", padx=20, pady=20)


USER = ""
loginPage()
root.mainloop()