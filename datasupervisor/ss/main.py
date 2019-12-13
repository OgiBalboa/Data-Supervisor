"""
Data finder MENU
author = @ogibalboa
"""
print("\n"*50)
from threading import Thread
from tkinter import *
print("Yükleniyor...")
import time
from time import sleep
import os
import sys
import verianaliz
import filesearch
print("veri analiz modülü içeri aktarıldı")
from datetime import datetime
def line(x):
    print("*" * x)
def wt():
    sleep(0.5)
global dosyayolu
dosyayolu = os.getcwd()
global son_dosya_adi
son_dosya_adi = ""
from settings import settings
settings = settings()
#-------------------------------MAKİNE İLE PARALEL ÇALIŞMA-----------------------
global sttw
def paralel(path):
    global veri_count
    global hata_count
    global son_dosya_adi
    global sttw
    os.chdir(path)
    file = filesearch.dosyabul()
    file.findate()
    if son_dosya_adi != file.filename:
        son_dosya_adi = file.filename
        print("\nTarama yapılan dosya tarihi : " + str(file.filename))
        Label(sttw,text = "Tarama yapılan dosya tarihi : " + str(file.filename),font=("Arial",12)).place(x=0,y=70)
    file.detect_new(file.filename)
    if file.iptal == True:
        return run(again = True)
    file.fileflag = None
    while 1:
        if len(file.data_name) > 1 :
                analiz = verianaliz.dosya_aktar(file.data_name,file.data_path,True)
                file = None
                veri_count+=1
                if analiz.errorflag == True:
                    hata_count+= 1
                print("\nTaranan veri sayısı : " + str(veri_count))
                print("Hatalı veri sayısı : " + str(hata_count))
                Label(sttw,text = "\nTaranan veri sayısı : " + str(veri_count),font=("Arial",12)).place(x=0,y=120)
                break
        else :
            file.findate()
def status():
    global sttw
    sttw = Tk()
    sttw.geometry("400x400")
    Label(sttw,text = "Tarama Başlama Tarihi : "+ str(datetime.now())[0:16],font=("Arial",12)).place(x=0,y=10)
    sttw.mainloop()

def run(again = None):
    global veri_count
    global hata_count
    global anayol
    global sttw
    if again != True:
        veri_count = 0
        hata_count = 0
        menu.destroy()
        anayol = os.getcwd()
        print("\n\nVeriler Taranıyor")
        print("Tarama Başlama Tarihi : "+ str(datetime.now())[0:16])
        print("(Çıkmak için CTRL + C ye basınız...)")
        durum = Thread(target = status)
        durum.start()
        durum.join()
    while 1:
            try :
                paralel(anayol)
            except KeyboardInterrupt :
                line(52)
                print("Taranan veri sayısı : " + str(veri_count))
                print("Hatalı veri sayısı : " + str(hata_count))
                input("\n\nDevam etmek için Enter'a basınız.")
                os.chdir(anayol)
                return Menu()
    #stw.mainloop()
    os.chdir(anayol)
    return Menu()
vericount = 0
hatacount = 0
#------------------------------ DOSYA SORGULAMA ------------------------------------
def hata_ekrani():
    def export_error():
        os.chdir(dosyayolu)
        os.chdir("Datas")
        global errorlist
        filename = verino.sorgu[-10::]
        for i in errorlist:
           data_name = verianaliz.sorgu.ayir(verino.files[i])+".txt"
           error = verianaliz.dosya_aktar(verino.files[i],filename,noprint = True,flag=False)
           recov = os.getcwd()
           os.chdir(dosyayolu)
           os.chdir("Errors")
           os.chdir("Manual")
           try:
               os.mkdir(filename)
           except:
               pass
           os.chdir(filename)
           fl = open(data_name,"a+")
           errorfilename = "Orijinal Dosya Adı : " + verino.files[i] +"\n"
           fl.write(errorfilename)
           fl.write(error.inf)
           fl.write(error.error_info)
           fl.close()
           os.chdir(recov)
        os.chdir(dosyayolu)
        hata_gui.destroy()
        return Menu()
    def select():
        pass
    def show_errors():
        pass
    def cikis():
        hata_gui.destroy()
    hata_gui = Tk()
    hata_gui.title("Sorgu Hataları")
    Button(hata_gui,text = "Hatalı dosya bilgilerini dışa aktar",command = export_error).pack()      
    #Button(hata_gui,text = "Hatayı detaylı görüntülemek için dosya seç",command = select).pack()
    #Button(hata_gui,text = "Tüm Dosyaları Sırayla Göster",command = show_errors).pack()
    Button(hata_gui,text = "ANA MENU",command = cikis).pack()      
  
