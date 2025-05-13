from sqlite3 import *
from tkinter import *
from tkinter import messagebox
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


# To-do List


connection()
root = mainwindow()

# Frames
loginFrame = Frame(root, bg="black")
menuFrame = Frame(root, bg="#ECEFCA")
profileFrame = Frame(root, bg="black")
noteFrame = Frame(root, bg="black")
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



# Images
loginlayout()
root.mainloop()