# -*- coding: utf-8 -*-

import time
import os
import sqlite3
from __init__ import *

class UsersDDBB():
    """ 
    Class to deal with users who can access to the application.
    Here, we can create/delete the database, inizialize/close the connections,
        add/delete users and change passwords. All users who are included in this
        database can access to the application. 
    The database which is created is called users.db, and can be found inside BBDD.
    The name of the table is "USERS".
    """
    
    def __init__(self):
        """
        Inizializes the connection to the ddbb in which the users are defined
        The self is defined
        """
        self.connection = sqlite3.connect('BBDD/users.db')
        self.cursor=self.connection.cursor()
    
    def closeCon(self):
        """
        Closes the connection
        """
        self.cursor.close()
        self.connection.close()
        
    def restart(self):
        """
        Restarts the connection to the database
        """
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        self.connection = sqlite3.connect('users.db')
        self.cursor=self.connection.cursor()
        
    def createTables(self):
        """
        Creates table if it doesnt exist.
        This option is never used for the application, but it is appropriate 
            to have a method which allows us to create the table if it has been 
            removed.
        """
        self.cursor.execute('CREATE TABLE IF NOT EXISTS USERS (user varchar(255), password varchar(255), CONSTRAINT norepeat UNIQUE(user))')  
  
    def dropTables(self):
        """ 
        This method removes the table "USERS". It is not convenient to use this
            method. 
        """
        self.cursor.execute('DROP TABLE IF EXISTS USERS')  
            
    def insUs(self, user, password):
        """ 
        This method inserts a new user inside the table.
        This method will be called once a user tries to sign up.
        
        Args:
            user: this will be the username
            password: this will be the password which will allow
                the user to get logged in. 
                
        """
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
        """ 
        This method allows to delete an existing user. However, the application
            does not allow to do this, so this accion must be done at the 
            command line. 
            
        Args:
            user: this will be the user to be deleted from the table
            
        """
        try:
            self.cursor.execute('DELETE FROM USERS WHERE user=?', [user])
            self.connection.commit()
            logging.info("Deleting user: {!s} ".format(str(user)))
        except sqlite3.OperationalError as er:
            logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
            self.connection.rollback()
            
    def showUsers(self):
        """ 
        This method shows all the users included inside the table.
        
        Returns:
            listUsers: List in which all the users are included. Every user is 
                added as a list: [username,password]
        """
        self.cursor.execute('SELECT * FROM USERS')
        listUsers=[]
        for row in self.cursor:
            listUsers.append(row)
        return listUsers
    
    def changePass(self, user, newpass):
        """ 
        Changes the password assigned to a specific user 
        
        Args:
            user: this is the username related to the user who wants to change 
                his/her password.
            newpassword: new password
        """
        try:
                self.cursor.execute('UPDATE USERS SET password=? WHERE user=? ', [newpass, user])
                logging.info("new password for {!s}".format(str(user)))
                self.connection.commit()
        except sqlite3.OperationalError as er:
                logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
                self.connection.rollback()

