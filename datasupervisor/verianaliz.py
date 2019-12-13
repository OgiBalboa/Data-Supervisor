import csv
import os
import tkinter
from tkinter import Button
import time
from datetime import datetime
#-----------------------------------------------------
# Name:         Data Supervisor Data Analisys Module
# Author :      ogulcan@AISIN
# Date :        13.12.2019
# Licence :     <GNU GCC>
#-----------------------------------------------------

import matplotlib.pyplot as plt
#import filesearch
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import math
import numpy as np
from settings import settings
settings = settings()
class dosya_aktar():
    def __init__(self,isim,yol=None,flag =None,noprint = None):
        self.vericount = 0
        self.defaultpath = os.getcwd() #Default dosya yolu
        self.surelist = []
        self.sensor1 = []
        self.sensor2 = []
        self.anglelist1 = ["0"]
        self.anglelist2 = ["0"]
        self.peakcount1 = 0
        self.curtime1 = 0
        self.peakcount2 = 0
        self.curtime2 = 0
        self.peaklist1= [] # sonpeak =  peaklist[-1] - peaklist[-2]
        self.peaklist2= []
        self.aramaflag = flag
        self.isim = isim
        self.error_info = "\n\nBULUNAN HATALAR \n"+"*"*60
        self.noprint = noprint
        self.errorflag = None
        self.peakhata = None
        try:
            os.chdir(yol)
        except:
            print("dir hatası")
            print(os.getcwd())
#-------------------------------DOSYA AÇILIR-------------------------------------------------------                         
        if self.aramaflag == True:
            time.sleep(settings.wait_for_data)
        with open(isim,newline='') as file:
            spm = csv.reader(file,delimiter=' ',quotechar = '|')
            for self.r in spm:    # DATA İÇERİSİNDEKİ HER BİR VERİYİ DENETLER          
                self.veriayir()               
                self.vericount+=1
            self.gen1 = settings.amp
            self.gen2 = settings.amp
            if self.errorflag == False and self.aramaflag != True and self.noprint != True :
                print("Basınç Bilgisi :\n")
                print("Basınç değerleri istenilen aralıkta ! ")
            elif self.errorflag == True and self.aramaflag != True and self.noprint != True:
                print("Basınç Bilgisi :\n")
                print("Hatalı basınç değeri tespit edildi ! ")
            try :
                self.denetle() #ALINAN VERİLERİ İNCELE
            except Exception as e:
                print(e)
#-------------------------------PEAK SAYI HATALARI-------------------------------------------------------  
            if self.peakcount1>settings.default_peak_count or self.peakcount2>settings.default_peak_count:
                if self.noprint != True:
                    print("\nHATA ! Sensörlerin birinde Peak sayısı fazla, Hata bulunmuş olabilir.")
                self.error_info += "\n Hata Tipi : Sensör Peak Sayısı Hatası\n"
                self.error_info += "\nTespit edilen Sensör 1 Peakler : "\
                           +str(self.peaklist1) + "\nTespit edilen Sensör 2 Peakler : " +str(self.peaklist2)
                self.errorflag = True
                self.peakhata = True
            if self.peakcount1 <settings.default_peak_count or self.peakcount2 < settings.default_peak_count:
                if self.noprint != True:
                    print("\nHATA ! Sensörlerin birinde Peak az, Hata bulunmuş olabilir.")
                if self.peakhata != True:
                    self.error_info += "\n Hata Tipi : Sensör Peak Sayısı Hatası\n"
                    self.error_info += "\nTespit edilen Sensör 1 Peakler : "\
                           +str(self.peaklist1) + "\nTespit edilen Sensör 2 Peakler : " +str(self.peaklist2)
                self.errorflag = True
