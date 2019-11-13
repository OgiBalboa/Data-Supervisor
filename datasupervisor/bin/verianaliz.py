
import csv
import os
import tkinter
from tkinter import Button
import time
from datetime import datetime
#import filesearch
class dosya_aktar():
    def __init__(self,isim,yol=None):
        i = 0
        self.defaultpath = os.getcwd() #Default dosya yolu
        try:
            os.chdir(yol)
        except:
            print("dir hatası")
        
        with open(isim,newline='') as file:
            spm = csv.reader(file,delimiter=' ',quotechar = '|')
            for r in spm:
                    a = r[0].split(',')
                    try:
                        if i>6:
                            b = r[1].split(',')                       
                            if int(b[0]) > 15 or int(a[1]) > 15:
                                self.info = "Süre : "+ str(a[0]) + "\nSensör 1: " + str(a[1]) + "\nSensör 2 : " + str(b[0]) 
                                print(self.info)
                                print("*" * 50)
                                self.hatakayit()
                    except :
                        pass

                    i+=1
            inf = "Veri Sayisi : " + str(i)
            self.veri_sayisi = i
            os.chdir(self.defaultpath)
            print(inf) 
    def hatakayit(self,):
            os.chdir(self.defaultpath)
            os.chdir("Errors")
            self.filename  = str(datetime.now())[0:10] + "_"+str(datetime.now())[11:16]+".txt"
            self.errorlog = open(self.filename,'a+')
            self.errorlog.write(self.info)
            self.errorlog.write('\n' + '*'*50 + '\n')
            self.errorlog.close()
                       
            


class sorgu():
    def __init__(self,):
        self.defaultpath = os.getcwd() #Default dosya yolu
        self.sorgu = input(" Tarih giriniz (YIL-AY-GUN seklinde)")
        self.search()
    def search(self,):
        os.chdir("Datas")
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

"""
gui = tkinter.Tk()
gui.title('MERHABA')
gui.geometry('700x700')

def bos():
    pass
Button(gui,text = "HATA RAPORLA",command = bos).pack()
gui.mainloop()
"""
