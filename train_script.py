from tkinter import * #tkinter untuk GUI
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import cv2, os      #cv2 (opencv) untuk proses dataset
import csv          #csv untuk jadiin list ke file .csv
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

window = Tk()
window.configure(background='#f1f0f0')
#window.resizable(0,0)
window.iconbitmap("Logo_Aplikasi.ico")
window.title("Sistem Keamanan Rumah")
window.configure(background='#f1f0f0')


width = 500
height = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
window.geometry("%dx%d+%d+%d" % (width, height, x, y))
window.resizable(0, 0)

logo = Image.open("banner.jpg")
renderlogo = ImageTk.PhotoImage(logo)

# label dijadiin variabel logo
img = Label(window, image=renderlogo)
img.image = renderlogo
img.place(x=50, y=30)

lbl2 = Label(window, text="Nama", font=('helvetica', 15))
entry2 = Entry(window, width=25, font=('helvetica', 15))
message1 = Label(window, text="", font=('helvetica', 15))
#button_rekam = Button(window, text="Mulai Rekam", font=('helvetica', 13, 'bold'))


lbl2.place(x=50, y=205)
entry2.place(x=160, y=205)
message1.place(x=250, y=250, anchor='center')


def cek_duplikat_nama(inputnama):
    try:
        with open ('DescUser.csv', 'r') as f:
            reader = csv.reader(f)
            list_kelas = list(reader)
        list_kelas = [i[0] for i in list_kelas]

        if inputnama in list_kelas:
            return True
        else:
            return False
    
    except(FileNotFoundError):
        return False

def csvgetmaxlabel(path):
    with open(path, 'rU') as f:
        reader = csv.reader(f)
        next(reader)     # Skip header row
        answer = max(int(column[-1].replace(',', '')) for column in reader)
    return answer


def getgambardanlabel(path):
    #ambil path dari file di folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #buat list kosong untuk muka
    mukamuka=[]
    #buat list kosong untuk npm
    labelgambar=[]
    #buat looping untuk path gambar dan load npm sama gambar
    for imagePath in imagePaths:
        #konversi gambar ke grayscale
        pilImage=Image.open(imagePath).convert('L')
        #konversi gambar PIL ke numpy array
        imageNp=np.array(pilImage,'uint8')
        #ambil NPM dari gambar
        labelfile=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract muka dari sample training
        mukamuka.append(imageNp)
        labelgambar.append(labelfile)        
    return mukamuka,labelgambar

def ambilgambar():   
    try:
        Nama=(entry2.get())
        Label=1
        
        if any(x.isalpha() for x in Nama) and any(x.isspace() for x in Nama) and not any(x.isdigit() for x in Nama) and cek_duplikat_nama(Nama)==False :
            mb.showinfo("Ambil Gambar","Pastikan Wajah yang tertangkap di kamera hanya wajah anda\ndan terdapat cukup sinar untuk kamera mendeteksi muka\nTekan Q untuk keluar dari kamera")   
            cam = cv2.VideoCapture(1)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            nomorSample=0
            width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
            height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT) # float

            teksx = int(width / 2) - int(width/4)
            teksy = int((95/100)* height)
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                font = cv2.FONT_HERSHEY_SIMPLEX 
                muka = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in muka:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.putText(img,'Tunggu Beberapa Detik',(teksx,teksy), font, 1,(255,255,255),2,cv2.LINE_AA)        
                    #increment nomor sample biar bisa dibedakan 
                    nomorSample=nomorSample+1
                    #ssimpan gambar yang ditangkap ke folder GambarTraining
                    if not os.path.exists("pretrained/GambarTraining/"):
                        if not os.path.exists("pretrained/"):
                            os.mkdir("pretrained/")
                        os.mkdir("pretrained/GambarTraining/")
                    try:    
                        if csvgetmaxlabel('DescUser.csv') >= 1:
                            cv2.imwrite("pretrained/GambarTraining/"+Nama +"."+str(int(csvgetmaxlabel('DescUser.csv'))+1)+'.'+ str(nomorSample) + ".jpg", gray[y:y+h,x:x+w])
                    except FileNotFoundError:
                        cv2.imwrite("pretrained/GambarTraining/"+Nama +"."+'1.'+ str(nomorSample) + ".jpg", gray[y:y+h,x:x+w])
                    #display frame windows
                    cv2.imshow('Deteksi Wajah',img)
                #tunggu 100 milisecond 
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break kalo sample udah sampai 50
                elif nomorSample>=100:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            res = "Data dengan Nama: "+ Nama +" disimpan"
            try:
                if csvgetmaxlabel('DescUser.csv') >= 1:
                    Label = str(int(csvgetmaxlabel('DescUser.csv'))+1)
            except FileNotFoundError:
                pass
            row = [Nama, Label]
            
            if not os.path.isfile('DescUser.csv'):
                with open('DescUser.csv', mode='w', newline='') as file_output:
                    file_csv = csv.writer(file_output)
                    file_csv.writerow(['Nama','Label'])
                file_output.close()
                with open('DescUser.csv',mode='a+', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()
            else:
                with open('DescUser.csv',mode='a+', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                csvFile.close()
            #message1.configure(text= res,fg='green')
            mb.showinfo("Data Disimpan",res)

            #recognizer = face.createLBPHFaceRecognizer()
            recognizer = cv2.face.LBPHFaceRecognizer_create() 
            #$cv2.createLBPHFaceRecognizer()
            mukamuka,labelgambar = getgambardanlabel('pretrained/gambartraining')
            recognizer.train(mukamuka, np.array(labelgambar))
            if not os.path.exists('trained/'):
                os.mkdir('trained/')
            recognizer.save('trained/Trainer.yml')
            #+",".join(str(f) for f in Id)
            #message1.configure(text= res,fg='green')
            mb.showinfo("Proses Selesai","Proses training data selesai")

        elif not any(x.isalpha() for x in Nama) and any(x.isspace() for x in Nama) or any(x.isdigit() for x in Nama):
             res = "Nama harus berisi huruf alfabet"
             message1.configure(text= res,fg='red')
        elif len(Nama)<=0:
            res = "Form harus dilengkapi"
            message1.configure(text= res,fg='red')
        elif cek_duplikat_nama(Nama):
            res = "Nama sudah ada didalam database"
            message1.configure(text= res,fg='red')
        
    except cv2.error as e:
        mb.showerror("Error",e)
    

img_rekam = Image.open("Button_Rekam.jpg")
#img_rekam = img_rekam.resize((180, 130))
renderimg = ImageTk.PhotoImage(img_rekam)
button_rekam = Button(window, image=renderimg, font=('helvetica', 13, 'bold'),bd=0,command=ambilgambar)
button_rekam.image = renderimg
button_rekam.place(x=170, y=270)


window.mainloop()