import os
import logging
import csv
import hashlib
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


mypath = os.getcwd()
FORMAT = '%(asctime)s [ %(levelname)s ]  :  %(message)s'
logging.basicConfig(filename=mypath + '\\log.txt', level=logging.INFO, filemode="w", format=FORMAT,
                    datefmt="Date %d/%m/%y Time: %I:%M:%S %p")

class MyApp:

    def __init__(self):
        self.root = Tk()
        self.root.minsize(250,150)
        self.root.geometry=('700x550+300+400')
        self.root.configure(background='gray')
        self.root.resizable()
        self.menu = Menu(self.root)
        self.root.config(menu= self.menu)
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label= "File", menu= self.file_menu)
        self.file_menu.add_command(label= "open file ", command= self.openfile)
        self.file_menu.add_command(label="Exit ", command=self.exit)
        self.help_menu = Menu(self.menu)
        self.menu.add_cascade(label="help",menu= self.help_menu)
        self.help_menu.add_command(label="about ", command=self.about)
        self.root.configure(borderwidth=5 ,highlightthickness= 7 )

        self.root.title("Head")
        self.reggstion_button = Button(self.root, text= "reggstion", command=self.regapp )
        self.reggstion_button.grid(column= 0 , row= 7, sticky= SE)
        self.login_button = Button(self.root, text="Login", command= self.logginapp)
        self.login_button.grid(column= 4 , row=7, sticky= SW)
        tit_label = ttk.Label(self.root, background='gray', font=('David', 25), text="AMB project")
        tit_label.grid(column=1, row=1, ipadx=5, ipady=5, sticky= N)

        Ask_label = ttk.Label(self.root, background='gray',font= 'David' ,text="What do you want to do?:")
        Ask_label.grid(column=1, row=4, ipadx=5, ipady=5, sticky= NSEW)
        print(logging.info('menu is run'))

    def exit(self):
        one_last_step = messagebox.askyesno('you r going to getout!',"are you sure?")
        if one_last_step == YES:
            messagebox.showinfo("exit","bey bey")
            self.root.quit()

    def about(self):
        messagebox.showinfo("about the progrem", "the program was created by Ahihod Buchnik")

    def openfile(self):
        global pathname ,pathfile
        my_p =StringVar()
        pathfile = Toplevel()
        #pathfile.grid(baseWidth=10,baseHeight=5)
        pathname = Entry(pathfile, textvariable=my_p )
        pathname.grid(column=1,row=1,columnspan=1,rowspan=15)
        ok_but = Button(pathfile, text= "OK", command=self.write_to_csv_DB)
        ok_but.grid(column=3,row=3)


    def regapp(self):
        global  e1, e2, e3 ,e4, top
        top = Toplevel()
        part_text1 =StringVar()
        part_text2 = StringVar()
        part_text3 = StringVar()
        part_text4 = StringVar()
        l1 = Label(top, text= "first name:",font=("David", 16))
        l2 = Label(top, text="Last name:", font=("David", 16))
        l3 = Label(top, text="usr name:", font=("David", 16))
        l4 = Label(top, text="password:", font=("David", 16))
        l1.grid(row=1,column=0, columnspan=3)
        l2.grid(row=2, column=0, columnspan=3)
        l3.grid(row=3, column=0, columnspan=3)
        l4.grid(row=4, column=0, columnspan=3)
        e1 = Entry(top,textvariable=part_text1)
        e2 = Entry(top,textvariable=part_text2)
        e3 = Entry(top,textvariable=part_text3)
        e4 = Entry(top , show="*",textvariable=part_text4)
        e1.insert(0,"enter your name")
        e2.insert(0, "enter your last name")
        e3.insert(0, "enter your user name")
        e4.insert(0, "enter your password")
        e1.grid(row=1,column=4)
        e2.grid(row=2, column=4)
        e3.grid(row=3, column=4)
        e4.grid(row=4, column=4)
        OK_button = Button(top, text="let's reggstion", command=self.send_to_mem)
        OK_button.grid(column=2, row=5, sticky=SW)




    def send_to_mem(self):
        mem = [e1.get(),e2.get(),e3.get(),haspassword(e4.get())]
        self.write_to_file(mem)
        top.destroy()
        self.run()

    def logginapp(self):
        # login window
        global password_entry, username_entry, login
        login = Toplevel()

        login.title('Login')
        login.resizable()

        # configure the grid
        login.columnconfigure(0, weight=1)
        login.columnconfigure(1, weight=3)

        # username
        username_label = ttk.Label(login, text="Username:")
        username_label.grid(column=0, row=0,  padx=5, pady=5)

        username_entry = ttk.Entry(login)
        username_entry.grid(column=1, row=0,  padx=5, pady=5)

        # password
        password_label = ttk.Label(login, text="Password:")
        password_label.grid(column=0, row=1,  padx=5, pady=5)

        password_entry = ttk.Entry(login, show="*")
        password_entry.grid(column=1, row=1,  padx=5, pady=5)

        # login button
        login_button = ttk.Button(login, text="Login", command= self.try_connect)
        login_button.grid(column=1, row=3,  padx=5, pady=5)
        timen=f"{time.gmtime().tm_mday}\\{time.gmtime().tm_mon}\\{time.gmtime().tm_year}  {time.gmtime().tm_hour}:{time.gmtime().tm_min}:{time.gmtime().tm_sec}"
        time_label = ttk.Label(login,text= timen )
        time_label.grid(column=0, row=3)
        login.mainloop()
        pass

    def try_connect(self):
        mem = [username_entry.get(),haspassword(password_entry.get())]
        check =self.find_usr_in_csv(mem[0],mem[1])
        if check is None:
            logging.info("try to get access with wrong user! ")
            messagebox.showerror("not access", "the user isn't exist ")
        elif check is False:
            logging.info("try to get access with wrong password! ")
            messagebox.showerror("not access","the password is wrong ")
        elif check is True:
            logging.info("succss to login")
            messagebox.showinfo("login", f"wellcom {mem[0]}")
            login.quit()

    def find_usr_in_csv(self,user,password, p=mypath):
        with open(p + r'\database.csv', 'r') as fd_csv:
            csvread= csv.reader(fd_csv,delimiter =",")

            for line in csvread:
                if line[2] == user:
                    if line[3] == password:
                        return True
                    else:
                        return False
                else:
                    continue
            return None


    def run(self):
        self.root.mainloop()

    def write_to_file(self,data, p=mypath):
        with open(p + r'\database.csv', 'a') as fd_csv:
            csvfile= csv.writer(fd_csv,delimiter =",", lineterminator= '\n')
            csvfile.writerow(data)
            logging.info("the User  add to mem")

    def write_to_csv_DB(self, pathto=mypath):
        pathfrom = pathname

        pathfile.destroy()
        if os.path.exists(str(pathfrom)) is True:
            self.write_to_csv_DB(str(pathfrom))
            with open (str(pathfrom), 'r') as read_file:
                for line in read_file:

                    data_for_read = line
                    with open(pathto + r'\database.csv', 'a') as fd_csv:
                        csvfile= csv.writer(fd_csv,delimiter =",", lineterminator= '\n')
                        csvfile.writerow(data_for_read)

def haspassword(passw):
    result = hashlib.sha256(passw.encode())
    return (result.hexdigest())


app =MyApp()
app.run()