def sorgula(again = None):
    global errorlist
    errorlist = []
    global vericount
    global hatacount
    global verino     # SORGU OBJESİ GLOBAL DEĞİŞKENDİR.
    try :
        menu.destroy()
    except:
        pass
    if again == True:        #AYNI SORGU TEKRAR MI YAPILIYOR ?
        verino.search(True)
        again = False # Tekrar flag reset
        pass
    else :
        verino = verianaliz.sorgu()  # DEĞİLSE YENİ SORGU OLUŞTUR
    if verino.gunluk == True:  # 1 GÜNDEKİ TÜM DOSYALARI TARATMAK İÇİN
        print("Gün içinde bulunan tüm veriler taranıyor....\n")
        for veriler in range (0,len(verino.files)):
            vericount+=1
            gunluk_analiz = verianaliz.dosya_aktar(verino.files[veriler],verino.dosya_yolu,flag = False,noprint = True)
            if gunluk_analiz.errorflag == True:
                errorlist.append(veriler)
                print("HATALI VERİ ADI  :  ",end = '')
                print(verianaliz.sorgu.ayir(verino.files[veriler],veriler),"\n")
                print(gunluk_analiz.inf)
                hatacount+=1  
                line(52)   
                print("\n")
        verino.gunluk = False
        print("\nTaranan veri sayısı : " + str(len(verino.files)) + "\nHatalı veri sayısı : " + str(hatacount))
        if hatacount >0:
            print("\n\nHatalı Dosyalar :\n\n" )
            for i in errorlist:
                print(verianaliz.sorgu.ayir(verino.files[i],i),"\n")
        input("Devam Etmek için Enter'a basınız...")
        return hata_ekrani()
           #print(verino.files[i],end = '')
    if verino.iptal == False:   # SORGU BİLGİLERİ İSTENİYOR MU ?
        analiz = verianaliz.dosya_aktar(verino.dosya,verino.dosya_yolu)
        print(analiz.inf)
        try:
            input('Grafiği görmek için Enterla \n Çıkmak için CTRL+C ...') 
            analiz.plot()
        except KeyboardInterrupt:
            pass
        print("Sorgu tamamlandı.\n")
        line(52)
    else :
        pass
    
    window = Tk()  # SORGU SONRASI PENCERE
    window.title("Sorgu Sonrası")
    def again():
        window.destroy()
        again = True
        return sorgula(True)
    def cikis():  # ÇIKIŞ
        window.destroy()
        os.chdir(dosyayolu)        
        return Menu()
    Button(window,text = " Aynı dosyadan başka sorgu ",command = again).pack()
    Button(window,text = "Menüye Dön ", command = cikis).pack()
    Button(window,text = " ÇIKIŞ ",command = window.destroy).pack()
    window.mainloop()