#-------------------------------ENJEKSİYON SÜRE HATASI-------------------------------------------------------                  
            try:
                self.zaman_hatasi()
            except Exception as e:
                if self.errorflag != True:
                    print(e)
                    self.inf = "Peak Bulunamadı"
                    print(self.inf)
                    print(self.peaklist1,self.peaklist2)
                    print(len(self.anglelist1),len(self.anglelist2))
                self.errorflag = True
            try :
                self.inf = "Veri Sayisi : " + str(self.vericount-8)+"\nSENSOR 1 ----> Peak Sayısı  :  " + str(self.peakcount1)
                self.inf +="\nSENSOR 1 ----> Enjeksiyon Başlangıç Zamanı   :  " + str(self.peaklist1[0]) +"\nSENSOR 1 ---->  Enjeksiyon Süresi  :  " + self.enjeksiyon_suresi1 
            except:
                self.inf += "\nSensör 1'de peak bulunamadı.\n"
            try:
                self.inf +="\n\nSENSOR 2 ----> Peak Sayısı  :  " + str(self.peakcount2)
                self.inf += "\nSENSOR 2 ----> Enjeksiyon Başlangıç Peak Time  :  " + str(self.peaklist2[0]) + "\nSENSOR 2 ----> Enjeksiyon Süresi :" + self.enjeksiyon_suresi2
            except:
                self.inf +="\nSensör 2'de peak bulunamadı\n"              
            self.veri_sayisi = self.vericount-8
            if self.aramaflag == True and self.errorflag == True:
                self.hatakayit()
            os.chdir(self.defaultpath) # ANA DOSYA YOLUNA GERİ DÖN 
            file.close()
    def veriayir(self,):
            self.a = self.r[0].split(',')   # SURE VERİSİNİ AYIRIR
            if self.vericount>6:  #ilk 6 veri info satırlarıdır
                self.b = self.r[1].split(',')  #SENSOR 2 'nin verilerini ayırır
                self.surelist.append(str(self.a[0]))
                self.sensor1.append(str(self.a[1]))
                self.sensor2.append(str(self.b[0])) #VERİLERİ AYIRIP LİSTELERE KAYDEDER
                self.basinchatadetect()
#-------------------------------VERİLERİ İNCELE-------------------------------------------------------                   
    def denetle(self,):
            count1 = 0   # VERİ İÇERİSİNDE ALINACAK ÖRNEKLER İÇİN SAYICI VE BOŞ DİZİ TANIMLANIR
            count2 = 0
            sample1 = []
            sample2 = []
            for i in range (0,len(self.surelist)):
                self.acibul1(i,self.gen1)
                self.acibul2(i,self.gen2)
                self.peakdetect()

                if 30 < i < 101: # 0.3 VE 1 ARASINDAKİ DEĞERLER
                    #print("girdim")
                    if count1<10:
                        if int(self.anglelist1[-1]) != 0:  # 0 değerlerini katma
                            sample1.append(abs(self.anglelist1[-1]))
                        count1+=1
                    if count2<10:
                        if int(self.anglelist2[-1]) != 0:
                            sample2.append(abs(self.anglelist2[-1]))
                        count2+=1
                    try :
                        if count1 == 10 and settings.min_angle < self.mean(sample1) < settings.max_angle:  # EĞER ALINAN ÖRNEKLERİN ORTALAMASI 13 İLE 20 ARASINDAYSA GENLİĞİ ARTTIRARAK BU DEĞERİ DÜŞÜRÜR
                            self.gen1 += 5
                            count1 = 0
                            #print("1.Genlik 5 arttı ! ")
                        if count2 == 10 and settings.min_angle < self.mean(sample2) < settings.max_angle:
                            self.gen2 += 5
                            count2 = 0
                            #print("2.Genlik 5 arttı ! ")
                    except Exception as e:
                        print(e)
            if len(self.peaklist1)== settings.default_peak_count:
                self.enjeksiyon_suresi1 = str(self.peaklist1[-1]-self.peaklist1[0])
            elif len(self.peaklist1) > settings.default_peak_count :
                self.enjeksiyon_suresi1 = str(self.peaklist1[-1]-self.peaklist1[0]) # PEAK SAYISI DEFAULTTAN FAZLA İSE İLK VE SONU AL !
                
            if len(self.peaklist2) == settings.default_peak_count:
                self.enjeksiyon_suresi2 = str(self.peaklist2[-1]-self.peaklist2[0])
            elif len(self.peaklist2) > settings.default_peak_count:
                self.enjeksiyon_suresi2 = str(self.peaklist2[-1]-self.peaklist2[0])
    def mean(self,liste):
        toplam = 0
        for i in liste:
            toplam += i
        if toplam == 0:
            return 1
        else:
            return toplam/len(liste)
