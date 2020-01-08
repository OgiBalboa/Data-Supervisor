#-------------------------------------------------
# Name:         Data Supervisor Main Menu
# Author :      ogulcan@AISIN
# Date :        13.12.2019
# Licence :     <GNU GCC>
#-------------------------------------------------
print("\n"*50)
from threading import Thread  
from tkinter import *
from tkinter import filedialog,messagebox
from tkinter import StringVar, IntVar
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
from settings import settings, program_files,bug_report
settings = settings()
program_files = program_files()
bug = bug_report()
#-------------------------------MAKİNE İLE PARALEL ÇALIŞMA--------------------------------------------
global sttw # Status window için global değişken
def parallel():   # Makine ile paralel çalışmayı sonsuz döngüye sokabilmek için ana programdan ayrılması gerekmekte. Bunun için threading kullanıldı.
    global file
    global ec
    ec = 0
    while 1:
            if settings.paralel_stop != True:
                file = None
                file = filesearch.dosyabul()
                #Label(sttw,text = "reftime : " + str(file.reftime),fg= "white",bg = "#094BFC",font=("Arial",12)).place(x=0,y=95)
                try:
                    paralel()
                except:
                    bug.report()
                    settings.paralel_stop = True
                    file.status = " PROGRAMDA HATA OLUŞTU LÜTFEN TEKRAR BAŞLATIN !"
                    durum_gui.set("\nDurum : " + str(file.status)+"\nBULUNAN HATA :"+bug.error)
                    durum_gui.get()
            else:
                time.sleep(1)
def paralel():
    global veri_count
    global hata_count
    global son_dosya_adi
    global sttw
    global file
    def gui_update():
        tarama_tarihi_gui.set("Tarama Başlama Tarihi : "+ str(datetime.now())[0:16])
        tarama_tarihi_gui.get()
        veri_sayisi_gui.set("Taranan Veri sayısı : " + str(veri_count))
        veri_sayisi_gui.get()
        hatali_veri_gui.set("\nHatalı Veri Sayısı : " + str(hata_count))
        hatali_veri_gui.get()
        durum_gui.set("\nDurum : " + str(file.status))
        durum_gui.get()
    os.chdir(program_files.datas)
    file.findate()
    Label(sttw,text = "Tarama yapılan dosya tarihi : " + str(file.filedate),fg= "white",bg = "#094BFC",font=("Arial",12)).place(x=0,y=70)
    file.detect_new(file.filedate) # Yeni veri bulmak için
    gui_update()
    if file.search_again == True:
        ec = 0
        return
    file.fileflag = None
    while 1:
            if file.data_name != None and settings.paralel_stop != True:
                if file.data_name[-4::] == ".csv":
                        file.status = "Analiz Başladı " +" "*55
                        gui_update()
                        analiz = verianaliz.analiz(file.data_name,file.data_path,date =file.filedate, aramaflag = True,noprint = True)
                        if analiz.errorflag == True :
                            err = "Var"
                        else :
                            err = "Yok"
                        file.status = "Analiz Tamamlandı, Hata : " +str(err) + ".....Yeni veri bekleniyor ....."+" "*55
                        veri_count+=1
                        if analiz.errorflag == True:
                            hata_count+= 1
                        gui_update()
                        ec  = 0
                        break
                else :
                    file.detect_new(file.filedate)
                    if file.search_again == True:
                        ec = 0
                        break
            elif settings.paralel_stop == True:
                ec = 0
                break

