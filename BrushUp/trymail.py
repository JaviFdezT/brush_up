
import time
import smtplib
import base64 as b
import random
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from  bbdd import UsersDDBB,WordsDDBB
from __init__ import *
 

class Email():
    def __init__(self,user):
        self.user=user
        self.fromaddr = 'brushupjft@gmail.com'
        self.smtpstring='smtp.gmail.com:587'

        file=open("PROPS/props.properties",'r')
        for line in file:
            temp=line.replace("\n","").split("=")
            if temp[0]=="sendT"+str(user):
                self.toaddrs=temp[1]
            elif temp[0]=="height":
                self.height=int(temp[1])
            elif temp[0]=="width":
                self.width=int(temp[1])
        file.close()

    def sendmail(self,subject, text):
        # Enviando el correo
        server = smtplib.SMTP(self.smtpstring)
        server.starttls()
        server.login('brushupjft@gmail.com',str(b.b64decode (self.p)).replace("b'","").replace("'",""))
        msg = 'Subject: {}\n\n{}'.format(subject, text)
        server.sendmail(self.fromaddr, self.toaddrs, msg)
        server.quit()

        print("sent")
      
    def sendpic(self,bool,bool2):
        
        file=open("LOGS/log.log",'r')
        mailssent=[]
        for line in file:
            if self.toaddrs in str(line):
                mailssent.append(line.replace("\n","").split()[0])
        file.close()
        
        checkifsend=True
        if len(mailssent)>0:
            curday=time.strftime("%Y%m%d")
            tmpstring=str(mailssent[-1])[6:]+str(mailssent[-1])[3:5]+str(mailssent[-1])[0:2]
            try:
                if int(curday)==int(tmpstring):
                    checkifsend=False
            except ValueError:pass
            
        if checkifsend:
            msg = MIMEMultipart()
            msg['Subject'] = "BrushUp! - The word of the day"
            msg['From'] = self.fromaddr
            msg['To'] = self.toaddrs

            if bool:
                C=WordsDDBB(self.user)
                words=C.showAll()
                C.closeCon()
                word=random.choice(words)

                font1 = ImageFont.truetype("arial.ttf", 42)
                font2 = ImageFont.truetype("arial.ttf", 22)
                font3 = ImageFont.truetype("arial.ttf", 12)
                img=Image.new("RGBA", (750,300),"#C8F9F9")
                draw = ImageDraw.Draw(img)
                draw.text((25, 20),word[0],"#000000",font=font1)
                if len(str(word[1]))>1:
                    draw.text((25, 100),"Example: "+str(word[1]),"#000000",font=font3)
                draw.text((25, 150),"Meaning: "+str(word[2]),"#000000",font=font2)
                draw.ellipse((670, 270, 690, 290), fill="#FF4500")
                draw.text((680, 275),"JaviFdezT","#000000",font=font3)
                draw.text((575, 270),"BrushUp!!","#000000",font=font2)
                draw = ImageDraw.Draw(img)

                img.save("temp.png")
                img_data = open("temp.png", 'rb').read()

            text = MIMEText("test")
            msg.attach(text)
            if bool=="True":
                image = MIMEImage(img_data, name=os.path.basename("temp.png"))
                msg.attach(image)
            if bool2=="True":
                img_data = open("plot.png", 'rb').read()
                image = MIMEImage(img_data, name=os.path.basename("plot.png"))
                msg.attach(image)

            try:
                s = smtplib.SMTP(self.smtpstring)
            except:
                s = smtplib.SMTP("smtp.gmail.com:587")
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login('brushupjft@gmail.com',str(b.b64decode ("YnJ1c2h1cDE=")).replace("b'","").replace("'",""))
            s.sendmail(self.fromaddr, self.toaddrs, msg.as_string())
            s.quit()
            logging.info("New mail sent to"+self.toaddrs)
            if bool=="True":
                os.remove("temp.png")
            if bool2=="True":
                os.remove("plot.png")

      
if __name__=="__main__":
    E=Email("javi")
    E.sendpic(False,False)
    


    
