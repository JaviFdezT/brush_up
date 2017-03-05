
import os
import shutil
import random
import math
import time
import sqlite3
import webbrowser
from tkinter  import *
from tkinter import filedialog,colorchooser,messagebox
from tkinter.ttk import *
import matplotlib.pyplot as plt
import PIL
import pronouncing
from PIL import ImageFont
from PIL import Image,ImageTk
from PIL import ImageDraw
from  bbdd import UsersDDBB,WordsDDBB
from  trymail import Email
from __init__ import *

class StartApp():
    """ 
    This is the class that will define the window where the game will appear, 
        its configuration, the dictionaries and theory. 
    """
    
    def __init__(self,loggedUser):
        """ 
        Once this class is executed, this function is run. 
        
        This method creates the window in which the user can play with his/her 
            content.  The properties of the new window are obtained from the 
            properties file.
        
        The self is defined
        """
        file=open("PROPS/props.properties",'r')
        props={}
        for line in file:
            temp=line.replace("\n","").split("=")
            if len(temp)==2:
                props[str(temp[0])]=str(temp[1])
        file.close()
        self.loggedUser=loggedUser
        self.window = Tk()
        #self.window.wm_iconbitmap(r"/icon.ico")
        self.window.resizable(0,0)
        try:
            self.width=int(props["width"])  
        except KeyError:
            self.width=750
        try:
            self.noptions=int(props["noptions"])  
        except KeyError:
            self.noptions=4
        try:
            self.height=int(props["height"])   
        except KeyError:
            self.height=350
        try:
            self.colour=str(props["colour"])  
        except KeyError:
            self.colour="#C8F9F9"  
        self.window.geometry(str(self.width)+"x"+str(self.height))
        self.MainMenu()
        self.window.title('BrushUp')
        self.currentUser=loggedUser
        self.s=Style()
        self.s.configure('My.TFrame',background=self.colour)
        self.window.mainloop()
        
        
    def MainMenu(self):
        """ 
        Shows the main menu 
        """
        self.window.configure(background=self.colour)
        self.f1 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        self.f1.columnconfigure(0,minsize=math.floor((self.width)/3))
        self.f1.columnconfigure(1,minsize=math.floor((self.width)/3))
        self.f1.columnconfigure(2,minsize=math.floor((self.width)/3))
        self.f1.grid(row=1, column=1, sticky='news')    
        
        Label(self.f1,text='Brush up!',font = "Helvetica 13 bold",background=self.colour).grid(row=1, column=1)
        Label(self.f1,text='JaviFdezT - February 2017', background=self.colour).grid(row=0, column=2)
        Label(self.f1,background=self.colour).grid(row=2, column=1)

        Button(self.f1, text='Play', command=lambda:self.letsPlay(),width=20).grid(row=3, column=1)
        Button(self.f1, text='Statistics', command=lambda:self.statistics(self.f1),width=20).grid(row=4, column=1)
        Button(self.f1, text='Dictionary', command=lambda:self.dictionary(self.f1),width=20).grid(row=5, column=1)
        Button(self.f1, text='Pronunciation', command=lambda:self.goToTheory(self.f1),width=20).grid(row=6, column=1)
        Button(self.f1, text='Insert new word', command=lambda:self.newWord(),width=20).grid(row=7, column=1)
        Button(self.f1, text='Delete word', command=lambda:self.deleteWord(),width=20).grid(row=8, column=1)
        Button(self.f1, text='Generate file with words', command=lambda:self.showWords(),width=20).grid(row=9, column=1)
        
        Label(self.f1,background=self.colour).grid(row=10, column=1)
        Button(self.f1, text='Credits', width=20, command=lambda:self.credits()).grid(row=12, column=1)
        Button(self.f1, text='Administration', width=20, command=lambda:self.Configure()).grid(row=11, column=1)
        Button(self.f1, text='Exit', width=20, command=lambda:self.exit()).grid(row=13, column=1)
        Label(self.f1,background=self.colour).grid(row=16, column=2)
            
        self.raise_frame(self.f1)
    
    def exit(self):
        """ 
        Closes the window and sends the daily mail if required 
        """
        self.window.destroy()
        file=open("PROPS/props.properties",'r')
        props={}
        for line in file:
            temp=line.replace("\n","").split("=")
            if len(temp)==2:
                props[str(temp[0])]=str(temp[1])
        file.close()
        try:
            if str(props["boolsendT"+self.loggedUser])==str(True):
                if str(props["boolincludestats"+self.loggedUser])==str(True):
                    C=WordsDDBB(self.loggedUser)
                    stats,numwords=C.showWordsAllLevels()
                    C.closeCon()
                    levels,counts=[],[]
                    for level in stats:
                        levels.append(int(level))
                        counts.append(int(stats[level]))
                    plt.bar(levels,counts,align='center')
                    plt.title("Statistics")
                    plt.xlabel("Level")
                    plt.ylabel("Number of words")
                    plt.xlim(0.5, 10.5)
                    plt.savefig('plot.png')
                E=Email(self.loggedUser)
                E.sendpic(str(props["boolincludeword"+self.loggedUser]),str(props["boolincludestats"+self.loggedUser]))
        except KeyError:
            file=open("PROPS/props.properties",'r')
            props={}
            for line in file:
                temp=line.replace("\n","").split("=")
                if len(temp)==2:
                    props[str(temp[0])]=str(temp[1])
            file.close()
            file=open("PROPS/props.properties",'w')
            props["boolsendT"+self.loggedUser]="False"
            for prop in props:
                file.write(str(prop)+"="+str(props[prop])+"\n")
            file.close()

            
    def ChangPass(self):
        """ 
        Frame to change the password associated with the user whose session is 
            opened.
        """
        self.f1.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')

        Label(f2,background=self.colour).grid(row=0)
        
        Label(f2, text="Changing password for {}".format(self.currentUser),font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=1)
        Label(f2,background=self.colour).grid(row=2)
        curpass=StringVar()
        Label(f2, text='Current password:  ',background=self.colour).grid(row=3, column=1)
        Entry(f2,textvariable=curpass,show="*").grid(row=3, column=2)
        
        passw=StringVar()
        Label(f2, text='New password:',background=self.colour).grid(row=4, column=1)
        Entry(f2,textvariable=passw,show="*").grid(row=4, column=2)
        
        passagain=StringVar()
        Label(f2, text='Repeat new password:  ',background=self.colour).grid(row=5, column=1)
        Entry(f2, textvariable=passagain,show="*").grid(row=5, column=2)
        
        Label(f2,background=self.colour).grid(row=6)
        
        Button(f2, text='Change password', command=lambda:self.ChangePass(passagain.get(),f2) if str(passw.get())==str(passagain.get()) and self.isCurpass(curpass.get()) and len(passw.get())>3 and str(passw.get())!=str(curpass.get()) else self.areDifferent(f2)).grid(row=7, column=1)
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=8, column=1)
    
    def statistics(self,frame):
        """ 
        Frame to show the statistics related to the number of words per level.
        
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
        """
        frame.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        C=WordsDDBB(self.loggedUser)
        stats,numwords=C.showWordsAllLevels()
        C.closeCon()
        levels,counts=[],[]
        
        Label(f2,background=self.colour).grid(row=0)
        Label(f2, text="Statistics",font = "Helvetica 12 bold",background=self.colour).grid(row=0, column=1)
        Label(f2,background=self.colour).grid(row=2)
        for level in stats:
            levels.append(int(level))
            counts.append(int(stats[level]))
            note="Level {!s} -> {!s} words".format(level,stats[level])
            Label(f2, text=note,font = "Helvetica 9 ",background=self.colour).grid(row=2+int(level), column=0)
        note="TOTAL -> {!s} words".format(str(numwords))
        Label(f2, text=note,font = "Helvetica 10 ",background=self.colour).grid(row=14, column=0)
        Label(f2,background=self.colour).grid(row=15)
        Button(f2, text='Statistics: word type', command=lambda:self.statsWord(f2)).grid(row=15, column=0)
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=16, column=0)
        fig=plt.figure()
        plt.bar(levels,counts,align='center')
        plt.title("Statistics")
        plt.xlabel("Level")
        plt.ylabel("Number of words")
        plt.xlim(0.5, 10.5)
        fig.savefig("IMG/temp.png")
        
        baseheight = self.height-50
        img = Image.open("IMG/temp.png")
        hpercent = (baseheight / float(img.size[1]))
        basewidth = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
        img.save("IMG/temp2.png")
        if basewidth>2*int(self.width)/3:
            basewidth = 2*int(self.width)/3       
            img = Image.open("IMG/temp2.png")
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((math.floor(basewidth), math.floor(hsize)), PIL.Image.ANTIALIAS)
            img.save("IMG/temp2.png")
        image = Image.open("IMG/temp2.png")
        image.load()
        photo = ImageTk.PhotoImage(image)
        label=Label(f2, image=photo)
        label.image = photo # keeping the reference
        label.grid(row=1, column=1, rowspan=19,columnspan=2)
        os.remove("IMG/temp.png")
        os.remove("IMG/temp2.png")
    
    def statsWord(self, frame):
        """ 
        Frame to show the statistics related to the number of words per word 
            type.
        
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
        """
        frame.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        C=WordsDDBB(self.loggedUser)
        stats,numwords=C.showWordsAllTypes()
        C.closeCon()
        wtype,counts=[],[]
        
        Label(f2,background=self.colour).grid(row=0)
        Label(f2, text="Statistics",font = "Helvetica 12 bold",background=self.colour).grid(row=0, column=1)
        Label(f2,background=self.colour).grid(row=2)
        ind=0
        for wt in stats:
            wtype.append(str(wt))
            counts.append(int(stats[wt]))
            note="Type: {!s} -> {!s} words".format(wt,stats[wt])
            Label(f2, text=note,font = "Helvetica 9 ",background=self.colour).grid(row=2+ind, column=0)
            ind+=1
        note="TOTAL -> {!s} words".format(str(numwords))
        Label(f2, text=note,font = "Helvetica 10 ",background=self.colour).grid(row=14, column=0)
        Label(f2,background=self.colour).grid(row=15)
        Button(f2, text='Statistics: level', command=lambda:self.statistics(f2)).grid(row=15, column=0)
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=16, column=0)
        fig=plt.figure()
        plt.bar(list(range(len(wtype))),counts,align='center')
        plt.xticks(list(range(len(wtype))), wtype)
        plt.title("Statistics")
        plt.xlabel("Word type")
        plt.ylabel("Number of words")
        fig.savefig("IMG/temp.png")
        
        baseheight = self.height-50
        img = Image.open("IMG/temp.png")
        hpercent = (baseheight / float(img.size[1]))
        basewidth = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
        img.save("IMG/temp2.png")
        if basewidth>2*int(self.width)/3:
            basewidth = 2*int(self.width)/3       
            img = Image.open("IMG/temp2.png")
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((math.floor(basewidth), math.floor(hsize)), PIL.Image.ANTIALIAS)
            img.save("IMG/temp2.png")
        image = Image.open("IMG/temp2.png")
        image.load()
        photo = ImageTk.PhotoImage(image)
        label=Label(f2, image=photo)
        label.image = photo # keeping the reference
        label.grid(row=1, column=1, rowspan=19,columnspan=2)
        os.remove("IMG/temp.png")
        os.remove("IMG/temp2.png")
        
    def newWord(self):
        """ 
        This method presents a frame to fill in a form with the data of the new 
            word to add. 
        """
        self.f1.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)

        Label(f2,background=self.colour).grid(row=0)
        Label(f2, text="Add a new word",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=1)
        Label(f2,background=self.colour).grid(row=2)
        
        word=StringVar()
        Label(f2, text='New word:',background=self.colour).grid(row=2, column=1)
        Entry(f2, textvariable=word).grid(row=3, column=1)
 
        example=StringVar()
        Label(f2, text='Example(s):',background=self.colour).grid(row=4, column=1)
        Entry(f2, textvariable=example).grid(row=5, column=1)
        
        meaning=StringVar()
        Label(f2, text='Meaning:',background=self.colour).grid(row=6, column=1)
        Entry(f2, textvariable=meaning).grid(row=7, column=1)
        
        syntax=StringVar()
        Label(f2, text='Word type:',background=self.colour).grid(row=8, column=1)
        input_position = Combobox(f2, values=sorted(["s","v","prep","conj","adv","adj","phrase/idiom"]),textvariable=syntax)
        input_position.current(6)
        input_position.grid(row=9, column=1)
      
        Button(f2, text='Insert new word', command=lambda:self.AddWord(f2, word.get(), example.get(), meaning.get(), syntax.get()) if len(str(word.get()))>0  else self.showError(f2)).grid(row=10, column=1)
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=14, column=1) 
        
        
    def AddWord(self,frame, word, example, meaning, syntax):
        """ 
        This method obtains the data from the form and uses it to add a new word 
            inside the database associated with the current user. 
        
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
            word: new word to be included
            example: example in which the word is used
            meaning: meaning of the word in the user's native language
            syntaxis: type of word (verb, preposition...)
        """
        C=WordsDDBB(self.loggedUser)
        now=time.localtime( time.time())
        mm=str(now.tm_mon) if len(str(now.tm_mon))==2 else "0"+str(now.tm_mon)
        dd=str(now.tm_mday) if len(str(now.tm_mday))==2 else "0"+str(now.tm_mday)
        day="{!s}/{!s}/{!s}".format(str(now.tm_year),mm,dd)
        C.insWord(str(word).strip(),str(example).strip(),str(meaning).strip(),str(syntax).strip(),1,day)
        C.closeCon()
        self.GoToMenu(frame)
      
    def goToTheory(self,frame):
        """ 
        This method shows the index associated with the prounuciation theory. 
        
        If the file  "DOCS/book.pdf" exists, it creates a button to open it. 
            This file should be a grammar book. The developer of this code does 
            not accept any liability with regard to the copyright permissions to 
            show that book.
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 

        """
        frame.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        Label(f2,background=self.colour).grid(row=0)
        Label(f2, text="Theory",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=1)
        Label(f2,background=self.colour).grid(row=2)
        Label(f2,background=self.colour).grid(row=4)
        Button(f2, text='Pronunciation: vowels', command=lambda:self.vowelsPron(f2)).grid(row=5, column=1)
        Button(f2, text='Pronunciation: diphthong', command=lambda:self.diptPron(f2)).grid(row=6, column=1)
        Button(f2, text='Pronunciation: consonants', command=lambda:self.consPron(f2)).grid(row=7, column=1)
        Button(f2, text='Look Up', command=lambda:self.lookUpWord(f2)).grid(row=3, column=1)
        Label(f2,background=self.colour).grid(row=12)
        if os.path.isfile("DOCS/book.pdf"):
            Label(f2,background=self.colour).grid(row=8) 
            Label(f2,background=self.colour).grid(row=11)        
            Button(f2, text='Grammar book', command=lambda:webbrowser.open_new("DOCS/book.pdf") and self.warnCopy()).grid(row=9, column=1)
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=13, column=1)
        
    @staticmethod
    def warnCopy():
        """ 
        This method shows warning related to the copyright permissions.
        
        Static method
        """
        messagebox.showinfo("Warning", "You could be using a file without the author's permissions. \n The developer of this code does not accept any liability with regard to this content.")
        
        
    def vowelsPron(self,frame):
        """ 
        This method shows the theory associated with the prounuciation of the 
            vowels. 
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 

        """
        frame.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        Label(f2,background=self.colour).grid(row=0)
        Label(f2, text="Pronunciation: vowels",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=1)
        Label(f2,background=self.colour).grid(row=2)
        image = Image.open("IMG/vowels.png")
        image.load()
        photo = ImageTk.PhotoImage(image)
        label=Label(f2, image=photo)
        label.image = photo # keeping the reference
        label.grid(row=3, column=0, rowspan=19,columnspan=3)
        Label(f2,background=self.colour).grid(row=12)
        Button(f2, text='Go back to \"Theory\"', command=lambda:self.goToTheory(f2)).grid(row=1, column=2)
    
    def diptPron(self,frame):
        """ 
        This method shows the theory associated with the prounuciation of the 
            diphthongs. 
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 

        """
        frame.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
    
        Label(f2, text="Pronunciation: diphthongs",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=1)
        image = Image.open("IMG/vowels.png")
        image.load()
        photo = ImageTk.PhotoImage(image)
        label=Label(f2, image=photo)
        label.image = photo # keeping the reference
        label.grid(row=2, column=0, columnspan=3)
        Label(f2,background=self.colour).grid(row=12)
        Button(f2, text='Go back to \"Theory\"', command=lambda:self.goToTheory(f2)).grid(row=0, column=2)
    
    
    def consPron(self,frame):
        """ 
        This method shows the theory associated with the prounuciation of the 
            consonants. 
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 

        """
        frame.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        Label(f2, text="Pronunciation: consonants",font = "Helvetica 12 bold",background=self.colour).grid(row=0, column=1)
        image = Image.open("IMG/cons.png")
        image.load()
        photo = ImageTk.PhotoImage(image)
        label=Label(f2, image=photo)
        label.image = photo # keeping the reference
        label.grid(row=2, column=0, columnspan=3)
        Label(f2,background=self.colour).grid(row=12)
        Button(f2, text='Go back to \"Theory\"', command=lambda:self.goToTheory(f2)).grid(row=0, column=2)
    
    @staticmethod
    def redirect(event):
        """ 
        This method opens the predefined web browser and shows the 
            "wordreference"  website. 
            
        Static method
        """
        webbrowser.open_new(r"http://www.wordreference.com")
    
    def lookUpWord(self,frame,word="brush"):
        """ 
        This method shows the phonetic transcription associated with a specific 
            word. If no word is provided, the default one is "brush".
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
            word: word whose phonetic transcription has to be shown to the user. 
                This transcription is shown as an image. If no word is provided, 
                the default one is "brush".

        """
        frame.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        Label(f2, text="Disctionary developed by using speech recognition. \nTo obtain a more accurate transcription, please go to",font = "Helvetica 8",background=self.colour).grid(row=0, column=0)
        link = Label(f2,text="www.wordreference.com", font = "Helvetica 8",foreground="#0000ff",background=self.colour,cursor="hand2")
        link.grid(row=1,column=0)
        link.bind("<Button-1>", self.redirect)
        Label(f2, text="Look for a word",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=1)
        Label(f2,background=self.colour).grid(row=0)
        inputword=StringVar()
        Entry(f2, textvariable=inputword).grid(row=3, column=1)
        Label(f2,background=self.colour).grid(row=4)
        Button(f2, text='Show transcription', command=lambda:self.lookUpWord(f2,word=str(inputword.get()))).grid(row=5, column=1)
        Label(f2,background=self.colour).grid(row=6)
        transcriptions=[]
        if word!="":
            if len(word.split())==1:
                tran=pronouncing.phones_for_word(word)
                listARPABET=[str(f).replace(".jpg","") for f in os.listdir("IMG/letters") if os.path.isfile(os.path.join("IMG/letters", f)) and str(f)!="unknown.jpg"]
                for i in tran:
                    ww=str(i).replace("0"," 0").replace("1"," 1").replace("2"," 2").split()
                    img=[]

                    for i in range(len(ww)):
                        if ww[i] in listARPABET:
                            rule=False
                            try:
                                if ww[i]=="EH" and ww[i+2]=="R":
                                    img.append("IMG/letters/ER.jpg")
                                    rule=True
                                elif ww[i]=="AA" and ww[i+2]=="R":
                                    img.append("IMG/letters/AL.jpg")
                                    rule=True
                                elif ww[i]=="ER" and ww[i+1]=="0" and ww[i+2]=="R":
                                    rule=True
                            except IndexError:pass
                            if not rule and ww[i]=="AH" and ww[i+1]=="0":
                                img.append("IMG/letters/EW.jpg")
                                rule=True
                            elif not rule and ww[i]=="EH" and ww[i+1]=="0":
                                img.append("IMG/letters/EW.jpg")
                                rule=True
                            elif not rule and ww[i]=="ER" and ww[i+1]=="0":
                                img.append("IMG/letters/EW.jpg")
                                rule=True 
                            elif not rule and ww[i]=="IY" and ww[i+1]=="0":
                                img.append("IMG/letters/IH.jpg")
                                rule=True 
                            try:
                                if not rule and ww[i]=="R" and ww[i-2]=="IH" and ww[i-1]!="0":
                                    img.append("IMG/letters/EW.jpg")
                                    rule=True
                            except IndexError:pass
                            if not rule:
                                img.append("IMG/letters/"+str(ww[i])+".jpg")
                            
                                
                        else:
                            img.append("IMG/letters/unknown.jpg")
                            
                    images = list(map(Image.open, img))
                    widths, heights = zip(*(i.size for i in images))

                    total_width = sum(widths)
                    max_height = max(heights)

                    new_im = Image.new('RGBA', (total_width, max_height))

                    x_offset = 0
                    for im in images:
                        new_im.paste(im, (x_offset,0))
                        x_offset += im.size[0]
                    new_im.save("IMG/tmp_"+"".join(str(ww).split())+".jpg")
                    transcriptions.append("IMG/tmp_"+"".join(str(ww).split())+".jpg")
                Label(f2, text=word,font = "Helvetica 12 bold",background=self.colour).grid(row=8, column=1)
                for i in range(len(transcriptions)):
                    image = Image.open(transcriptions[i])
                    image.load()
                    photo = ImageTk.PhotoImage(image)
                    label=Label(f2, image=photo)
                    label.image = photo # keeping the reference
                    label.grid(row=9+i, column=0, columnspan=3)
                    os.remove(transcriptions[i])
                if len(transcriptions)==0:
                    Label(f2, text="\nNOT TRANSCRIPTIONS FOUND\n\tFOR THIS WORD",font = "Helvetica 13 bold",background=self.colour).grid(row=9, column=1)
            else:
                self.lookUpWord(f2)
                messagebox.showerror("Error", "Only one word must be provided!")
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=0, column=2) 

        
        
    def dictionary(self,frame,inputword="brush up"):
        """ 
        This method shows the details associated with a specific word. If no
            word is provided, the default one is "brush up".
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
            inputword: word whose details has to be shown to the user. This 
                details are: word name, meaning, example (if it was provided
                when the word was added to the database) and level. If no
                word is provided, the default one is "brush up".

        """
        frame.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        C=WordsDDBB(self.loggedUser)
        words=C.showWords()
        C.closeCon()
        if inputword=="brush up":
            for i in words:
                if str(i[0])=="brush up":
                    inword=i
                    break
        else:
            inputword=inputword.split("[")[0].strip()
            for i in words:
                if str(i[0])==inputword:
                    inword=i
                    break
        
        Label(f2,background=self.colour).grid(row=0)
        Label(f2, text="Dictionary",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=1)
        Label(f2,background=self.colour).grid(row=2)
        Label(f2,background=self.colour).grid(row=2)
        
        listWords=[]
        for i in words:
            listWords.append(i[0]+"  ["+i[3]+"]")
        word=StringVar()
        Label(f2, text='Word:',background=self.colour).grid(row=3, column=1)

        input_position = Combobox(f2, values=sorted(listWords),textvariable=word,width=30)
        input_position.current(0)
        input_position.grid(row=4, column=1)
        
        Label(f2, width=20,background=self.colour).grid(row=5)
        Button(f2, text='Show word', command=lambda:self.dictionary(f2,inputword=str(word.get()))).grid(row=6, column=1)
        Label(f2,background=self.colour).grid(row=7, column=1)
        
        Label(f2, text="WORD: "+str(inword[0]),font = "Helvetica 12 bold",background=self.colour).grid(row=8, column=0, columnspan=3)
        Label(f2, text="MEANING: "+str(inword[2]),font = "Helvetica 11 bold",background=self.colour).grid(row=9, column=0, columnspan=3)
        if str(inword[1])!="":
            Label(f2, text="EXAMPLE(S): "+str(inword[1]),font = "Helvetica 10 bold",background=self.colour).grid(row=10, column=0, columnspan=3)
        Label(f2, text="LEVEL: "+str(inword[4]),font = "Helvetica 10 bold",background=self.colour).grid(row=11, column=0, columnspan=3)
        Label(f2, width=11,background=self.colour).grid(row=12)
        
        
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=13, column=1) 


    def deleteWord(self):
        """ 
        This method obtains the data from the word that the user wants to delete. 
            This word is picked out from a ComboBox.
        """
        self.f1.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        C=WordsDDBB(self.loggedUser)
        words=C.showWords()
        listWords=[]
        for i in words:
            listWords.append(i[0]+"  ["+i[3]+"]")
        C.closeCon()
            
        Label(f2,background=self.colour).grid(row=0)
        Label(f2, text="Delete an existing word",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=1)
        Label(f2,background=self.colour).grid(row=2)
        Label(f2,background=self.colour).grid(row=2)
        
        word=StringVar()
        Label(f2, text='Word:',background=self.colour).grid(row=3, column=1)

        input_position = Combobox(f2, values=sorted(listWords),textvariable=word,width=30)
        input_position.current(0)
        input_position.grid(row=4, column=1)
        
        Label(f2, width=20,background=self.colour).grid(row=5)
        Button(f2, text='Delete word', command=lambda:self.ByeWord(f2, word.get()) if len(str(word.get()))>0  else self.showError(f2)).grid(row=10, column=1)
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=14, column=1) 
        
        
    def ByeWord(self,frame, word):
        """ 
        This method obtains the data from the form and uses it to delete an
            existing word from the database associated with the current user. 
        
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
            word: word to be included
        """
        word=word.split("[")[0].strip()
        if word!="brush up":
            C=WordsDDBB(self.loggedUser)
            C.deleteWord(word)
            C.closeCon()
        self.GoToMenu(frame)      
        
    def areDifferent(self,frame):
        """ 
        Returns an error if 2 inputs dont match while trying to change the 
            current user's password.
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
        """
        Label(frame,background=self.colour).grid(row=9)
        frame.columnconfigure(0,minsize=math.floor((self.width)/3))
        frame.columnconfigure(1,minsize=math.floor((self.width)/3))
        frame.columnconfigure(2,minsize=math.floor((self.width)/3))
        Label(frame,background=self.colour).grid(row=9)
        Label(frame, text="Both passwords don't match, your current password is wrong or your new one is too short",background=self.colour).grid(row=10, column=0, columnspan=3)
        self.raise_frame(frame)
        
      
    def isCurpass(self,curp):
        """ 
        Checks if 2 inputs dont match while trying to change the current user's 
            password.
            
        Args:
            curp: string provided for the new user's password
        """
        connection = sqlite3.connect ('users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM USERS WHERE user=?', [self.currentUser])
        PASS=""
        for row in cursor:
            currow=str(row).replace("(", "").replace(")", "").replace("'", "").split(",")
            PASS=currow[1].strip()
        cursor.close()
        connection.close()
        BOO=False
        if PASS==curp:
            BOO=True
        return BOO
        
    def ChangePass(self,newpass,frame):
        """ 
        This method connects to the database "users.db" and changes the user's 
            password.
        """
        C=UsersDDBB()
        C.changePass(self.currentUser, newpass)
        C.closeCon()
        frame.columnconfigure(0,minsize=math.floor((self.width)/3))
        frame.columnconfigure(1,minsize=math.floor((self.width)/3))
        frame.columnconfigure(2,minsize=math.floor((self.width)/3))
        Label(frame,background=self.colour).grid(row=9)
        Label(frame, text="Password has been changed",background=self.colour).grid(row=10, column=0, columnspan=3) 
        self.raise_frame(frame)
        
        
    def raise_frame(self,frame):
        """ 
        Raises a new frame inside the window.
        
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
        """
        frame.tkraise()
        
    def GoToMenu(self,frame):
        """ 
        Destroys the current frame and shows the main menu.
        
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
        """
        frame.destroy()
        self.MainMenu()
        
    def showError(self, frame):
        """ 
        Returns an error related to incomplete information when the user is
            filling in a form 
        
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
        """
        messagebox.showerror("Wrong data", "Remember that all fields must be filled in ")
        
    def checkIfPlay(self,frame, level,wordOrMeaning,wordType):
        """ 
        Checks if there are words enough before proceeding to play
        
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
            level: level of the words that can be selected for the game. If all
                levels can be picked out, then level="all levels".
            wordOrMeaning: "Choose meaning" if the options to chose are the 
                meanings, or "Choose word" if the options to chose are the word
                names. 
            wordType: word type of the words that can be selected for the game.
                If all word types can be picked out, then wordType="all".
        """
        nList=[]
        C=WordsDDBB(self.loggedUser)
        if str(level)!="all levels":
            if str(wordType)!="all":
                words=C.showWordsByLevelwordType(int(str(level)),str(wordType))
                listWords=[]
                for i in words:
                    listWords.append(i[0])
                n=len(listWords)
            else:
                nList=[]
                for i in ["s","v","prep","conj","adv","adj","phrase/idiom"]:
                    listWords=C.showWordsByLevelwordTypewordType(int(str(level)),i)
                    nList.append(len(listWords))
                n=min(nList)
        else:
            if str(wordType)!="all":
                words=C.showWordswordType(str(wordType))
                listWords=[]
                for i in words:
                    listWords.append(i[0])
                n=len(listWords)
            else:
                nList=[]
                for i in ["s","v","prep","conj","adv","adj","phrase/idiom"]:
                    listWords=C.showWordswordType(i)
                    nList.append(len(listWords))
                n=min(nList)
        C.closeCon()
        
        
        if n<self.noptions:
            frame.grid_forget()
            f2 = Frame(self.window ,width=500, height=600, style='My.TFrame')
            f2.columnconfigure(0,minsize=math.floor((self.width)/3))
            f2.columnconfigure(1,minsize=math.floor((self.width)/3))
            f2.columnconfigure(2,minsize=math.floor((self.width)/3))
            f2.grid(row=0, column=0, sticky='news')
            self.raise_frame(f2)
            Label(f2,background=self.colour).grid(row=1,column=0)
            Label(f2, text="There are no words enough to play",font = "Helvetica 12 bold",background=self.colour).grid(row=2, column=0, columnspan=3)
            Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=14, column=1) 
        else:
            self.Play(frame, level,wordOrMeaning,wordType)
        
    def letsPlay(self):
        """ 
        Shows a form with the configuration for the game. 
        """
        self.f1.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)      
        
        Label(f2, text="Choose format",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=1)
        Label(f2,background=self.colour).grid(row=2)
        Label(f2,background=self.colour).grid(row=2)

        level=StringVar()
        input_position = Combobox(f2, values=["all levels"]+[str(i+1) for i in range(9)],textvariable=level)
        input_position.current(0)
        input_position.grid(row=4, column=1)
        wordOrMeaning=StringVar()
        input_position = Combobox(f2, values=["Choose word","Choose meaning"],textvariable=wordOrMeaning)
        input_position.current(0)
        input_position.grid(row=5, column=1)
        wordType=StringVar()
        input_position = Combobox(f2, values=sorted(["s","v","prep","conj","adv","adj","phrase/idiom","all"]),textvariable=wordType)
        input_position.current(2)
        input_position.grid(row=6, column=1)

        Label(f2, width=20,background=self.colour).grid(row=7)
        Button(f2, text='Proceed to play', command=lambda:self.checkIfPlay(f2, level.get(),wordOrMeaning.get(),wordType.get())).grid(row=10, column=1)

        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=14, column=1) 
        
        
    def Play(self,frame,level,wordOrMeaning,wordType):
        """ 
        Shows the question and the options
        
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
            level: level of the words that can be selected for the game. If all
                levels can be picked out, then level="all levels".
            wordOrMeaning: "Choose meaning" if the options to chose are the 
                meanings, or "Choose word" if the options to chose are the word
                names. 
            wordType: word type of the words that can be selected for the game.
                If all word types can be picked out, then wordType="all".
        """
        frame.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        if str(wordType)=="all":
            wType=random.choice(["s"]*19+["v"]*52+["prep"]*2+["conj"]*2+["adv"]*8+["adj"]*14+["phrase/idiom"]*3)
        else:
            wType=str(wordType)
            
        C=WordsDDBB(self.loggedUser)
        if str(level)=="all levels":
            listWords=C.showWordswordType(wType)
        else:
            listWords=C.showWordsByLevelwordType(int(level),wType)
        C.closeCon()
        n=len(listWords)
        
        
        option=[i for i in range(n)]
        options=[]
        for i in range(self.noptions):
            bool=True
            while bool:
                num=random.choice(option)
                if num not in options:
                    options.append(num)
                    bool=False
        
        testonIndex=random.choice(options)
        Label(f2,background=self.colour).grid(row=0,column=0)
        if str(wordOrMeaning)=="Choose word":
            Label(f2, text=str(listWords[testonIndex][2]),font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=0, columnspan=3)
        else:
            Label(f2, text=str(listWords[testonIndex][0]),font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=0, columnspan=3)
        Label(f2, text="Options",font = "Helvetica 11",background=self.colour).grid(row=2, column=1)
        var = IntVar()
        for i in range(self.noptions):
            if str(wordOrMeaning)=="Choose word":
                input_position=Radiobutton(f2, text=listWords[options[i]][0], variable=var, value=options[i])
            else:
                input_position=Radiobutton(f2, text=listWords[options[i]][2], variable=var, value=[options[i]])              
            input_position.grid(row=int(3+i), column=0, columnspan=3)
        Label(f2,background=self.colour).grid(row=11,column=0)
        Button(f2, text='Answer', command=lambda:self.answerPlay(f2,listWords[int(str(var.get()))],listWords[testonIndex],level,wordOrMeaning,wordType)).grid(row=14, column=0, columnspan=3) 
            
    def answerPlay(self,frame, answer, word,level,wordOrMeaning,wordType):
        """ 
        Shows if the player's answer is correct, update the level (+1 if 
            correct; -1 if wrong. Levels between 1 and 10), adn shows the 
            information about the correct answer (word name, meaning, example 
            -if there is-,new level).
        
        Args:
            frame: previous frame of the window to be deleted before creating 
                the new one. 
            answer: option picked out by the user
            word: correct answer
            level: level of the words that can be selected for the game. If all
                levels can be picked out, then level="all levels".
            wordOrMeaning: "Choose meaning" if the options to chose are the 
                meanings, or "Choose word" if the options to chose are the word
                names. 
            wordType: word type of the words that can be selected for the game.
                If all word types can be picked out, then wordType="all".
        """
        frame.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        Label(f2,background=self.colour).grid(row=0)
        if str(answer[2])==str(word[2]):
            Label(f2, text="Correct answer",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=0, columnspan=3)
            newLevel=int(word[4])+1
        else:
            Label(f2, text="Wrong answer",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=0, columnspan=3)
            newLevel=int(word[4])-1
        if newLevel not in [i+1 for i in range(9)]:
            newLevel=int(word[4])
        else:
            C=WordsDDBB(self.loggedUser)
            C.updateLevel(word[0], word[2], newLevel)
            C.closeCon()
        
        Label(f2,background=self.colour).grid(row=2)
        
        Label(f2, text="WORD: "+word[0],font = "Helvetica 12 bold",background=self.colour).grid(row=3, column=0, columnspan=3)
        Label(f2, text="MEANING: "+word[2],font = "Helvetica 11 bold",background=self.colour).grid(row=4, column=0, columnspan=3)
        if len(str(word[1]))>1:
            Label(f2, text="EXAMPLE(S): "+word[1],font = "Helvetica 10 bold",background=self.colour).grid(row=5, column=0, columnspan=3)
        Label(f2, text="NEW LEVEL: "+str(word[4])+"->"+str(newLevel),font = "Helvetica 12 bold",background=self.colour).grid(row=6, column=0, columnspan=3)
        Label(f2, width=20,background=self.colour).grid(row=7)
        
        
        Button(f2, text='Continue playing', command=lambda:self.Play(f2,level,wordOrMeaning,wordType)).grid(row=10, column=0, columnspan=3)
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=14, column=0, columnspan=3) 
        
    def showWords(self):
        """ 
        This method is executed when the user wants to obtain a pdf with the 
            words stored in his/her database. Shows a form to obtain the 
            details: order by "date","word","level" or "word type" and  
            "ascending" or "descending" order 
        """
        self.f1.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)

        Label(f2,background=self.colour).grid(row=0)
        Label(f2, text=" Create file ",font = "Helvetica 12 bold",background=self.colour).grid(row=1, column=1)
        Label(f2,background=self.colour).grid(row=2)
        
        Label(f2, text='Order by: ',background=self.colour).grid(row=3, column=1)
        orderBy=StringVar()
        input_position = Combobox(f2, values=sorted(["date","word","level","word type"]),textvariable=orderBy)
        input_position.current(0)
        input_position.grid(row=4, column=1)
        Label(f2,background=self.colour).grid(row=5)
        Label(f2, text='Type: ',background=self.colour).grid(row=7, column=1)
        orderType=StringVar()
        input_position = Combobox(f2, values=sorted(["ASC","DESC"]),textvariable=orderType)
        input_position.current(0)
        input_position.grid(row=8, column=1)
        Label(f2,background=self.colour).grid(row=9)
      
        Button(f2, text='Create file', command=lambda:self.createFile(f2, orderBy.get(), orderType.get())).grid(row=10, column=1)
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=14, column=1) 
        
    def createFile(self,frame,orderBy,orderType):
        """ 
        This method creates a pdf with the words stored in the database. The
            details have been obtained from the method showWords() and are
            passed as arguments.
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                    the new one.
            orderBy: indicates the column to choose the order ("date","word",
                "level" or "word type")
            orderType: select the order type (ascending ,"ASC", or descending,
                DESC")
        """
        have=["date","word","level","word type"]
        need=[5,0,4,3]
        order=need[have.index(str(orderBy))]
        C=WordsDDBB(self.loggedUser)
        words=C.showAll()
        C.closeCon()
        if str(orderType)=="ASC":
            ordt=False
        else:
            ordt=True
        words.sort(key=lambda x: x[order], reverse=ordt)
        filename =  filedialog.asksaveasfilename(initialdir = "/",defaultextension='.txt',title = "Save file as",filetypes = (("text plain files","*.txt"),("all files","*.*")))
        try:
            fobj = open(filename,"w")
            for i in words:
                fobj.write("{!s}\n".format('|'.join([i[0],i[2],i[1]])))
            fobj.close()
            self.GoToMenu(frame)
        except TypeError : pass
        except FileNotFoundError: pass
        
        
    def Configure(self):
        """ 
        Shows a frame with the different variables that can be modified. The 
            user can modify:
                -The background colour. 
                -If the user wants to activate the automatics mails (they are 
                    desactivated by default). The user can choose the content
                    of the email (statistics and/or word of the day).
                -If the user wants to desactivate the automatics mails.
                -The number of options of the game (4,5 or 6)
                -If the user wants to restart the game (update the levels to 1).
                -If the user wants to import data from an external database.
                -If the user wants to open the log file.
                -The password  
        """
        self.f1.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/4))
        f2.columnconfigure(1,minsize=math.floor((self.width)/4))
        f2.columnconfigure(2,minsize=math.floor((self.width)/4))
        f2.columnconfigure(3,minsize=math.floor((self.width)/4))
        
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        Label(f2, text="Configuration",font = "Helvetica 11 bold",background=self.colour).grid(row=1, column=1)      
        Label(f2, text="Administration",font = "Helvetica 11 bold",background=self.colour).grid(row=1, column=2)      
        Label(f2,background=self.colour).grid(row=2)
        Button(f2, text='Change background colour ', command=lambda:self.changeColour(f2)).grid(row=3, column=1)
        Label(f2,text="".ljust(30,"-"),background=self.colour).grid(row=4, column=1)
        includeWordOfMoment = IntVar()
        includeStatistics = IntVar()
        Checkbutton(f2, text="Iclude \"Word of the day\"", variable=includeWordOfMoment).grid(row=5, column=1)
        Checkbutton(f2, text="Iclude statistics", variable=includeStatistics).grid(row=6 , column=1)
        usermail=StringVar(value="mail")
        Entry(f2, textvariable=usermail).grid(row=7, column=1)
        Button(f2, text='Activate automatic mails', command=lambda:self.automails(f2,includeWordOfMoment.get(),includeStatistics.get(),usermail.get(),True)).grid(row=8, column=1)
        Button(f2, text='Cancel automatic mails', command=lambda:self.automails(f2,includeWordOfMoment.get(),includeStatistics.get(),usermail.get(),False)).grid(row=10, column=1)
        Label(f2,text="".ljust(30,"-"),background=self.colour).grid(row=9, column=1)
        Label(f2,text="".ljust(30,"-"),background=self.colour).grid(row=11, column=1)
        var=IntVar()
        input_position=Radiobutton(f2, text="4", variable=var, value=4)
        input_position.grid(row=int(12), column=1)
        input_position=Radiobutton(f2, text="5", variable=var, value=5)
        input_position.grid(row=int(13), column=1)
        input_position=Radiobutton(f2, text="6", variable=var, value=6)
        input_position.grid(row=int(14), column=1)
        Button(f2, text='Chose number of options', command=lambda:self.changeNoptions(f2,int(str(var.get())))).grid(row=15, column=1)
        
        Button(f2, text='Restart game', command=lambda:self.restartLevels(f2)).grid(row=3, column=2)
        Label(f2,text="".ljust(30,"-"),background=self.colour).grid(row=4, column=2)
        Button(f2, text='Import data from database', command=lambda:self.importData(f2)).grid(row=5, column=2)
        Label(f2,text="".ljust(30,"-"),background=self.colour).grid(row=6, column=2)
        Button(f2, text='Open log file', command=lambda:webbrowser.open("LOGS/log.log") and self.GoToMenu(f2)).grid(row=7, column=2)
        Label(f2,text="".ljust(30,"-"),background=self.colour).grid(row=8, column=2)
        Button(self.f1, text='Change password', width=20, command=lambda:self.ChangPass()).grid(row=9, column=1)
        
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=0, column=3,sticky=E) 
        
    def changeNoptions(self,frame,value):
        """ 
        This method allows to change the number of options of the game.
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                    the new one.
            value: new number of options of the game. It is 4 by default. This 
                value is stored in the properties file. 
        """
        file=open("PROPS/props.properties",'r')
        props={}
        for line in file:
            temp=line.replace("\n","").split("=")
            if len(temp)==2:
                props[str(temp[0])]=str(temp[1])
        file.close()
        props["noptions"]=str(value) 
        file=open("PROPS/props.properties",'w')
        for prop in props:
                file.write(str(prop)+"="+str(props[prop])+"\n")
        file.close()
        logging.info("new number of options")
        messagebox.showinfo("Done!", "Changes will be applied once the app has been restarted")
        self.GoToMenu(frame)
            
    def credits(self):
        """ 
        This method shows information about the application.
        """
        self.f1.grid_forget()
        f2 = Frame(self.window ,width=self.width, height=self.height, style='My.TFrame')
        f2.columnconfigure(0,minsize=math.floor((self.width)/3))
        f2.columnconfigure(1,minsize=math.floor((self.width)/3))
        f2.columnconfigure(2,minsize=math.floor((self.width)/3))
        
        f2.grid(row=0, column=0, sticky='news')
        self.raise_frame(f2)
        
        Label(f2, background=self.colour).grid(row=0, column=1)    
        Label(f2, background=self.colour).grid(row=2, column=1)    
        Label(f2, background=self.colour).grid(row=4, column=1) 
        Label(f2, background=self.colour).grid(row=11, column=1)  
        image = Image.open("IMG/app.ico")
        image.load()
        photo = ImageTk.PhotoImage(image)
        label=Label(f2, image=photo)
        label.image = photo # keeping the reference
        label.grid(row=1, column=1)
        Label(f2, text="By: JAVIER FDEZ. TRONCOSO",font = "Helvetica 13 bold",background=self.colour).grid(row=5, column=1)      
        Label(f2, text="Programming language: Python3",font = "Helvetica 11 bold ",background=self.colour).grid(row=6, column=1)      
        Label(f2, text="External libraries: tkinter,matplotlib.pyplot,time",font = "Helvetica 9",background=self.colour).grid(row=7, column=1)      
        Label(f2, text="os,sqlite3,shutil,random,math,webbrowser,",font = "Helvetica 9",background=self.colour).grid(row=8, column=1)      
        Label(f2, text="PIL,pronouncing,logging,smtplib,email",font = "Helvetica 9",background=self.colour).grid(row=9, column=1)      
        Button(f2, text='Go back to main menu', command=lambda:self.GoToMenu(f2)).grid(row=0, column=2) 
        
    def restartLevels(self,frame):
        """ 
        This method connects to the database and updates the levels to 1 
        """
        C=WordsDDBB(self.loggedUser)
        C.resetLevels()
        C.closeCon()
        self.GoToMenu(frame)
                
    def automails(self,frame,includeword,includestats,mail,bool):
        """ 
        This method allows to change the information about the mails. It 
            connects to the properties file and save the new configuration.
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                    the new one.
            includeword: boolean. If True, the email will include information 
                about one of the words in the user's database. This word is 
                randomly generated.
            includestats: boolean. If True, the email will include the  
                statistics about the game to the user. 
            mail: name of the recipient.
            bool: boolean. If True, the automatic mails are activated. False 
                otherwise
        """
        file=open("PROPS/props.properties",'r')
        props={}
        for line in file:
            temp=line.replace("\n","").split("=")
            if len(temp)==2:
                props[str(temp[0])]=str(temp[1])
        file.close()
        props["sendT"+str(self.loggedUser)]=str(mail)
        props["boolsendT"+str(self.loggedUser)]=bool
        props["boolincludeword"+str(self.loggedUser)]=True if str(includeword)==str(1) else False
        props["boolincludestats"+str(self.loggedUser)]=True if str(includestats)==str(1) else False
        file=open("PROPS/props.properties",'w')
        for prop in props:
            file.write(str(prop)+"="+str(props[prop])+"\n")
        file.close()
        if bool:
            messagebox.showinfo("Done!", "You will receive a mail every time you click on \"Exit\"")
        else:
            messagebox.showinfo("Done!", "Service has been desactivated")
        self.GoToMenu(frame)
        
        
    def importData(self,frame):
        """
        Chooses an external ddbb and imports its words. 

        Args:
            frame: previous frame of the window to be deleted before creating 
                    the new one.
        """
        yourdb="BBDD/"+str(self.loggedUser)+".db"
        now=time.localtime( time.time())
        mm=str(now.tm_mon) if len(str(now.tm_mon))==2 else "0"+str(now.tm_mon)
        dd=str(now.tm_mday) if len(str(now.tm_mday))==2 else "0"+str(now.tm_mday)
        day="{!s}{!s}{!s}".format(str(now.tm_year),mm,dd)
        if not os.path.exists("BBDD/bkp/"):
            os.makedirs("BBDD/bkp/")
        backupyourdb="BBDD/bkp/"+str(self.loggedUser)+day+".db"
        day="{!s}/{!s}/{!s}".format(str(now.tm_year),mm,dd)
        filename =  filedialog.askopenfilename(title = "Choose database file",filetypes = (("database files","*.db"),("all files","*.*")))
        if len(filename)>0:
            try:
                messagebox.showinfo("In progress!", "This operation can take several minutes. Please, wait")
                C=WordsDDBB(self.loggedUser)
                mw=C.showAll()
                mywords=[]
                for i in mw:
                    mywords.append(i[0])
                C.fileToImport(filename)
                words=C.showAll()
                C.closeCon()
                C=WordsDDBB(self.loggedUser)
                shutil.copyfile(yourdb, backupyourdb)
                for i in words:
                    if i[0] not in mywords:
                        print(i[0])
                        C.insWord(i[0],i[1],i[2],i[3],1,day)
                C.closeCon()
                messagebox.showinfo("Done!", "Operation have be completed successfully.")
                self.GoToMenu(frame)
            except:
                messagebox.showerror("Caution", "Operation cannot be completed.\n Check if the file is a valid database")
        
    def changeColour(self,frame):
        """ 
        This method allows to change the information about the background colour. 
            It connects to the properties file and save the new configuration.
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                    the new one.
        """
        file=open("PROPS/props.properties",'r')
        props={}
        for line in file:
            temp=line.replace("\n","").split("=")
            if len(temp)==2:
                props[str(temp[0])]=str(temp[1])
        file.close()
        newcolour=colorchooser.askcolor(color='#C8F9F9',title = "Select colour") 
        if str(newcolour[1])!="None":
            props["colour"]=str(newcolour[1].upper())
            file=open("PROPS/props.properties",'w')
            for prop in props:
                file.write(str(prop)+"="+str(props[prop])+"\n")
            file.close()
            self.GoToMenu(frame)
            logging.info("new background color")
            messagebox.showinfo("Done!", "Changes will be applied once the app is restarted")
        
    def updateSize(self,frame, widthNew, heightNew):
        """ 
        This method allows to change the information about the size of the 
            window. It connects to the properties file and save the new 
            configuration.
            
        Args:
            frame: previous frame of the window to be deleted before creating 
                    the new one.
            widthNew: new width
            heightNew: new height
        """
        if int(heightNew)<300:
            messagebox.showerror("Caution", "\"height\" value cannot be lower than 300 pixels.")
        else:
            file=open("PROPS/props.properties",'r')
            props={}
            for line in file:
                temp=line.replace("\n","").split("=")
                if len(temp)==2:
                    props[str(temp[0])]=str(temp[1])
            file.close()
            props["width"]=str(widthNew)
            props["height"]=str(heightNew)
            file=open("PROPS/props.properties",'w')
            for prop in props:
                file.write(str(prop)+"="+str(props[prop])+"\n")
            file.close()
            logging.info("new size")
            self.GoToMenu(frame)