def run(again = None):
    global tarama_tarihi_gui
    global veri_sayisi_gui
    global hatali_veri_gui
    global durum_gui
    global veri_count
    global hata_count
    global anayol
    global sttw
    settings.paralel_stop = None
    def stop():
        sttw.destroy()
        settings.paralel_stop = True
        return Menu()
    if again != True:
        veri_count = 0
        hata_count = 0
        try:
            menu.destroy()
        except:
            pass
        anayol = os.getcwd()
        print("\n\nVeriler Taranıyor")
        print("Tarama Başlama Tarihi : "+ str(datetime.now())[0:16])
        print("(Çıkmak için CTRL + C ye basınız...)")
        global sttw
        sttw = Tk()
        sttw.title("TARAMA BAŞLADI")
        sttw.geometry("600x600")
        sttw.configure(bg = "#094BFC")
        try:
            sttw.iconbitmap("bin/icon.ico")
        except:
            pass
        tarama_tarihi_gui = StringVar()
        tarama_tarihi_gui.set("Tarama Başlama Tarihi : "+ str(datetime.now())[0:16])
        veri_sayisi_gui = StringVar()
        veri_sayisi_gui.set("Taranan Veri sayısı : " + str(veri_count))
        hatali_veri_gui = StringVar()
        hatali_veri_gui.set("\nHatalı Veri Sayısı : " + str(hata_count))
        durum_gui = StringVar()
        durum_gui.set("\nDurum : Yeni Tarama Başladı, Dosya Bekleniyor...")
        Label(sttw,textvariable = tarama_tarihi_gui,fg= "white",bg = "#094BFC",font=("Arial",12)).place(x=0,y=10)
        Label(sttw,textvariable =veri_sayisi_gui ,fg= "white",bg = "#094BFC",font=("Arial",12)).place(x=0,y=120)
        Label(sttw,textvariable =hatali_veri_gui ,fg= "red",bg = "#094BFC",font=("Arial",12)).place(x=0,y=180)
        Label(sttw,textvariable = durum_gui,fg= "green",bg = "#094BFC",justify = LEFT,font=("Arial",12)).place(x=0,y=300)
        Label(sttw,text = "_"*150,fg= "white",bg = "#094BFC").place(x=0,y=100)
        Label(sttw,text = "_"*150,fg= "white",bg = "#094BFC").place(x=0,y=220)
        Button(sttw,text = "TARAMAYI DURDUR ",font=("Arial",12),fg = "white",bg = "#570215",command = stop).place(x=50,y=500)
        durum = Thread(target = parallel)
        durum.daemon = True
        durum.start()
    sttw.mainloop()
    try:
        if file.search_again == True:
            durum.join()
    except:
        pass
    """
    os.chdir(anayol)
    return Menu()
    """
vericount = 0 # Paralel çalışma sırasında verileri ve hataları sayacak olan değişken.
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
           error = verianaliz.analiz(verino.files[i],filename,noprint = True,aramaflag=False)
           recov = os.getcwd()
           os.chdir(dosyayolu)
           os.chdir("Errors")
           os.chdir("Manual")
           try:
               os.mkdir(filename)
           except:
               pass
           os.chdir(filename)
           try:
               fl = open(data_name,"a+")
               errorfilename = "\nOrijinal Dosya Adı : " + verino.files[i] +"\n"
               fl.write(errorfilename)
               fl.write(error.info)
               fl.write(error.error_info)
               fl.close()
           except:
                bug.report()
           os.chdir(recov)
        os.chdir(dosyayolu)
        hata_gui.destroy()
        return Menu()
    def again():
        hata_gui.destroy()
        again = True
        return sorgula(True)
    def cikis():  # ÇIKIŞ
        hata_gui.destroy()
        os.chdir(dosyayolu)        
        return Menu()
    hata_gui = Tk()
    hata_gui.title("Sorgu Hataları")
    hata_gui.geometry("200x200")
    try:
        hata_gui.iconbitmap("bin/icon.ico")
    except:
        pass
    Button(hata_gui,text = " Aynı dosyadan başka sorgu ",command = again).pack()
    Button(hata_gui,text = "Hatalı dosya bilgilerini dışa aktar",command = export_error).pack()      
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

    try:
        if verino.gunluk == True:  # 1 GÜNDEKİ TÜM DOSYALARI TARATMAK İÇİN
                print("Gün içinde bulunan tüm veriler taranıyor....\n")
                for veriler in range (0,len(verino.files)):
                    vericount+=1
                    gunluk_analiz = verianaliz.analiz(verino.files[veriler],verino.dosya_yolu,aramaflag = False,noprint = True)
                    if gunluk_analiz.errorflag == True:
                        errorlist.append(veriler)
                        print("HATALI VERİ ADI  :  ",end = '')
                        print(verianaliz.sorgu.ayir(verino.files[veriler],veriler),"\n")
                        print(gunluk_analiz.info)
                        hatacount+=1  
                        line(52)   
                        print("\n")
                    #print(vericount,"/",len(verino.files))
                verino.gunluk = False
                print("\nTaranan veri sayısı : " + str(len(verino.files)) + "\nHatalı veri sayısı : " + str(hatacount))
                if hatacount >0:
                    print("\n\nHatalı Dosyalar :\n\n" )
                    for i in errorlist:
                        print(verianaliz.sorgu.ayir(verino.files[i],i),"\n")
                input("Devam Etmek için Enter'a basınız...")
                hatacount = 0
                vericount = 0
                return hata_ekrani()
    except Exception as e:
        print(e)
    #input("Devam Etmek için Enter'a basınız")
    if verino.iptal == False:   # SORGU BİLGİLERİ İSTENİYOR MU ?
        analiz = verianaliz.analiz(verino.dosya,verino.dosya_yolu,noprint = False)
        try:
            input('Grafiği görmek için Enterla \n Çıkmak için CTRL+C ...') 
            analiz.plot()
            input('\n\nDevam etmek için Entera basınız....')
            return hata_ekrani()
        except :
            pass
        print("Sorgu tamamlandı.\n")
        line(52)
    else :
        pass
    return Menu()
