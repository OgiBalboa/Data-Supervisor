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
import filesearch
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import math
import numpy as np
from settings import settings,program_files
settings = settings()
program_files = program_files()
class analiz():
    def __init__(self,isim,yol=None,aramaflag =None,noprint = None, date = None):
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
        self.peaklist1= [] 
        self.peaklist2= []
        self.aramaflag = aramaflag
        self.isim = isim
        self.error_info = "\n\nBULUNAN HATALAR \n"+"*"*60
        self.noprint = noprint
        self.errorflag = None
        self.peakhata = None
        try:
            os.chdir(yol)
        except:
            pass         
        if self.aramaflag == True:
            time.sleep(settings.wait_for_data) # DOSYA GELMESİNİ BEKLE
        #-------------------------------DOSYA AÇILIR------------------------------------------------------- 
        with open(isim,newline='') as file:
            spm = csv.reader(file,delimiter=' ',quotechar = '|')
            for self.r in spm:    # DATA İÇERİSİNDEKİ HER BİR VERİYİ DENETLER          
                self.veriayir()               
                self.vericount+=1
            #----------Veri Sayısına Göre Amplitude çarpanı değeri değişir--------
            if self.vericount <3001:
                self.gen1 = settings.amp
                self.gen2 = settings.amp
            elif self.vericount >3000:
                self.gen1 = settings.amp1
                self.gen2 = settings.amp1
            #------------- Sorgu Sırasında Terminale Bilgi Yazılıp yazılmayacağı noprint flagı ile belirlenir---------
            if self.errorflag == False and self.noprint != True :
                print("Basınç Bilgisi :\n")
                print("Basınç değerleri istenilen aralıkta ! ")
            elif self.errorflag == True and self.noprint != True:
                print("Basınç Bilgisi :\n")
                print("Hatalı basınç değeri tespit edildi ! ")
            try :
                self.denetle() #ALINAN VERİLERİ İNCELE
            except Exception as e:
                pass
            #-------------------------------PEAK SAYI HATALARI-------------------------------------------------------  
            self.peak_sayi_hatasi()
            #-------------------------------ENJEKSİYON SÜRE HATASI-------------------------------------------------------                  
            try:
                self.zaman_hatasi() # ZAMAN HATASINI DENETLEYEN FONKSİYON
            except Exception as e:
                pass
                self.errorflag = True
            try :
                self.info = "Veri Sayisi : " + str(self.vericount-8)+"\nSENSOR 1 ----> Peak Sayısı  :  " + str(self.peakcount1)
                self.info +="\nSENSOR 1 ----> Enjeksiyon Başlangıç Zamanı   :  " + str(self.peaklist1[0]) +"\nSENSOR 1 ---->  Enjeksiyon Süresi  :  " + self.enjeksiyon_suresi1 
            except:
                self.info += "\nSensör 1'de peak bulunamadı.\n"
            try:
                self.info +="\n\nSENSOR 2 ----> Peak Sayısı  :  " + str(self.peakcount2)
                self.info += "\nSENSOR 2 ----> Enjeksiyon Başlangıç Peak Time  :  " + str(self.peaklist2[0]) + "\nSENSOR 2 ----> Enjeksiyon Süresi :" + self.enjeksiyon_suresi2
            except:
                self.info +="\nSensör 2'de peak bulunamadı\n"              
            self.veri_sayisi = self.vericount-8
            #-------------------------------ANALİZ SONRASI SON İŞLEMLER-------------------------------------------------------   
            if self.aramaflag == True and self.errorflag == True: # ARAMA YAPILIYORSA VE HATA OLUŞMUŞSA HATAYI KAYDET
                self.hatakayit(date)
            os.chdir(program_files.main) # ANA DOSYA YOLUNA GERİ DÖN
            
            if self.noprint != True: # BİLGİ YAZILMASI İSTENİYORSA HATALARI TERMİNALE YAZ
                print(self.info)
                if self.aramaflag != True and self.errorflag == True:
                    print("\n"*3)
                    print(self.error_info)
                    print("*" * 50)
            file.close()
#-------------------------------VERİLERİ AYIRIP LİSTELERE EKLEMEK İÇİN FONKSİYON-------------------------------------------------------   
    def veriayir(self,):
            self.csv_time = self.r[0].split(',')   # SURE VERİSİNİ AYIRIR
            if self.vericount>6:  #ilk 6 veri info satırlarıdır
                self.csv_sensor2 = self.r[1].split(',')  #SENSOR 2 'nin verilerini ayırır
                self.surelist.append(str(self.csv_time[0]))
                self.sensor1.append(str(self.csv_time[1]))
                self.sensor2.append(str(self.csv_sensor2[0])) #VERİLERİ AYIRIP LİSTELERE KAYDEDER
    
