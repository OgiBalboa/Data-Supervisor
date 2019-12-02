"""
Data finder MENU
author = @ogibalboa

ALGORİTMA

Menu açılır --> Seçim yapılır ( sorgu değişkenine seçim numarası aktarılır.) --> sorgu numarasına göre gerekli modüller çağırılır.
"""
import tkinter 
from tkinter import *
print("Yükleniyor...")
import time
from time import sleep
sleep(0.2)
print("Time lib içeri aktarıldı.")
import os
import sys
print("Os lib içeri aktarıldı.")
#import bin.verianaliz as verianaliz
import verianaliz
import filesearch
sleep(0.2)
print("veri analiz modülü içeri aktarıldı")
def line(x):
    print("*" * x)
def wt():
    sleep(0.5)
global dosyayolu
dosyayolu = os.getcwd()
global son_dosya_adi
son_dosya_adi = ""
#-------------------------------MAKİNE İLE PARALEL ÇALIŞMA-----------------------
def paralel(path):
    global veri_count
    global hata_count
    global son_dosya_adi
    os.chdir(path)
    file = filesearch.dosyabul()
    file.findate()
    if son_dosya_adi != file.filename:
        son_dosya_adi = file.filename
        print("\nTarama yapılan dosya tarihi : " + str(file.filename))
    file.detect_new(file.filename)
    file.fileflag = None
    while 1:
        if len(file.data_name) > 1 :
                analiz = verianaliz.dosya_aktar(file.data_name,file.data_path,True)
                file = None
                veri_count+=1
                if analiz.errorflag == True:
                    hata_count+= 1
                break
        else :
            file.findate()
def run():
    global veri_count
    global hata_count
    veri_count = 0
    hata_count = 0
    menu.destroy()
    anayol = os.getcwd()
    print("\n\nVeriler Taranıyor")
    print("Çıkmak için CTRL + C ye basınız...")

    while 1:
            try :
                paralel(anayol)
            except KeyboardInterrupt :
                print("Taranan veri sayısı : " + str(veri_count))
                print("Hatalı veri sayısı : " + str(hata_count))
                input("\n\nDevam etmek için Enter'a basınız.")
                os.chdir(anayol)
                return Menu()
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
           fl.write(error.info)
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
        print("\nTaranan veri sayısı : " + str(len(verino.files)) + "\nHatalı veri sayısı : " + str(hatacount) +"\n\nHatalı Dosyalar :\n\n" )
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
        line(52)
        print("Error Logları : \n")
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
        errorwindow = Tk()
        errorwindow.title("Error Log")
        def gotofile():
            errorwindow.destroy()
            name = hatalar[goruntule-1][2:4]+hatalar[goruntule-1][5:7]+hatalar[goruntule-1][8:10]+hatalar[goruntule-1][11:13]+hatalar[goruntule-1][14:16]
            
            error_analiz = verianaliz.sorgu.errorfile(name,hatalar[goruntule-1][0:10])
            if error_analiz == None :
                print("\n\nHATA ! dosya kayıp ! ")
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
        Button(errorwindow,text = " Hataları Tekrar Görüntüle ", command = again).pack()
        Button(errorwindow,text = " Hataya ait veriyi incele ", command = gotofile).pack()
        Button(errorwindow,text = " Menüye Dön ", command = cikis).pack()
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
