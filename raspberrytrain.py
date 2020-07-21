import cv2, os      #cv2 (opencv) untuk proses dataset
import numpy as np
from PIL import Image, ImageTk
import pandas as pd #untuk dataframe
import datetime     #untuk waktu
from datetime import date
import time
import glob
import os.path
import shutil
import operator

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sent=False
emailtreshold=300
detected = False
standbyawal = True

def getgambardanlabel(path):
    #ambil path dari file di folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #buat list kosong untuk muka
    mukamuka=[]
    #buat list kosong untuk npm
    nomormhs=[]
    #buat looping untuk path gambar dan load npm sama gambar
    for imagePath in imagePaths:
        #konversi gambar ke grayscale
        pilImage=Image.open(imagePath).convert('L')
        #konversi gambar PIL ke numpy array
        imageNp=np.array(pilImage,'uint8')
        #ambil NPM dari gambar
        NPM=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract muka dari sample training
        mukamuka.append(imageNp)
        nomormhs.append(NPM)        
    return mukamuka,nomormhs


def sendemail():
    
    daftar_file = glob.glob('Takdikenal/'+'/*.jpg')
    file_terbaru = max(daftar_file, key=os.path.getctime)

    subject = "Seseorang tidak dikenal berada didepan pintu"
    body = "This is an email with attachment sent from Python"
    sender_email = "sistemkamera1998@gmail.com"
    receiver_email = "christiandaomara@gmail.com"
    password = 'vaticancameos'

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = file_terbaru  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')    
    cam = cv2.VideoCapture(1)
    font = cv2.FONT_HERSHEY_SIMPLEX  

    #recognizer = face.createLBPHFaceRecognizer()
    #$cv2.createLBPHFaceRecognizer()
    # mukamuka,nomormhs = getgambardanlabel('pretrained/')
    # recognizer.train(mukamuka, np.array(nomormhs))
    recognizer.read('trained/Trainer.yml')
          
    data_timestamp=pd.DataFrame(columns=['TIME'])
    time.sleep(2.0)
    starttime=time.time()
    while True:
        runtime=time.time()
        ret, im =cam.read()  
        #im=cv2.flip(im,1) 
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        mukamuka=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in mukamuka:
            
            nomormhs, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 40):
                tt = ''
                detected = True
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

            else:
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                nomormhs=''                
                tt=str(nomormhs) 
                try:
                    nomorFile=len(os.listdir("Takdikenal"))
                except FileNotFoundError:
                    os.mkdir('Takdikenal')
                    nomorFile=len(os.listdir("Takdikenal"))
                tst = time.time()    
                tst=int(tst)
                data_timestamp.loc[len(data_timestamp)] = [tst]
                #cv2.imwrite("Takdikenal/Gambar"+str(nomorFile) + ".jpg", im[y:y+h,x:x+w]) 
                      
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)

        totaltime=int(runtime)-int(starttime)
        print (totaltime)
            # print (len(data_timestamp))

        if len(data_timestamp)>0 and detected == False:
            data_timestamp.drop_duplicates(subset=['TIME'],keep='first')
            data_timestamp_awal=data_timestamp.head(1)
            #data_timestamp_akhir=data_timestamp.tail(1)
            data_timestamp_awal=data_timestamp.values.tolist()
            data_timestamp_akhir=data_timestamp.values.tolist()
            data_timestamp_awal=data_timestamp_awal[0]
            data_timestamp_akhir=data_timestamp_akhir[-1]
            data_timestamp_awal=str(data_timestamp_awal)
            data_timestamp_akhir=str(data_timestamp_akhir)
            data_timestamp_awal=(data_timestamp_awal.lstrip("['").rstrip("']"))
            data_timestamp_akhir=(data_timestamp_akhir.lstrip("['").rstrip("']"))

            #print (data_timestamp)
            #print (int(data_timestamp_awal),'dan',int(data_timestamp_akhir))

            if totaltime>=emailtreshold:
                sent=False
                emailtreshold=emailtreshold+300
                standbyawal = False
            
            treshold=10
            if int(data_timestamp_akhir)>=(int(data_timestamp_awal)+treshold):
                #cv2.imwrite("Takdikenal/Gambar"+str(nomorFile) + "a.jpg", im[y:y+h,x:x+w]) 
                cv2.imwrite("Takdikenal/Gambar"+str(nomorFile) + ".jpg",im) 
                if sent==False and standbyawal==False:
                    sendemail()
                    print('email')
                    sent=True
                        #emailtreshold=emailtreshold+60
                
                #if totaltime %60>=0 and totaltime>=60:
                    # print('sukses')
                data_timestamp=data_timestamp[0:0]
            
            


        width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
        height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT) # float

        teksx = int(width / 2) - int(width/4)
        teksy = int((95/100)* height)

        
                
        cv2.putText(im,'Tekan Q untuk keluar',(teksx,teksy), font, 1,(255,255,255),2,cv2.LINE_AA)          
        #im = cv2.resize(im, (1280,720))
        cv2.imshow('Kenali Wajah',im) 
        if (cv2.waitKey(1)==ord('q')):
            break 
    
except cv2.error as e:
        print(e)
  