#-------------------------------VERİLERİ İNCELE-------------------------------------------------------                   
    def denetle(self,):
            count1 = 0   # VERİ İÇERİSİNDE ALINACAK ÖRNEKLER İÇİN SAYICI VE BOŞ DİZİ TANIMLANIR
            count2 = 0
            sample1 = []
            sample2 = []
            for i in range (0,len(self.surelist)): # Zamanı teker teker arttırır.
                self.acibul1(i,self.gen1)
                self.acibul2(i,self.gen2) # açı hesaplama için zaman bilgisi girilir.
                self.peakdetect(i) # Hesaplanan açılar üzerinden peak denetlenir.
                self.basinchatadetect(i)
                if settings.sample_range_start < i < settings.sample_range_stop: # 0.06 ve 2. saniye arasındaki değerler örnek olarak alınır.
                    if count1<10: # ilk 10 veri hesaplanır.
                        if int(self.anglelist1[-1]) != 0:  # 0 değerlerini katma
                            sample1.append(abs(self.anglelist1[-1]))
                        count1+=1
                    if count2<10:
                        if int(self.anglelist2[-1]) != 0:
                            sample2.append(abs(self.anglelist2[-1]))
                        count2+=1
                    try :
                        if count1 == 10 and settings.min_angle < self.mean(sample1) < settings.max_angle:#Settings dosyasından alınan veriye göre açı değerini istenilen aralığa
                            if int(self.anglelist1[-1]) >=settings.min_angle:
                                self.gen1 += settings.inc_amp                                            #çekebilmek için genliği arttırır.
                                count1 = 0
                        if count2 == 10 and settings.min_angle < self.mean(sample2) < settings.max_angle:
                            if int(self.anglelist1[-1]) >=settings.min_angle:
                                self.gen2 += settings.inc_amp
                                count2 = 0
                    except Exception as e:
                        print(e)
            self.enjeksiyon_suresi1 = str(self.peaklist1[-1]-self.peaklist1[0])
            self.enjeksiyon_suresi2 = str(self.peaklist2[-1]-self.peaklist2[0]) # Enjeksiyon süresi hesaplanır. (ilk ve son peak)
            
    def mean(self,liste): #ALINAN ÖRNEKLEMİN ORTALAMA DEĞERİNİ HESAPLAR
        toplam = 0
        for i in liste:
            toplam += i
        if toplam == 0:
            return 1
        else:
            return toplam/len(liste)
#-------------------------------PEAK BULMA-------------------------------------------------------     
    def peakdetect(self,i):
        
        if  len(self.peaklist1) <  1 and float(self.anglelist1[-1]) > settings.first_peak_value and float(self.sensor1[i+10])> 2: #Settings'den alınan veriye göre peak denetlenir.   
            self.peak1()
        elif len(self.peaklist1)  >= 1 and float(self.anglelist1[-1]) > settings.last_peak_value :
            self.peak1()
        if   len(self.peaklist2)  < 1 and float(self.anglelist2[-1]) > settings.first_peak_value and float(self.sensor2[i+10])> 2 :
            self.peak2()
        elif len(self.peaklist2)  >= 1 and float(self.anglelist2[-1]) > settings.last_peak_value :    
            self.peak2()

    def peak1(self,):
        
        self.peakno1 = len(self.anglelist1)-1
        self.reftime1 = float(str(self.surelist[self.peakno1]))
        if self.reftime1 < settings.wait_for_next_peak*2: # Başlangıçta bir süre peak algılama
            return None
        if len(self.peaklist1) >= 1 and  self.reftime1 - float(self.peaklist1[-1])  >= settings.wait_for_next_peak :
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
        if self.reftime2 < settings.wait_for_next_peak:
            return None        
        if len(self.peaklist2) >= 1 and self.reftime2 - float(self.peaklist2[-1]) >= settings.wait_for_next_peak :
                self.peaklist2.append(self.reftime2)
                self.peakcount2 += 1
        elif len(self.peaklist2) < 1 :
                self.peaklist2.append(self.reftime2)
                self.peakcount2 += 1
