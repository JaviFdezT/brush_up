# Brush Up!

#Introduction
This app allows you to brush up your language skills and manage those words that you are studying in a database. Moreover, you can find an annex about pronunciation.

#How to use
0. Install requiriments:

   a) Install Python3

   b) Install external libraries(tkinter,sqlite3; matplotlib, time, os, shutil, random, math, webbrowser, PIL, pronouncing, logging, smtplib, email).
   
      In linux (command line):

      sudo apt-get install python3-tk

      sudo apt-get install libsqlite3-dev

      sudo pip3 matplotlib

      sudo pip3 Pillow

      sudo pip3 pronouncing


1. Start the application by executing the script inside "brush_up/BrushUp/brushup.py". It can be done from the command line: "python3 brushup.py".

2. Create your account and then log in. You can also log into the admin's account by using username "admin" and pasword "pass".

3. Onced logged into your personal account, the main page will pop up. You dictionary will contain only one word (brush up), so you can import a list of words from the admin's database (brush_up/BrushUp/BBDD/admin.db) by clicking on  "Administration"->"Import data from database".