class WordsDDBB():
    """ 
    Class to deal with the words that every user include in their databases. 
    Here, we can insert/delete the database, inizialize/close the connections,
        add/delete words and change passwords. 
    The database which is created is the name of the user, and each user has 
        his/her own database. 
    The name of the table is "WORDS".
    """
    
    def __init__(self,username):
        """
        Inizializes the connection to a specific ddbb .
        The self is defined.
        The name of the database is defined here, and it is defined as a class 
            variable. The connection is kept opened to allow the user to 
            execute another actions inside this database. It is necessary to 
            close the connection through the method closeCon(). 
            
        Args:
            username: name of the database
        """
        self.file="BBDD/"+str(username)+".db"
        self.connection = sqlite3.connect(self.file)
        self.cursor=self.connection.cursor()
    
    def fileToImport(self,file):
        """
        Inizializes the connection to an external ddbb and open the connection. 
            It is important to know that the actions to be performed later will 
            be done inside this database if it is not closed through the method 
            closeCon(). 

        Args:
            file: database file
        """
        self.cursor.close()
        self.connection.close()
        self.connection = sqlite3.connect(file)
        self.cursor=self.connection.cursor()
        
    def closeCon(self):
        """
        Closes the connection
        """
        self.cursor.close()
        self.connection.close()
        
    def restart(self):
        """ 
        Restarts the connection 
        """
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        self.connection = sqlite3.connect(self.file)
        self.cursor=self.connection.cursor()
        
    def createTables(self):
        """
        Creates the table if it doesnt exist.
        This table is created when the database is created (after the signup)
        """
        self.cursor.execute('CREATE TABLE IF NOT EXISTS WORDS (word varchar(255), example varchar(255), meaning varchar(255), syntaxis varchar(255),category int, day varchar(255))')  
  
    def dropTables(self):
        """ 
        This method removes the table "USERS". It is not convenient to use this
            method. 
        """
        self.cursor.execute('DROP TABLE IF EXISTS WORDS')  
            
    def insWord(self, word, example, meaning, syntaxis,category,when):
        """ 
        This method inserts a new word inside the table.
        
        Args:
            word: new word to be included
            example: example in which the word is used
            meaning: meaning of the word in the user's native language
            syntaxis: type of word (verb, preposition...)
            category: level. By default, all words are iniziated with the first 
                level.
            when: day in which the word is created.
                
        """
        t=(word, example, meaning, syntaxis,category,when)
        try:
            self.cursor.execute('INSERT INTO WORDS (word, example, meaning, syntaxis,category,day) VALUES (?,?,?,?,?,?)', t)
            self.connection.commit()
            logging.info("Inserting new word: {!s} ".format(str(word)))
        except sqlite3.OperationalError as er:
            logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
            self.connection.rollback()

    def deleteWord(self, word):
        """ 
        This method allows to delete an existing word. 
        
        Args:
            word: word that the user ask to delete
            
        """
        try:
            self.cursor.execute('DELETE FROM WORDS WHERE word=?', [word])
            self.connection.commit()
            logging.info("Deleting word: {!s} ".format(str(word)))
        except sqlite3.OperationalError as er:
            logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
            self.connection.rollback()
            
    def updateLevel(self, word, meaning, newLevel):
            """ 
            Changes the level assigned to a specific word

            Args:
                word: word whose level will be updated.
                meaning: meaning of word whose level will be updated.
                newLevel: new level
            """
            try:
                self.cursor.execute('UPDATE WORDS SET category=? WHERE word=? AND meaning=?', [newLevel, word, meaning])
                self.connection.commit()
            except sqlite3.OperationalError as er:
                logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
                self.connection.rollback()
                
    def resetLevels(self):
            """ 
            Updates the level associated with all the words to 1 
            """
            try:
                self.cursor.execute('UPDATE WORDS SET category=?', [1])
                logging.info( "levels have been reseted")
                self.connection.commit()
            except sqlite3.OperationalError as er:
                logging.error( "{!s}.  Please, try it again in a few minutes".format(str(er)))
                self.connection.rollback()
                
    def showWords(self):
        """ 
        This method shows all the words  included inside the table.
        
        Returns:
            listWords: List in which all the word are included. They are ordered 
                depending on its word name. Every word is added as a list: 
                [word, example, meaning, word type,level,creation day]
        """
        self.cursor.execute('SELECT * FROM WORDS ORDER BY word')
        listWords=[]
        for row in self.cursor:
            listWords.append(list(row))
        return listWords
    
    def showWordsByLevel(self,level):
        """ 
        This method shows all the words associated with a specific level.
        
        Args:
            level: This method will show the words with this level.
            
        Returns:
            listWords: List in which all the words meeting the requirement are 
                included. Every word is added as a list: 
                [word, example, meaning, word type,level,creation day]
        """
        self.cursor.execute('SELECT * FROM WORDS WHERE category=?', [level])
        listWords=[]
        for row in self.cursor:
            listWords.append(list(row))
        return listWords
    
    def showWordswordType(self,wordType):
        """ 
        This method shows all the words associated with a specific word type.
        
        Args:
            wordType: This method will show the words with this word type.
            
        Returns:
            listWords: List in which all the words meeting the requirement are 
                included. Every word is added as a list: 
                [word, example, meaning, word type,level,creation day]
        """
        self.cursor.execute('SELECT * FROM WORDS WHERE syntaxis=?', [wordType])
        listWords=[]
        for row in self.cursor:
            listWords.append(list(row))
        return listWords
    
    def showWordsByLevelwordType(self,level,wordType):
        """ 
        This method shows all the words associated with a specific level and 
            word type.
        
        Args:
            wordType: This method will show the words with this word type.
            level: This method will show the words with this level.
            
        Returns:
            listWords: List in which all the words meeting the requirement are 
                included. Every word is added as a list:  
                [word, example, meaning, word type,level,creation day]
        """
        self.cursor.execute('SELECT * FROM WORDS WHERE category=? AND syntaxis=?', [level,wordType])
        listWords=[]
        for row in self.cursor:
            listWords.append(list(row))
        return listWords
    
    def showWord(self,word):
        """ 
        This method shows all the words associated with a specific word name.
        
        Args:
            word: This method will show the words with this name.
            
        Returns:
            listWords: List in which all the words meeting the requirement are 
                included. Every word is added as a list: 
                [word, example, meaning, word type,level,creation day]
        
        Note: We have to take into account that the same word can have different
            inputs associated with different meanings or word types.
        """
        self.cursor.execute('SELECT * FROM WORDS WHERE word=?', [word])
        listWords=[]
        for row in self.cursor:
            listWords.append(row)
        return listWords
    
    def showAll(self):
        """ 
        This method shows all the words included in a specific database.
        
        Returns:
            listWords: List in which all the words are included. Every word is 
                added as a list: 
                [word, example, meaning, word type,level,creation day]
        
        Note: We have to take into account that the same word can have different
            inputs associated with different meanings or word types.
        """
        self.cursor.execute('SELECT * FROM WORDS')
        listWords=[]
        for row in self.cursor:
            listWords.append(list(row))
        return listWords
    
    def showWordsAllLevels(self):
        """ 
        This method allows to show how many words there are for each level
        
        Returns:
            stats: dictionary in which we show the level and the number of words
                included inside that level.
            totalWords: total number of words, regardless the level. 
        """
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
        """ 
        This method allows to show how many words there are for each word type
        
        Returns:
            stats: dictionary in which we show the word type and the number of 
            words included inside that type.
            totalWords: total number of words, regardless the word type. 
        """
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
    C.insUs("admin","pass")
    print(C.showUsers())
    C.closeCon()
    C=WordsDDBB("admin")
    C.dropTables()
    C.createTables()
    now=time.localtime( time.time())
    mm=str(now.tm_mon) if len(str(now.tm_mon))==2 else "0"+str(now.tm_mon)
    dd=str(now.tm_mday) if len(str(now.tm_mday))==2 else "0"+str(now.tm_mday)
    day="{!s}/{!s}/{!s}".format(str(now.tm_year),mm,dd)
    C.insWord("brush up","My spoken French is quite good, but I would like to brush up a bit","repasar, hacer un repaso","v",1,day)
    C.closeCon()