#-------------------------------PEAK BULMA-------------------------------------------------------     
    def peakdetect(self,):
        
        if  len(self.peaklist1)   < 1 and float(self.anglelist1[-1]) > settings.first_peak_value:    
            self.peak1()
        elif len(self.peaklist1)  >= 1 and float(self.anglelist1[-1]) > settings.last_peak_value :
            self.peak1()
        if   len(self.peaklist2)  < 1 and float(self.anglelist2[-1]) > settings.first_peak_value :
            self.peak2()
        elif len(self.peaklist2)  >= 1 and float(self.anglelist2[-1]) > settings.last_peak_value :    
            self.peak2()

    def peak1(self,):
        
        self.peakno1 = len(self.anglelist1)-1
        self.reftime1 = float(str(self.surelist[self.peakno1]))
        self.pressure_time1 =float(str(self.reftime1)) - float(str(self.curtime1))
        if self.reftime1 < 1:
            return None
        if len(self.peaklist1) >= 1 and  self.reftime1 - float(self.peaklist1[-1])  >= 0.3 :
                self.peaklist1.append(self.reftime1)
                self.curtime1 = self.reftime1
                self.peakcount1 += 1
        elif len(self.peaklist1) < 1 :
                self.peaklist1.append(self.reftime1)
                self.curtime1 = self.reftime1
                self.peakcount1 += 1
        
    def peak2(self,):
        self.peakno2 = len(self.anglelist2)-1
        self.reftime2 = float(str(self.surelist[self.peakno2]))
        self.pressure_time2 =float(str(self.reftime2)) - float(str(self.curtime2))
        if self.reftime2 < 1:
            return None        
        if len(self.peaklist2) >= 1 and self.reftime2 - float(self.peaklist2[-1]) >= 0.3 :
                self.peaklist2.append(self.reftime2)
                self.curtime2 = self.reftime2
                self.peakcount2 += 1
        elif len(self.peaklist2) < 1 :
                self.peaklist2.append(self.reftime2)
                self.curtime2 = self.reftime2
                self.peakcount2 += 1

    def zaman_hatasi(self,):
            if float(self.peaklist1[1]-self.peaklist1[0]) < settings.min_enj_time or float(self.peaklist2[1]-self.peaklist2[0] < settings.min_enj_time):
                    self.error_info += "\n\nHata Türü : Enjeksiyon Süre Hatası" +"\nSENSOR 1 ----> Peak Sayısı  :  " + str(self.peakcount1) + \
                    "\nSENSOR 1 ----> Enjeksiyon Başlangıç Zamanı   :  " + str(self.peaklist1[0]) +"\nSENSOR 1 ---->  Enjeksiyon Süresi  :  "+ self.enjeksiyon_suresi1 + \
                    "\n\nSENSOR 2 ----> Peak Sayısı  :  " + str(self.peakcount2) + \
                    "\nSENSOR 2 ----> Enjeksiyon Başlangıç Peak Time  :  " + str(self.peaklist2[0]) + "\nSENSOR 2 ----> Enjeksiyon Süresi :" + self.enjeksiyon_suresi2
                    if self.noprint != True:
                        print(self.error_info)
                        print("*" * 50)
                    self.errorflag = True
            else:
                self.errorflag = False

    def basinchatadetect(self,):
            if self.vericount > 6:
                if float(self.b[0]) > settings.max_pressure or float(self.a[1]) > settings.max_pressure: # HATALI DURUM KOŞULLARI
                    self.error_info += "\n\nHata Türü : Sensör Basınç Hatası\n" + "Süre : "+ str(self.a[0]) + "\nSensör 1 Basınç Değeri (kPa): " + str(self.a[1]) + \
                                "\nSensör 2 Basınç Değeri (kPa): " + str(self.b[0]) 
                    if self.aramaflag != True:
                        if self.noprint != True:
                            print(self.error_info)
                            print("*" * 50)
                        self.errorflag = True
                        return
                    #self.hatakayit() #HATALI DURUMU BİR LOG DOSYASINA KAYDEDEN FONKSİYON
                    self.errorflag = True
                else :
                    self.errorflag = False

    def hatakayit(self,):
            os.chdir(self.defaultpath)
            try :
                os.chdir("Errors")
            except:
                os.chdir("..")
                os.chdir("..")
                os.chdir("Errors")
            self.filename = "20" + self.isim[-17:-15] +"-"+ self.isim[-15:-13] +"-"+ self.isim[-13:-11] +"_" + self.isim[-11:-9] +"-"+ self.isim[-9:-7] +".txt"
            self.errorlog = open(self.filename,'a+')
            self.errorlog.write(self.inf)
            self.errorlog.write(self.error_info)
            self.errorlog.write('\n' + '*'*50 + '\n')
            self.errorlog.close()
  
