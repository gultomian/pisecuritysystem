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





#Main Program
def mainroot():
    window = Tk()
    window.configure(background='#f1f0f0')
    #window.resizable(0,0)
    window.iconbitmap("Logo_Aplikasi.ico")
    window.title("Sistem Keamanan Rumah")

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

    lbl1 = Label(window, text="Nama", font=('Bahnschrift', 16))
    lbl2 = Label(window, text="Email", font=('Bahnschrift', 16))
    entry1 = Entry(window, width=25, font=('Bahnschrift', 15))
    entry2 = Entry(window, width=25, font=('Bahnschrift', 15))
    message1 = Label(window, text="", font=('Bahnschrift', 12))
    #button_rekam = Button(window, text="Mulai Rekam", font=('helvetica', 13, 'bold'))


    lbl1.place(x=50, y=175)
    lbl2.place(x=50, y=210)
    entry1.place(x=160, y=175)
    entry2.place(x=160, y=210)
    message1.place(x=250, y=250, anchor='center')


    menu = Menu(window)
    window.config(menu=menu)

    dropdown_file = Menu(menu, tearoff=0)
    dropdown_view = Menu(menu, tearoff=0)

    menu.add_cascade(label='File', menu=dropdown_file)
    menu.add_cascade(label='View', menu=dropdown_view)

    global pathsave
    pathsave = StringVar()
    pathsave.set('FOLDERSISTEMKEAMANAN/')
    def savingpath(): 
        folder_pilihan = fd.askdirectory(title='Pilih Folder')
        direktoripenyimpanan=folder_pilihan+'/FOLDERSISTEMKEAMANAN/'
        os.mkdir(direktoripenyimpanan)
        pathsave.set(direktoripenyimpanan)
        
    def hapusdata():
        folder_pilihan = fd.askdirectory(title='Pilih Folder',)
        if 'FOLDERSISTEMKEAMANAN' in folder_pilihan:
            yesnohapus=mb.askyesno('Anda Yakin','Anda yakin ingin menghapus folder ini?')
            if yesnohapus:
                shutil.rmtree(folder_pilihan)
        else:
            mb.showinfo('Nama Folder Salah', 'Nama Folder Harus "FOLDERSISTEMKEAMANAN"')
        
    def viewuser():
        userwin = Toplevel(window)
        userwin.iconbitmap("Logo_Aplikasi.ico")
        userwin.title("Daftar User")
        width = 400
        height = 400
        screen_width = userwin.winfo_screenwidth()
        screen_height = userwin.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        userwin.geometry("%dx%d+%d+%d" % (width, height, x, y))
        userwin.resizable(0, 0)
        frame_header = Frame(userwin, width=200, pady=5) 
        frame_header.pack(side=TOP, anchor=CENTER)  
        
        TableMargin = Frame(userwin, width=200)
        TableMargin.pack(side=TOP)
        scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
        scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
        tree = ttk.Treeview(TableMargin, columns=("Nama", "Email"), height=200, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('Nama', text="Nama", anchor=W)
        tree.heading('Email', text="Email", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=190)
        tree.column('#2', stretch=NO, minwidth=0, width=190)
        tree.pack()

        tree.delete(*tree.get_children())
        try:
            with open(pathsave.get()+'DescUser.csv') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    Nama = row['Nama']
                    Email = row['Email']
                    tree.insert("", 0, values=(Nama, Email))
        except FileNotFoundError:
            pass

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
    dropdown_file.add_command(label='Set Direktori Penyimpanan...',command=savingpath)
    dropdown_file.add_separator()
    dropdown_file.add_command(label='Hapus Data User',command=hapusdata)
    dropdown_view.add_command(label='User',command =viewuser)
    



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
            answer = max(int(column[1].replace(',', '')) for column in reader)
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
            Nama=(entry1.get())
            Email=(entry2.get())
            savepath=pathsave.get()
            Label=1
            
            if not os.path.exists("FOLDERSISTEMKEAMANAN/"):
                os.mkdir("FOLDERSISTEMKEAMANAN/")
            
            if any(x.isalpha() for x in Nama) and not any(x.isdigit() for x in Nama) and cek_duplikat_nama(Nama)==False and cek_duplikat_nama(Email)==False and '@' in Email:
                mb.showinfo("Ambil Gambar","Pastikan Wajah yang tertangkap di kamera hanya wajah anda\ndan terdapat cukup sinar untuk kamera mendeteksi muka\nTekan Q untuk keluar dari kamera")   
                cam = cv2.VideoCapture(portnum.get())
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
                        if not os.path.exists(savepath+"pretrained/GambarTraining/"):
                            if not os.path.exists(savepath+"pretrained/"):
                                os.mkdir(savepath+"pretrained/")
                            os.mkdir(savepath+"pretrained/GambarTraining/")
                        try:    
                            if csvgetmaxlabel(savepath+'DescUser.csv') >= 1:
                                cv2.imwrite(savepath+"pretrained/GambarTraining/"+Nama +"."+str(int(csvgetmaxlabel(savepath+'DescUser.csv'))+1)+'.'+ str(nomorSample) + ".jpg", gray[y:y+h,x:x+w])
                        except FileNotFoundError:
                            cv2.imwrite(savepath+"pretrained/GambarTraining/"+Nama +"."+'1.'+ str(nomorSample) + ".jpg", gray[y:y+h,x:x+w])
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
                    if csvgetmaxlabel(savepath+'DescUser.csv') >= 1:
                        Label = str(int(csvgetmaxlabel(savepath+'DescUser.csv'))+1)
                except FileNotFoundError:
                    pass
                row = [Nama, Label, Email]
                
                if not os.path.isfile(savepath+'DescUser.csv'):
                    with open(savepath+'DescUser.csv', mode='w', newline='') as file_output:
                        file_csv = csv.writer(file_output)
                        file_csv.writerow(['Nama','Label','Email'])
                    file_output.close()
                    with open(savepath+'DescUser.csv',mode='a+', newline='') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                    csvFile.close()
                else:
                    with open(savepath+'DescUser.csv',mode='a+', newline='') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow(row)
                    csvFile.close()
                #message1.configure(text= res,fg='green')
                mb.showinfo("Data Disimpan",res)

                #recognizer = face.createLBPHFaceRecognizer()
                recognizer = cv2.face.LBPHFaceRecognizer_create() 
                #$cv2.createLBPHFaceRecognizer()
                mukamuka,labelgambar = getgambardanlabel(savepath+'pretrained/gambartraining')
                recognizer.train(mukamuka, np.array(labelgambar))
                if not os.path.exists(savepath+'trained/'):
                    os.mkdir(savepath+'trained/')
                recognizer.save(savepath+'trained/Trainer.yml')
                #+",".join(str(f) for f in Id)
                #message1.configure(text= res,fg='green')
                mb.showinfo("Proses Selesai","Proses training data selesai")

            elif len(Nama)<=0 and len(Email)<=0:
                res = "Form harus dilengkapi"
                message1.configure(text= res,fg='red')
            elif not any(x.isalpha() for x in Nama) or any(x.isdigit() for x in Nama):
                res = "Nama harus berisi huruf alfabet"
                message1.configure(text= res,fg='red')
            elif cek_duplikat_nama(Nama):
                res = "Nama sudah ada didalam database"
                message1.configure(text= res,fg='red')
            elif cek_duplikat_nama(Email):
                res = "Email sudah ada pernah digunakan sebelumnya"
                message1.configure(text= res,fg='red')
            elif not '@' in Email:
                res = "Email harus diisi dengan benar"
                message1.configure(text= res,fg='red')
            
        except cv2.error as e:
            mb.showerror("Error",e)
            

    img_rekam = Image.open("Button_Rekam.jpg")
    #img_rekam = img_rekam.resize((180, 130))
    renderimg = ImageTk.PhotoImage(img_rekam)
    button_rekam = Button(window, image=renderimg, font=('Bahnschrift', 13, 'bold'),bd=0,command=ambilgambar)
    button_rekam.image = renderimg
    button_rekam.place(x=170, y=267)


def call_mainroot():
	splashscreen.destroy()
	mainroot()

splashscreen.after(3000,call_mainroot)         #TimeOfSplashScreen
mainloop()