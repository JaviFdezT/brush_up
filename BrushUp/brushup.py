

from tkinter  import *
from tkinter import messagebox
from  bbdd import UsersDDBB,WordsDDBB
from  mainPage import StartApp
from __init__ import *
import time


class LoginPage(object):
    
    def __init__(self):
        """ Create the window in which the user can log in and sign in """
        self.window = Tk()
        
        self.window.geometry("400x210")
        self.window.resizable(0,0)
        self.f1 = Frame(self.window,bg='#B0FFFD')
        self.f2 = Frame(self.window,bg='#B0FFFD')
        Label(self.f1,text="\n Log in to your account.\n",font = "Helvetica 12 bold",background='#B0FFFD').grid(row=0, column=1, sticky=E+S, columnspan=1000,rowspan=1, padx=110)
        Label(self.f2,text="\n Log in to your account.\n",font = "Helvetica 12 bold",bg='#B0FFFD').grid(row=0, column=1, sticky=E+S, columnspan=1000,rowspan=1, padx=110)
        Label(self.f2, text="\nWrong user/password. Try it again \n",bg='#B0FFFD',fg="red").grid(row=6, column=1, sticky=E+N+S, columnspan=200)

        for frame in (self.f1, self.f2):
            frame.grid(row=0, column=0, sticky='news')

        self.window.title('Login Page')
        
        self.user = StringVar()
        self.password = StringVar()
        
        Label(self.f1, text='User:',width=25,bg='#B0FFFD').grid(row=1, column=1)
        Entry(self.f1, textvariable=self.user).grid(row=1, column=2)
        Label(self.f2, text='User:',width=25,bg='#B0FFFD').grid(row=1, column=1)
        Entry(self.f2, textvariable=self.user).grid(row=1, column=2)

        Label(self.f1, text='Password: ',width=25,bg='#B0FFFD',).grid(row=2, column=1)
        Entry(self.f1, textvariable=self.password,show="*").grid(row=2, column=2)
        Label(self.f2, text='Password: ',width=25,bg='#B0FFFD',).grid(row=2, column=1)
        Entry(self.f2, textvariable=self.password,show="*").grid(row=2, column=2)
 
        Button(self.f1, text='Log in', command=lambda:self.raise_frame(self.f2) or self.login()).grid(row=4, column=2)
        Button(self.f1, text='Sign in', command=lambda:self.signin()).grid(row=5, column=2)
        Button(self.f2, text='Log in', command=lambda:self.raise_frame(self.f2) or self.login()).grid(row=4, column=2)
        Button(self.f2, text='Sign in', command=lambda:self.signin()).grid(row=5, column=2)
        
        self.raise_frame(self.f1)
        self.window.mainloop() 
        
    def login(self):
            """ Login process """
            result = [self.user.get(), self.password.get()]
            con=UsersDDBB()
            users=list(con.showUsers())
            userExists=False
            for i in range(len(users)):
                if str(result[0])==users[i][0] and str(result[1])==users[i][1]:
                    self.window.destroy()
                    logging.info("{!s} has logged in".format(str(result[0])))
                    StartApp(str(result[0]))
                    userExists=True
            if userExists==False:     
                self.raise_frame(self.f2)
                
    def signin(self):
            """ Check if a provided username already exists before proceeding to create it """
            result = [self.user.get(), self.password.get()]
            con=UsersDDBB()
            users=list(con.showUsers())
            userExists=False
            for i in range(len(users)):
                if str(result[0])==users[i][0]:
                    userExists=True
                    break
            if userExists or len(str(self.user.get()))<3:
                print(str(self.user.get()))
                messagebox.showerror("Caution", "This username is already been used or is too short")
            else:
                logging.info("new user".format(str(self.user.get())))
                self.createUser(str(self.user.get()), str(self.password.get()))
                
    def createUser(self,user,password):
        """ Create a new user """
        C=UsersDDBB()
        C.insUs(user, password)
        C.closeCon()
        C=WordsDDBB(user)
        C.createTables()
        now=time.localtime( time.time())
        mm=str(now.tm_mon) if len(str(now.tm_mon))==2 else "0"+str(now.tm_mon)
        dd=str(now.tm_mday) if len(str(now.tm_mday))==2 else "0"+str(now.tm_mday)
        day="{!s}/{!s}/{!s}".format(str(now.tm_year),mm,dd)
        C.insWord("brush up","My spoken French is quite good, but I would like to brush up a bit","repasar, hacer un repaso","v",1,day)
        C.closeCon()
        file=open("PROPS/props.properties",'r')
        props={}
        for line in file:
            temp=line.replace("\n","").split("=")
            if len(temp)==2:
                props[str(temp[0])]=str(temp[1])
        file.close()
        props["boolsendT"+str(user)]=False
        file=open("PROPS/props.properties",'w')
        for i in props:
            file.write(str(i)+"="+str(props[i])+"\n")
        file.close()
        messagebox.showinfo("Done!", "Your account has been created. Please, log in")
        self.raise_frame(self.f1)
        
    def raise_frame(self,frame):
        """ Raise a new frame inside the window """
        frame.tkraise()
    
c=LoginPage()  
