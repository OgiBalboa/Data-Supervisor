
import csv
import os
import tkinter
from tkinter import Button
import time
from datetime import datetime
import matplotlib.pyplot as plt
#import filesearch
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import math
import numpy as np
class dosya_aktar():
    def __init__(self,isim,yol=None):
        i = 0
        self.defaultpath = os.getcwd() #Default dosya yolu
        self.surelist = []
        self.sensor1 = []
        self.sensor2 = []
        self.anglelist1 = []
        self.anglelist2 = []
        self.errorflag = False
        try:
            os.chdir(yol)
        except:
            print("dir hatası")
        
        with open(isim,newline='') as file:
            spm = csv.reader(file,delimiter=' ',quotechar = '|')
            for r in spm:                 # DATA İÇERİSİNDEKİ HER BİR VERİYİ DENETLER
                    a = r[0].split(',')   # SURE VERİSİNİ AYIRIR
                    try:
                        if i>6:  #ilk 6 veri info satırlarıdır
                            b = r[1].split(',')  #SENSOR 2 'nin verilerini ayırır
                            self.surelist.append(str(a[0]))
                            self.sensor1.append(str(a[1]))
                            self.sensor2.append(str(b[0])) #VERİLERİ AYIRIP LİSTELERE KAYDEDER
                            if int(b[0]) > 20 or int(a[1]) > 20: # HATALI DURUM KOŞULLARI
                                self.info = "Süre : "+ str(a[0]) + "\nSensör 1: " + str(a[1]) + \
                                            "\nSensör 2 : " + str(b[0]) 
                                print(self.info)
                                print("*" * 50)
                                self.hatakayit() #HATALI DURUMU BİR LOG DOSYASINA KAYDEDEN FONKSİYON
                                self.errorflag = True


                    except :
                        pass

                    i+=1
            if self.errorflag == False:
                    print("Hatalı veri bulunamadı ! ")
            inf = "Veri Sayisi : " + str(i)
            self.veri_sayisi = i-8
            self.denetle() #ALINAN VERİLERİ İNCELE
            os.chdir(self.defaultpath) # ANA DOSYA YOLUNA GERİ DÖN
            print(inf)
            
    def hatakayit(self,):
            os.chdir(self.defaultpath)
            os.chdir("Errors")
            print(str(datetime.now())[11:16])
            self.filename  = str(datetime.now())[0:10] + "_"+str(datetime.now())[11:13]+ \
                             "-"+ str(datetime.now())[14:16]+".txt"
            
            self.errorlog = open(self.filename,'a+')
            self.errorlog.write(self.info)
            self.errorlog.write('\n' + '*'*50 + '\n')
            self.errorlog.close()
#-------------------------------GRAFİK ÇİZDİRME-------------------------------------------------------                         
    def plot (self,):  
            """
            inf = ' Sure ' + str(len(self.surelist)) + ' Sens ' + str(len(self.sensor1))
            print(inf)
            print(self.surelist)
            print('----------------')
            print(self.sensor1)
            """
            fig,(sub1,sub2) = plt.subplots(2)
            #fig = plt.figure()
            #sub = fig.add_subplot(111)
            sub1.plot(self.surelist,self.sensor1,label = 'sensor1',color = 'lightblue')
            sub1.set_title("SENSÖR 1")
            sub1.set_xlabel("Süre(ms)")
            sub1.set_ylabel("Basınç(kPa)")
            sub2.plot(self.surelist,self.sensor2,label = 'sensor2',color = 'darkred')
            sub2.set_title("SENSÖR 2")
            sub2.set_xlabel("Süre(ms)")
            sub2.set_ylabel("Basınç(kPa)")        
            plt.show()