#-------------------------------HATA ARAMA VE KAYIT-------------------------------------------------------
    def zaman_hatasi(self,):
            if float(self.peaklist1[-1]-self.peaklist1[0]) < settings.min_enj_time or float(self.peaklist2[-1]-self.peaklist2[0] < settings.min_enj_time):
                    self.error_info += "\n\nHata Türü : Enjeksiyon Süre Hatası" 
                    if self.noprint != True:
                        print(self.error_info)
                        print("*" * 50)
                    self.errorflag = True
    def basinchatadetect(self,i):
            if float(self.sensor1[i]) > settings.max_pressure or float(self.sensor2[i]) > settings.max_pressure:     # HATALI DURUM KOŞULLARI
                self.error_info += "\n\nHata Türü : Sensör Basınç Hatası\n" + "Süre : "+ str(self.surelist[i]) + \
                                "\nSensör 1 Basınç Değeri (kPa): " + str(self.sensor1[i]) + \
                                "\nSensör 2 Basınç Değeri (kPa): " + str(self.sensor2[i]) 
                self.errorflag = True
                return
    def peak_sayi_hatasi(self,):
            if self.peakcount1 <settings.default_peak_count or self.peakcount2 < settings.default_peak_count:  # PEAK SAYISI DEFAULTTAN AZ İSE HATA BİLDİR
                if self.noprint != True:
                    print("\nHATA ! Sensörlerin birinde Peak az, Hata bulunmuş olabilir.")
                if self.peakhata != True:
                    self.error_info += "\n Hata Tipi : Sensör Peak Sayısı Hatası\n"
                    self.error_info += "\nTespit edilen Sensör 1 Peakler : "\
                           +str(self.peaklist1) + "\nTespit edilen Sensör 2 Peakler : " +str(self.peaklist2)
                self.errorflag = True
    def hatakayit(self,date):
            os.chdir(program_files.auto_errors)
            try:
                os.mkdir(date)
            except:
                pass
            finally:
                os.chdir(date)
            self.error_filename = "20" + self.isim[-17:-15] +"-"+ self.isim[-15:-13] +"-"+ self.isim[-13:-11] +"_" + self.isim[-11:-9] +"-"+ self.isim[-9:-7] +".txt"
            self.errorlog = open(self.error_filename,'a+')
            self.errorlog.write("\nOrijinal dosya adı :"+self.isim+"\n")
            self.errorlog.write(self.info)
            self.errorlog.write(self.error_info)
            self.errorlog.write('\n' + '*'*50 + '\n')
            self.errorlog.close()
  
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
                
    def acibul(self,x2,x1,t2,t1):  # Manuel olarak bir açı hesaplanmak istenirse bu fonksiyonu kullan.
                y = float(x2) - float(x1)
                x = 100*float(t2) - 100*float(t1)
                tan = y/x
                self.aci = math.degrees(math.atan(tan))
#-------------------------------GRAFİK ÇİZDİRME-------------------------------------------------------                         
    def plot (self,):
            def draw(name,ccolor,title,xlabel,ylabel,axisx,axisy):
                name.plot(axisx,axisy,color = ccolor)
                name.set_title(title)
                name.set_xlabel(xlabel)
                name.set_ylabel(ylabel)   
            fig,(sub1,sub3) = plt.subplots(2)
            fig,(sub2,sub4) = plt.subplots(2)
            draw(sub1,"darkred","SENSÖR 1","Süre(s)","Basınç(MPa)",self.surelist,self.sensor1)
            draw(sub2,'darkred',"SENSÖR 2","Süre(s)","Basınç(MPa)",self.surelist,self.sensor2)
            draw(sub3,'lightblue',"SENSRÖR 1 AÇILAR", "Süre (s)"," Açı (Derece)",self.surelist,self.anglelist1)
            draw(sub4,'lightblue',"SENSRÖR 2 AÇILAR", "Süre (s)"," Açı (Derece)",self.surelist,self.anglelist2)
            plt.show()
         
#-------------------------------DOSYALARI BULMA MODÜLÜ-------------------------------------------------------      
class sorgu():
    def __init__(self,):
        self.defaultpath = os.getcwd() #Default dosya yolu
        os.chdir(program_files.datas)
        self.temppath = os.getcwd()
        self.gui()
    def gui(self,):
        self.penc = Tk()
        self.penc.title("Veri Analiz")
        self.penc.geometry("450x300")
        try:
            self.penc.iconbitmap("bin/icon.ico")
        except:
            pass
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
            self.sorgu = "C:/Users/ITStaj/Desktop/datasupervisor/Datas/2019-12-09"
            self.penc.destroy()
            self.search()
        def cikis():
            self.iptal = True
            self.gunluk = False
            self.penc.destroy()
            os.chdir(program_files.main)
            
        Button(self.penc,text = "Tarih ile arama ",command = tarih).place(x = 60, y = 20)
        Button(self.penc,text = "Dosya Bul",command = askdir).place(x = 180, y = 20)
        Button(self.penc,text = " DENEME ",command = immediate).place(x = 300, y = 20)
        Button(self.penc,text = " MENÜYE DÖN ",command = cikis).place(x = 160, y = 120)

        self.penc.mainloop()
                
    def search(self,again = None):
        self.iptal = False
        os.chdir(program_files.datas)
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
        os.chdir(program_files.main)
    def go_to_date(name,date): # manuel olarak Datas içerisinde bir tarihe erişmek için kullanılır.name, yıl (son iki indisi) ay gün ve saat şeklinde bitişik olarak girilmelidir.(190702). Bunun için ayir fonksiyonu kullanılabilir.
        global check
        os.chdir(program_files.datas)
        os.chdir(date)
        dosyalar = os.listdir()
        for i in dosyalar:
             if name == i[-17:-7]:
                    dosya = i
                    return dosya
    def ayir(name,i = None): # manuel olarak veri adı ayrılmak istenirse bu fonksiyonu kullan.
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
                   
    def check(self,x): # csv dosya uzantısı kontrol 
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