def sorgu_sonrasi():    
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
        """
        try:
            menu.destroy()
        except:
            pass
        """
        try:
            window.destroy()
        except:
            pass
        def erwindow():
            global errorwindow
            errorwindow = Tk()
            errorwindow.title("Error Log")
            errorwindow.geometry("300x300")
            try:
                errorwindow.iconbitmap("bin/icon.ico")
            except:
                pass
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
            os.chdir(program_files.auto_errors)
            tarih = filedialog.askdirectory(initialdir =os.getcwd() ,title = "Dosya Tarihi Seçiniz",)
            try:
                os.chdir(tarih)
                menu.destroy()
            except:
                messagebox.showerror("HATA ! "," Tarih Seçmediniz !")
                try:
                    menu.destroy()
                except:
                    pass
                return Menu()
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
                menu.destroy()
                return Menu()
            except Exception as e:
                hata = "Hatalı veri girdiniz. \nHata adı : " +str(e)
                messagebox.showerror("HATA !",hata)
                os.chdir(dosyayolu)
                menu.destroy()
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
            os.chdir(program_files.manu_errors)
            initial = os.getcwd()
            tarih = filedialog.askdirectory(initialdir =initial ,title = "Dosya Tarihi Seçiniz",)
            try:
                os.chdir(tarih)
                menu.destroy()
            except:
                messagebox.showerror("HATA ! "," Tarih Seçmediniz !")
                try:
                    menu.destroy()
                except:
                    pass
                return Menu()
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
                error_analiz = verianaliz.sorgu.go_to_date(name,hatalar[goruntule-1][0:10])
                print(name,hatalar[goruntule-1])
            else:
                
                name = tarih[-8:-6]+tarih[-5:-3]+tarih[-2::]+hatalar[goruntule-1][0:2]+ hatalar[goruntule-1][3:5]
                os.chdir(dosyayolu)
                error_analiz = verianaliz.sorgu.go_to_date(name,tarih[-10:])
            if error_analiz == None :
                print("\n\nHATA ! DOSYA KAYIP ! ")
                menu.destroy()
                return Menu()
            else:
                    analiz = verianaliz.analiz(str(error_analiz),hatalar[goruntule-1][0:10],noprint = True)
                    input('Grafiği görmek için Enterla')
                    analiz.plot()
                    print("Sorgu tamamlandı.\n")
                    line(52)
            return errorlog()
        def cikis():
            errorwindow.destroy()
            os.chdir(dosyayolu)
            try:
                menu.destroy()
            except:
                pass
            return Menu()
        def again():
            errorwindow.destroy()
            os.chdir(dosyayolu)
            return errorlog()
        Button(errorwindow,text = "Otomatik kaydedilen verileri görüntüle",command = oto).pack()
        Button(errorwindow,text = "Manuel kaydedilen verileri görüntüle",command = manual).pack()
        Button(errorwindow,text = "Menüye Dön",command = cikis).pack()
        errorwindow.mainloop()

#----------------------------------- ANA MENU ------------------------------------------        
def Menu():
    os.chdir(program_files.main)
    global menu
    menu = Tk()
    menu.title("Trend Tracker")
    menu.geometry("400x400")
    menu.configure(bg = "#094BFC")
    try:
        menu.iconbitmap("bin/icon.ico")
    except:
        pass
    def settin():
        messagebox.showinfo("DİKKAT !","Ayarlar dosyasını açtıktan sonra programı yeniden başlatınız !")
        os.system("start setting.bat")
    Label (menu,text = "Ne Yapmak İstiyorsunuz ?",bg = "#094BFC",fg = "white",font=("Arial",14)).pack()
    Button(menu,text = "Makine ile Paralel Çalışma",font=("Arial",12),command = run).pack()
    Button(menu,text = "Makine Verileri Sorgula",font = ("Arial",12),command = sorgula).pack()
    Button(menu,text = "Hataları Görüntüle",font = ("Arial",12),command = errorlog).pack()
    Button(menu,text = "Ayarlar",font = ("Arial",12),command = settin).pack()    
    Button(menu,text = " ÇIKIŞ ",command = menu.destroy).pack()
    if settings.wait_for_data < settings.process_time:
        messagebox.showinfo("DİKKAT !","veri bekleme süreniz ("+str(settings.wait_for_data)+\
                             ") Proses Sürenizden ("+str(settings.process_time)+") daha kısa, hataya yol açabilir !")
    menu.mainloop()
    
if __name__== "__main__":
    try:
        if sys.argv[1] == "run":
            run()
        else:
            Menu()
    except:
        try:
            Menu()
        except :
            bug.report()
            run()