#-------------------------------VERİLERİN AÇILARINI BULMAK-------------------------------------------------------       
    def acibul1(self,veri):
            if veri < len(self.surelist)-1:
                self.y = float(self.sensor1[veri+1]) - float(self.sensor1[veri])
                self.x = 100*float(self.surelist[veri+1]) - 100*float(self.surelist[veri])
                self.tan = self.y / self.x
                self.angle = math.degrees(math.atan(self.tan))
                self.anglelist1.append(self.angle)
                
    def  acibul2(self,veri):
            if veri < len(self.surelist)-1:
                self.y2 = float(self.sensor2[veri+1]) - float(self.sensor2[veri])
                self.x2 = 100*float(self.surelist[veri+1]) - 100*float(self.surelist[veri])
                self.tan2 = self.y2 / self.x2
                self.angle2 = math.degrees(math.atan(self.tan2))
                self.anglelist2.append(self.angle2)
                
    def acibul(self,x2,x1,t2,t1):
                y = float(x2) - float(x1)
                x = 100*float(t2) - 100*float(t1)
                tan = y/x
                self.aci = math.degrees(math.atan(tan))
#-------------------------------VERİLERİ İNCELE-------------------------------------------------------                   
    def denetle(self,):
             for i in range (0,len(self.surelist)):
                 self.acibul1(i)
                 self.acibul2(i)

#-------------------------------DOSYALARI BULMA MODÜLÜ-------------------------------------------------------      
class sorgu():
    def __init__(self,):
        self.defaultpath = os.getcwd() #Default dosya yolu
        os.chdir("Datas")
        self.temppath = os.getcwd()
        self.gui()
        
    def gui(self,):
        self.penc = Tk()
        self.penc.title("Veri Analiz")
        self.penc.geometry("500x500")
        
        def check():
            if len(self.sorgu) < 1:
                messagebox.showerror("HATA !","Dosya seçmediniz !")
                self.gui()

        def atama(entr):
            self.sorgu = entr
            self.penc.destroy()
            check()
            self.search()
            return None
        def entry():
            self.entr = Entry(self.penc,width = 5)
            self.entr.bind("<Return>", (lambda event: atama(self.entr.get())))
            self.entr.pack()
        def tarih():
            Label(self.penc,text = "İstediğiniz dosya için tarih giriniz (YIL-AY-GUN seklinde)").pack()
            entry()
        def askdir():
            self.sorgu = filedialog.askdirectory(initialdir =self.temppath ,title = "Dosya Seçiniz",)
            self.penc.destroy()
            check()
            self.search()
        Button(self.penc,text = "Tarih ile arama ",command = tarih).pack()
        Button(self.penc,text = "Dosya Bul",command = askdir).pack()

        self.penc.mainloop()
                
    def search(self,):
        try:
            os.chdir("Datas")
        except:
            pass
        try:
            os.chdir(self.sorgu)
        except:
            #messagebox("HATA !", "Tarihi yanlis girdiniz ve ya o tarih de dosya bulunmamakta,tekrar deneyin. ")
            print("hatali")
            self.gui()
            return None
        os.chdir(self.sorgu)
        self.dosya_yolu = os.getcwd()
        self.dosyalar = os.listdir()
        self.files = []
        self.cout = 0
        print("Arama başlatılıyor..")
        time.sleep(0.5)
        for i in self.dosyalar:
            self.check(i)
            if self.flag:
                self.cout +=1
                self.files.append(i)
                self.dosyaid = i[20:26]
                self.dosyah = i[33:39][0:2]
                self.dosyamin = i[33:39][2:4]
                self.dosyas = i[33:39][4:6]
                self.dosyadate = self.dosyah + ":" + self.dosyamin + ":" + self.dosyas
                self.dosyainfo  =  "Dosya No : " + str(self.cout) + "  Saat : "+self.dosyah +":"+self.dosyamin+":"+self.dosyas
                print(self.dosyainfo,"\n")
        self.secim = int(input("Hangi dosyayi istiyorsunuz ?\n"))
        self.dosya = self.files[self.secim-1]
        os.chdir(self.defaultpath)
        
    def check(self,x):
        c = 0
        b = list(x)
        
        vflag = False
        cflag = False
        sflag = False
        self.flag = False
        
        for i in b[::-1]:
            c+=1
            if i == "v":
                vflag = True
            if i == "s" :
                sflag = True
            if i == "c":
                cflag = True
            if c == 3 and vflag and sflag and cflag:
                self.flag = True
                break
    

        

#yenisorgu = sorgu()

#yeni = dosya_aktar(yenisorgu.dosya,yenisorgu.dosya_yolu)

