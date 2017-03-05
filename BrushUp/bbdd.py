# -*- coding: utf-8 -*-

import time
import os
import sqlite3
from __init__ import *

class UsersDDBB():
    def __init__(self):
        """Inizialize the connection to the ddbb in which the users are defined"""
        self.connection = sqlite3.connect('BBDD/users.db')
        self.cursor=self.connection.cursor()
    
    def closeCon(self):
        """Close the connection"""
        self.cursor.close()
        self.connection.close()
        
    def restart(self):
        """Restart the connection"""
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        self.connection = sqlite3.connect('users.db')
        self.cursor=self.connection.cursor()
        
    def createTables(self):
        """Create table if it doesnt exist"""
        self.cursor.execute('CREATE TABLE IF NOT EXISTS USERS (user varchar(255), password varchar(255), CONSTRAINT norepeat UNIQUE(user))')  
  
    def dropTables(self):
        """ Drop the table Users"""
        self.cursor.execute('DROP TABLE IF EXISTS USERS')  
            
    def insUs(self, user, password):
        """ Insert a new user """
        t=(user, password)
        try:
            self.cursor.execute('INSERT INTO USERS (user, password) VALUES (?,?)', t)
            self.connection.commit()
        except sqlite3.IntegrityError:
            logging.error("Row already exists. Please, try a new ID")
        except sqlite3.OperationalError as er:
            logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
            self.connection.rollback()

    def deleteUs(self, user):
        """ Delete an existing user """
        try:
            self.cursor.execute('DELETE FROM USERS WHERE user=?', [user])
            self.connection.commit()
            logging.info("Deleting user: {!s} ".format(str(user)))
        except sqlite3.OperationalError as er:
            logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
            self.connection.rollback()
            
    def showUsers(self):
        """ Return a list with all the user """
        self.cursor.execute('SELECT * FROM USERS')
        listUsers=[]
        for row in self.cursor:
            listUsers.append(row)
        return listUsers
    
    def changePass(self, user, newpass):
        """ Change the password assigned to a specific user """
        try:
                self.cursor.execute('UPDATE USERS SET password=? WHERE user=? ', [newpass, user])
                logging.info("new password for {!s}".format(str(user)))
                self.connection.commit()
        except sqlite3.OperationalError as er:
                logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
                self.connection.rollback()