#-------------------------------GRAFİK ÇİZDİRME-------------------------------------------------------                         
    def plot (self,):  
            def draw(name,ccolor,title,xlabel,ylabel,axisx,axisy):
                name.plot(axisx,axisy,color = ccolor)
                name.set_title(title)
                name.set_xlabel(xlabel)
                name.set_ylabel(ylabel)
                
            fig,(sub1,sub3) = plt.subplots(2)
            fig,(sub2,sub4) = plt.subplots(2)
            #fig = plt.figure()
            #sub = fig.add_subplot(111)
            draw(sub1,"darkred","SENSÖR 1","Süre(ms)","Basınç(kPa)",self.surelist,self.sensor1)
            draw(sub2,'darkred',"SENSÖR 2","Süre(ms)","Basınç(kPa)",self.surelist,self.sensor2)
            draw(sub3,'lightblue',"SENSRÖR 1 AÇILAR", "Süre (ms)"," Açı (Derece)",self.surelist,self.anglelist1)
            draw(sub4,'lightblue',"SENSRÖR 2 AÇILAR", "Süre (ms)"," Açı (Derece)",self.surelist,self.anglelist2)
            plt.show()
#-------------------------------VERİLERİN AÇILARINI BULMAK-------------------------------------------------------       
    def acibul1(self,veri,gen):

            if veri < len(self.surelist)-1:
                self.y = float(self.sensor1[veri+1]) - float(self.sensor1[veri])
                self.x = gen*float(self.surelist[veri+1]) - gen*float(self.surelist[veri])
                self.tan = self.y / self.x
                self.angle = math.degrees(math.atan(self.tan))
                self.anglelist1.append(self.angle)
                
    def  acibul2(self,veri,gen):
            if veri < len(self.surelist)-1:
                self.y2 = float(self.sensor2[veri+1]) - float(self.sensor2[veri])
                self.x2 = gen*float(self.surelist[veri+1]) - gen*float(self.surelist[veri])
                self.tan2 = self.y2 / self.x2
                self.angle2 = math.degrees(math.atan(self.tan2))
                self.anglelist2.append(self.angle2)
                
    def acibul(self,x2,x1,t2,t1):
                y = float(x2) - float(x1)
                x = 100*float(t2) - 100*float(t1)
                tan = y/x
                self.aci = math.degrees(math.atan(tan))

        
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
            self.entr = Entry(self.penc,width = 13)
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
        def immediate():
            self.sorgu = "C:/Users/ITStaj/Desktop/datasupervisor/Datas/2019-02-07"
            self.penc.destroy()
            self.search()
        def cikis():
            self.iptal = True
            self.gunluk = False
            self.penc.destroy()
            os.chdir(self.defaultpath)
            
        Button(self.penc,text = "Tarih ile arama ",command = tarih).pack()
        Button(self.penc,text = "Dosya Bul",command = askdir).pack()
        Button(self.penc,text = " DENEME ",command = immediate).pack()
        Button(self.penc,text = " MENÜYE DÖN ",command = cikis).pack()

        self.penc.mainloop()
                
    def search(self,again = None):
        self.iptal = False
        try:
            os.chdir("Datas")
        except:
            pass
        
        try:
            #os.chdir(self.sorgu)
            pass
        except:
            #messagebox("HATA !", "Tarihi yanlis girdiniz ve ya o tarih de dosya bulunmamakta,tekrar deneyin. ")
            print(os.getcwd())
            print("hatali")
            self.gui()
            return None
        os.chdir(self.sorgu)
        self.dosya_yolu = os.getcwd()
        self.dosyalar = os.listdir()
        self.files = []
        self.cout = 0
        print("*"*52)
        print("Arama başlatılıyor..")
        time.sleep(0.5)
        try:
         for i in self.dosyalar:
            self.check(i)
            if self.flag:
                self.cout +=1
                self.files.append(i)
                self.dosyaid = i[-24:-18]
                self.dosyah = i[-11:-9]
                self.dosyamin = i[-9:-7]
                self.dosyas = i[-7:-5]
                self.dosyadate = self.dosyah + ":" + self.dosyamin + ":" + self.dosyas
                self.dosyainfo  =  "Dosya No : " + str(self.cout) + "  Saat : "+self.dosyah +":"+self.dosyamin+":"+self.dosyas
                if again != True:
                    print(self.dosyainfo,"\n")
         while 1:
            self.secim = input("Hangi dosyayi istiyorsunuz ?\n\n(Tümünü görmek için 'a' giriniz.)\n(Çıkmak için CTRL+C 'ye basın)\n")
            if self.secim == "a" or len(self.files)>= int(self.secim) > 0:
                break
            else :
                print("\n\n\n HATALI GİRDİNİZ. TEKRAR DENEYİN ! \n\n ")
        except KeyboardInterrupt:
            return
        if self.secim == "a":
            self.iptal = True
            self.gunluk = True
            pass
        else:
            self.gunluk = False
            self.dosya = self.files[int(self.secim)-1]
        os.chdir(self.defaultpath)
    def errorfile(name,path):
        global check
        try:
            os.chdir("Datas")
        except:
            os.chdir("..")
            try :
                os.chdir("Datas")
            except:
                os.chdir("..")
                os.chdir("Datas")
        os.chdir(path)
        dosyalar = os.listdir()
        for i in dosyalar:
             if name == i[-17:-7]:
                    dosya = i
                    return dosya
    def ayir(name,i = None):
           dosyaid = name[-24:-18]
           dosyah = name[-11:-9]
           dosyamin = name[-9:-7]
           dosyas = name[-7:-5]
           dosyadate = dosyah + ":" + dosyamin + ":" + dosyas
           if i == None:
               dosyainfo  =dosyah+"-"+dosyamin+"-"+dosyas
               return dosyainfo
           else :
               dosyainfo  =  "Dosya No : " + str(i+1) + "  Saat : "+dosyah +":"+dosyamin+":"+dosyas
               return dosyainfo
                   
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
        return self.flag
    
#yenisorgu = sorgu()

#yeni = dosya_aktar(yenisorgu.dosya,yenisorgu.dosya_yolu)
