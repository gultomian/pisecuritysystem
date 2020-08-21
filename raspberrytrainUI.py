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
import csv

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from tkinter import * #tkinter untuk GUI
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from PIL import Image, ImageTk
#Splashscreen

splashscreen = Tk()
splashscreen.configure(background='#f1f0f0')
#splashscreen.resizable(0,0)
splashscreen.iconbitmap("Logo_Aplikasi.ico")
splashscreen.title("Sistem Keamanan Rumah")
splashscreen.configure(background='#f1f0f0')


width = 447
height = 327
screen_width = splashscreen.winfo_screenwidth()
screen_height = splashscreen.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
splashscreen.geometry("%dx%d+%d+%d" % (width, height, x, y))
splashscreen.overrideredirect(1)
splashscreen.resizable(0, 0)

logo = Image.open("Splashscreen_Aplikasi.png")
logo = logo.resize((447,327))
renderlogo = ImageTk.PhotoImage(logo)

# label dijadiin variabel logo
img = Label(splashscreen, image=renderlogo)
img.image = renderlogo
img.pack()

def mainroot():
    window = Tk()
    window.configure(background='#f1f0f0')
    #window.resizable(0,0)
    window.iconbitmap("Logo_Aplikasi.ico")
    window.title("Sistem Keamanan Rumah")

    width = 450
    height = 350
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    window.resizable(0, 0)
    #window.overrideredirect(1)

    logo = Image.open("banner.jpg")
    renderlogo = ImageTk.PhotoImage(logo)

    # label dijadiin variabel logo
    img = Label(window, image=renderlogo)
    img.image = renderlogo
    img.place(x= 30, y=30)


    menu = Menu(window)
    window.config(menu=menu)
    dropdown_file = Menu(menu, tearoff=0)
    menu.add_cascade(label='File', menu=dropdown_file)


    sent=False
    emailtreshold=300
    detected = False
    #standbyawal = False #stand by awal agar nggak bakal ngirim email selama 5 menit pertama

    global pathload
    pathload = StringVar()
    def loadingpath(): 
        folder_pilihan = fd.askdirectory(title='Pilih Folder')
        pathload.set(folder_pilihan)
        startrecog()

    def timestamp(time):
        result = datetime.datetime.fromtimestamp(time).strftime('%H:%M:%S')
        return result
        
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
        with open("FOLDERSISTEMKEAMANAN/DescUser.csv") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for nama, label, email in reader:
                print(f"Sending email to {nama}")
                daftar_file = glob.glob('FOLDERSISTEMKEAMANAN/Takdikenal/'+'/*.jpg')
                file_terbaru = max(daftar_file, key=os.path.getctime)

                subject = "Seseorang tidak dikenal berada didepan pintu"
                body = "Email ini otomatis dikirim dari aplikasi sistem keamanan"
                sender_email = "sistemkamera1998@gmail.com"
                receiver_email = email
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

                # Open file in binary mode
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
                try:
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, text)
                except smtplib.socket.gaierror:
                    mb.showinfo("No Connection", "Program tidak terkoneksi ke Internet")
                    
    
    global portnum
    portnum = IntVar()
    def set_port():
        setportwin = Toplevel(window)
        setportwin.iconbitmap("Logo_Aplikasi.ico")
        setportwin.title("Port USB")
        width = 200
        height = 60
        screen_width = setportwin.winfo_screenwidth()
        screen_height = setportwin.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        setportwin.geometry("%dx%d+%d+%d" % (width, height, x, y))
        setportwin.resizable(0, 0)

        lbl_port= Label(setportwin,text='Set Index Port USB:')
        lbl_port.pack(side=TOP,anchor=CENTER,pady=1)
        frame1 = Frame(setportwin)
        frame1.pack(side=TOP,anchor=CENTER)
        entry_nmr = Entry(frame1, width=10)
        entry_nmr.pack(side=LEFT)

        def btn_nmr_get():
            if any(x.isdigit() for x in (entry_nmr.get())):
                if not entry_nmr.get():
                    portnum.set(0)
                else:
                    portnum.set(entry_nmr.get())
                    mb.showinfo('Info','Input Nomor Port Berhasil Dimasukkan')
                    setportwin.focus_set()
            else:
                mb.showerror('Error Input','Input Harus menggunakan angka')
                setportwin.focus_set()

        def helpport():
            mb.showinfo('Help',"Jika anda memiliki kamera eksternal selain kamera bawaan, anda bisa mengetik angka '1' di dalam kotak input")
            setportwin.lift()

        btn_nmr = Button(frame1, text = 'Set',width=5, command=btn_nmr_get)
        btn_nmr.pack(side=LEFT,padx=3)
        btn_nmr = Button(frame1, text = 'Help',width=5,command=helpport)
        btn_nmr.pack(side=LEFT,padx=3)

    dropdown_file.add_command(label='Port Kamera...',command = set_port)

    def startrecog():
        loadpath=pathload.get()
        numport=portnum.get()
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')    
            cam = cv2.VideoCapture(numport)
            font = cv2.FONT_HERSHEY_DUPLEX
            recognizer.read(loadpath+'/trained/Trainer.yml')
            df=pd.read_csv(loadpath+'/DescUser.csv')
            df.reset_index(drop=True)


            facedetected = False
            unrecognized=False
            emailsent=False
            tresholddetect=10
            tresholdemail=300
            listcoordinates =[]

            while True:
                runtime=time.time()
                ret, im =cam.read()  
                gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                prevlen=len(listcoordinates)
                mukamuka=faceCascade.detectMultiScale(gray, 1.2,5)
                
                for(x,y,w,h) in mukamuka:
                    facedetected = True
                    listcoordinates.append([x,y,w,h])
                    newlen=len(listcoordinates)
                    nomormhs, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                    if(conf < 40):   
                        unrecognized=False
                        cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                        aa=df.loc[df['Label'] == nomormhs]['Nama'].values
                        aa=(str(aa).lstrip("['").rstrip("']"))#hapus bracket dan tanda petik
                        cv2.putText(im,str(aa),(x,y+h), font, 1,(255,255,255),2)
                    else:
                        unrecognized = True
                        cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                        try:
                            nomorFile=len(os.listdir("FOLDERSISTEMKEAMANAN/Takdikenal"))
                            #cv2.putText(im,str(int(timestamp(timerB)[6:8])+tresholddetect-int(timestamp(timerA)[6:8])),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
                        except FileNotFoundError:
                            os.mkdir('FOLDERSISTEMKEAMANAN/Takdikenal')
                            nomorFile=len(os.listdir("FOLDERSISTEMKEAMANAN/Takdikenal"))
                    # except NameError:
                        #   pass

                    if int(timestamp(runtime)[6:8]) >= tresholdemail:
                        emailsent=False
                try:
                    if prevlen==newlen:
                        facedetected=False

                    if facedetected == True:
                        if unrecognized == True:
                            timerA=time.time()
                        else:
                            timerB=time.time()
                    else:
                        timerB=time.time()

                    print (timestamp(timerA),timestamp(timerB))
                    
                    #print(timestamp(timerA)[6:8],timestamp(timerB)[6:8])
                except NameError:
                    pass
                try:
                    #print (timestamp(recognizedstart),timestamp(recognizedend))
                    if int(timestamp(timerA)[3:5])==int(timestamp(timerB)[3:5]) and int(timestamp(timerA)[6:8])>=(int(timestamp(timerB)[6:8])+tresholddetect):
                        if emailsent==False:
                            cv2.imwrite("FOLDERSISTEMKEAMANAN/Takdikenal/Gambar"+str(nomorFile) + ".jpg",im)
                            sendemail()
                            #listcoordinates.clear()
                            emailsent=True
                    if int(timestamp(timerA)[3:5]) > int(timestamp(timerB)[3:5]) and int(timestamp(timerA)[7])>=int(timestamp(timerB)[7]):
                        if emailsent==False:
                            cv2.imwrite("FOLDERSISTEMKEAMANAN/Takdikenal/Gambar"+str(nomorFile) + ".jpg",im)
                            sendemail()
                            #listcoordinates.clear()
                            emailsent=True
                except NameError:
                    pass
                cv2.imshow('Kenali Wajah',im)
                if (cv2.waitKey(1)==ord('q')):
                    #print (len(listcoordinates))
                    break 

                width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
                height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT) # float

                teksx = int(width / 2) - int(width/4)
                teksy = int((95/100)* height)
                            
                cv2.putText(im,'Tekan Q untuk keluar',(teksx,teksy), font, 1,(255,255,255),2,cv2.LINE_AA)   
                #im = cv2.resize(im, (1280,720))
                cv2.imshow('Kenali Wajah',im) 
                if (cv2.waitKey(1)==ord('q')):
                    break 
            cam.release()
            cv2.destroyAllWindows() 

        except cv2.error as e:
                print(e)
    
    
    

    img_rekam = Image.open("Button_Deteksi.jpg")
    #img_rekam = img_rekam.resize((180, 130))
    renderimg = ImageTk.PhotoImage(img_rekam)
    button_rekam = Button(window, image=renderimg, font=('Bahnschrift', 13, 'bold'),bd=0,command=loadingpath)
    button_rekam.image = renderimg
    button_rekam.place(x=150, y=200)
    

    

def call_mainroot():
	splashscreen.destroy()
	mainroot()

splashscreen.after(3000,call_mainroot)
mainloop()