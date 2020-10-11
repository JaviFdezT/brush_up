

import time
import sqlite3
from tkinter.filedialog import askopenfilename
from tkinter import Tk


Tk().withdraw()

filename = askopenfilename(initialdir="./BBDD")
connection = sqlite3.connect(filename)
cursor=connection.cursor()

file = open("DOCS/words.txt",'r')

words,discardedwords=[],[]
now=time.localtime(time.time())
mm=str(now.tm_mon) if len(str(now.tm_mon))==2 else "0"+str(now.tm_mon)
dd=str(now.tm_mday) if len(str(now.tm_mday))==2 else "0"+str(now.tm_mday)
day="{!s}/{!s}/{!s}".format(str(now.tm_year),mm,dd)

for line in file:
    line=line.split("*")
    for i in range(len(line)):
        line[i]=line[i].strip().replace("\t","").replace("\n","")
    if len(line)==3:
        words.append([line[0],line[1],line[2]])
    else:
        discardedwords.append(line)

for word in words:
    syn=input("sysntaxis for \'"+str(word[0])+"\' as \'"+str(word[2])+"\':")
    t=(str(word[0]), str(word[1]), str(word[2]), str(syn),1,day)
    cursor.execute('INSERT INTO WORDS (word, example, meaning, syntaxis,category,day) VALUES (?,?,?,?,?,?)', t)
    connection.commit()  
    print("New word "+str(word[0]))     
    if len(word[1])>100:
        print("although its example is too large")


print("Added words:"+str(len(words))+". Discarded lines:"+str(len(discardedwords)))