#-------------------------------ERROR LOGLARI-----------------------------------------
def errorlog():
        try:
            menu.destroy()
        except:
            pass
        try:
            window.destroy()
        except:
            pass
        def erwindow():
            global errorwindow
            errorwindow = Tk()
            errorwindow.title("Error Log")
        erwindow()
        def after():
            Button(errorwindow,text = " Hataları Tekrar Görüntüle ", command = again).pack()
            Button(errorwindow,text = " Hataya ait veriyi incele ", command = gotofile).pack()
            Button(errorwindow,text = " Menüye Dön ", command = cikis).pack()
            errorwindow.mainloop()
        def oto():
            global hatalar
            global goruntule
            global anlik
            global cout
            global otom
            otom = True
            errorwindow.destroy()
            line(52)
            print("\nError Logları : \n")
            anlik = os.getcwd()
            os.chdir(dosyayolu)
            os.chdir('Errors')
            hatalar = os.listdir()
            cout = 0
            for i in hatalar:
                if i[:2] == "20":   
                    cout+=1
                    print("Dosya No  :" + str(cout) + "  Dosya Adı : "+ i)
                    print('\n')
                else :
                    hatalar.pop(cout)
            try :    
                goruntule = int(input("(Çıkmak için CTRL+C'ye basınız)\nGörüntülemek istediğiniz dosya No  : "))
            except KeyboardInterrupt:
                os.chdir(dosyayolu)
                return Menu()
            dosya = open(hatalar[goruntule - 1],'r')
            print(dosya.read())
            os.chdir(anlik)
            input("Devam etmek için Enter'a basın")
            erwindow()
            after()
        def manual():
            global hatalar
            global goruntule
            global anlik
            global cout
            global otom
            global tarih
            otom = False
            errorwindow.destroy()
            line(52)
            anlik = os.getcwd()
            os.chdir(dosyayolu)
            os.chdir('Errors')
            os.chdir("Manual")
            initial = os.getcwd()
            tarih = filedialog.askdirectory(initialdir =initial ,title = "Dosya Tarihi Seçiniz",)
            os.chdir(tarih)
            hatalar = os.listdir()
            cout = 0
            print("\nError Logları : \n")
            for i in hatalar:
                    cout+=1
                    print("Dosya No  :" + str(cout) + "  Dosya Adı : "+ i)
                    print('\n')
            try :    
                goruntule = int(input("(Çıkmak için CTRL+C'ye basınız)\nGörüntülemek istediğiniz dosya No  : "))
            except KeyboardInterrupt:
                os.chdir(dosyayolu)
                return Menu()
            dosya = open(hatalar[goruntule - 1],'r')
            print(dosya.read())
            os.chdir(anlik)
            input("Devam etmek için Enter'a basın")
            erwindow()
            after()            
        def gotofile():
            errorwindow.destroy()
            if otom == True:
                name = hatalar[goruntule-1][2:4]+hatalar[goruntule-1][5:7]+hatalar[goruntule-1][8:10]+hatalar[goruntule-1][11:13]+hatalar[goruntule-1][14:16]
                
                os.chdir(dosyayolu)
                error_analiz = verianaliz.sorgu.errorfile(name,hatalar[goruntule-1][0:10])
                print(name,hatalar[goruntule-1])
            else:
                
                name = tarih[-8:-6]+tarih[-5:-3]+tarih[-2::]+hatalar[goruntule-1][0:2]+ hatalar[goruntule-1][3:5]
                print(name)
                print(tarih[-10:])
                os.chdir(dosyayolu)
                error_analiz = verianaliz.sorgu.errorfile(name,tarih[-10:])
            if error_analiz == None :
                print("\n\nHATA ! DOSYA KAYIP ! ")
                input("\nDevam Etmek için Enter'a basınız...")
            else:
                    analiz = verianaliz.dosya_aktar(str(error_analiz),hatalar[goruntule-1][0:10])
                    print(analiz.inf)
                    input('Grafiği görmek için Enterla')
                    analiz.plot()
                    print("Sorgu tamamlandı.\n")
                    line(52)
            return errorlog()
        def cikis():
            errorwindow.destroy()
            os.chdir(dosyayolu)
            return Menu()
        def again():
            errorwindow.destroy()
            os.chdir(dosyayolu)
            return errorlog()
        Button(errorwindow,text = "Otomatik kaydedilen verileri görüntüle",command = oto).pack()
        Button(errorwindow,text = "Manuel kaydedilen verileri görüntüle",command = manual).pack()
        errorwindow.mainloop()

#----------------------------------- ANA MENU ------------------------------------------        
def Menu():
    global menu
    menu = Tk()
    menu.title("MENU")
    menu.geometry("400x400")        
    Label (menu,text = "Ne Yapmak İstiyorsunuz ?",font=("Arial",14)).pack()
    Button(menu,text = "Makine ile Paralel Çalışma",font=("Arial",12),command = run).pack()
    Button(menu,text = "Makine Verileri Sorgula",font = ("Arial",12),command = sorgula).pack()
    Button(menu,text = "Hataları Görüntüle",font = ("Arial",12),command = errorlog).pack()
    Button(menu,text = " ÇIKIŞ ",command = menu.destroy).pack()
    line(52)
    menu.mainloop()

Menu()