class WordsDDBB():
    def __init__(self,username):
        """Inizialize the connection to the ddbb in which the words are defined"""
        self.file="BBDD/"+str(username)+".db"
        self.connection = sqlite3.connect(self.file)
        self.cursor=self.connection.cursor()
    
    def fileToImport(self,file):
        """Inizialize the connection to a ddbb whose words will be imported"""
        self.cursor.close()
        self.connection.close()
        self.connection = sqlite3.connect(file)
        self.cursor=self.connection.cursor()
        
    def closeCon(self):
        """Close the connection"""
        self.cursor.close()
        self.connection.close()
        
    def restart(self):
        """ Restart the connection """
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        self.connection = sqlite3.connect(self.file)
        self.cursor=self.connection.cursor()
        
    def createTables(self):
        """ Create the table """
        self.cursor.execute('CREATE TABLE IF NOT EXISTS WORDS (word varchar(255), example varchar(255), meaning varchar(255), syntaxis varchar(255),category int, day varchar(255))')  
  
    def dropTables(self):
        """ Drop the table """
        self.cursor.execute('DROP TABLE IF EXISTS WORDS')  
            
    def insWord(self, word, example, meaning, syntaxis,category,when):
        """ Add a new word """
        t=(word, example, meaning, syntaxis,category,when)
        try:
            self.cursor.execute('INSERT INTO WORDS (word, example, meaning, syntaxis,category,day) VALUES (?,?,?,?,?,?)', t)
            self.connection.commit()
            logging.info("Inserting new word: {!s} ".format(str(word)))
        except sqlite3.OperationalError as er:
            logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
            self.connection.rollback()

    def deleteWord(self, word):
        """ Delete a specific word """
        try:
            self.cursor.execute('DELETE FROM WORDS WHERE word=?', [word])
            self.connection.commit()
            logging.info("Deleting word: {!s} ".format(str(word)))
        except sqlite3.OperationalError as er:
            logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
            self.connection.rollback()
            
    def updateLevel(self, word, meaning, newLevel):
        """ Change the level assigned to a specific word """
            try:
                self.cursor.execute('UPDATE WORDS SET category=? WHERE word=? AND meaning=?', [newLevel, word, meaning])
                self.connection.commit()
            except sqlite3.OperationalError as er:
                logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
                self.connection.rollback()
                
    def resetLevels(self):
            """ Reset level to 1 """
            try:
                self.cursor.execute('UPDATE WORDS SET category=?', [1])
                logging.info( "levels have been reseted")
                self.connection.commit()
            except sqlite3.OperationalError as er:
                logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
                self.connection.rollback()
                
    def showWords(self):
        """ Return a list with all the words """
        self.cursor.execute('SELECT * FROM WORDS ORDER BY word')
        listWords=[]
        for row in self.cursor:
            listWords.append(list(row))
        return listWords
    
    def showWordsByLevel(self,level):
        """ Return a list with the words associated with a specific level """
        self.cursor.execute('SELECT * FROM WORDS WHERE category=?', [level])
        listWords=[]
        for row in self.cursor:
            listWords.append(list(row))
        return listWords
    
    def showWordswordType(self,wordType):
        """ Return a list with the words associated with a specific word type """
        self.cursor.execute('SELECT * FROM WORDS WHERE syntaxis=?', [wordType])
        listWords=[]
        for row in self.cursor:
            listWords.append(list(row))
        return listWords
    
    def showWordsByLevelwordType(self,level,wordType):
        """ Return a list with the words associated with a specific level and word type """
        self.cursor.execute('SELECT * FROM WORDS WHERE category=? AND syntaxis=?', [level,wordType])
        listWords=[]
        for row in self.cursor:
            listWords.append(list(row))
        return listWords
    
    def showWord(self,word):
        """ Return a list with the inputs associated with a specific word """
        self.cursor.execute('SELECT * FROM WORDS WHERE word=?', [word])
        listWords=[]
        for row in self.cursor:
            listWords.append(row)
        return listWords
    
    def showAll(self):
        """ Return a list with all the words """
        self.cursor.execute('SELECT * FROM WORDS')
        listWords=[]
        for row in self.cursor:
            listWords.append(list(row))
        return listWords
    
    def showWordsAllLevels(self):
        """ Return the number of number of words inside each level """
        stats={}
        totalWords=0
        for i in list(range(1,11)):
            self.cursor.execute('SELECT * FROM WORDS WHERE category=?', [i])
            num=0
            for row in self.cursor:
                num+=1
            stats[str(i)]=str(num)
        for i in stats:
            totalWords+=int(stats[i])
        return stats,totalWords
    
    def showWordsAllTypes(self):
        """ Return the number of number of words inside each word type """
        stats={}
        totalWords=0
        for i in ["s","v","prep","conj","adv","adj","phrase/idiom"]:
            self.cursor.execute('SELECT * FROM WORDS WHERE syntaxis=?', [i])
            num=0
            for row in self.cursor:
                num+=1
            stats[str(i)]=str(num)
        for i in stats:
            totalWords+=int(stats[i])
        return stats,totalWords
   
            
if __name__=="__main__":
    C=UsersDDBB()
    C.dropTables()
    C.createTables()
    C.insUs("javi","pass")
    print(C.showUsers())
    C.closeCon()
    C=WordsDDBB("javi")
    C.dropTables()
    C.createTables()
    now=time.localtime( time.time())
    mm=str(now.tm_mon) if len(str(now.tm_mon))==2 else "0"+str(now.tm_mon)
    dd=str(now.tm_mday) if len(str(now.tm_mday))==2 else "0"+str(now.tm_mday)
    day="{!s}/{!s}/{!s}".format(str(now.tm_year),mm,dd)
    C.insWord("brush up","My spoken French is quite good, but I would like to brush up a bit","repasar, hacer un repaso","v",1,day)
    C.closeCon()
    
    '''
    C=WordsDDBB("javi")
    C.cursor.execute('UPDATE WORDS SET day=?', ["2017/02/05"])
    C.connection.commit()
    C.closeCon()
    '''
