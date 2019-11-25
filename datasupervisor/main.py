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
global emp
emp = []
for i in range(0,50):
    emp.append(i)

global a
a = 0
def sorgular():
    global a
    global sorgu
    anayol = os.getcwd()
    if sorgu == 1:
        print("Dosya Kontrol")
        file = filesearch.dosyabul()
        file.findate()
        while 1:
            if len(file.data_name) > 1 :
                analiz = verianaliz.dosya_aktar(file.data_name,file.data_path)
                input("Enter")
                analiz.plot()
                break
        os.chdir(anayol)
        Menu()
    elif sorgu == 2:
        emp[a] = verianaliz.sorgu()
        b = verianaliz.dosya_aktar(emp[a].dosya,emp[a].dosya_yolu)
        input('Grafiği görmek için Enterla')
        b.plot()
        print("Sorgu tamamlandı.\n")
        a+=1
        line(52)
        gir = int(input("1. Aynı dosyadan başka sorgu \n2.Farklı Tarihe git\n3.Ana Menü\n"))

        if gir == 1:
            
            emp[a-1].search()
            gir = int(input("1. Aynı dosyadan başka sorgu \n2.Farklı Tarihe git\n3.Ana Menü\n"))
            sorgu = 2
            sorgular()
            
        if gir == 2:
            
            emp[a] = verianaliz.sorgu()
            verianaliz.dosya_aktar(emp[a].dosya,emp[a].dosya_yolu)
            gir = int(input("1. Aynı dosyadan başka sorgu \n2.Farklı Tarihe git\n3.Ana Menü\n"))
            wt()
            sorgu = 2
            sorgular()
            
        if gir == 3:
            Menu()        
        Menu()
        
    elif sorgu == 3:
        print("Error Logları : \n")
        anlik = os.getcwd()
        os.chdir('Errors')
        hatalar = os.listdir()
        cout = 0
        for i in hatalar:
            cout+=1
            print("Dosya No  :" + str(cout) + "  Dosya Adı : "+ i)
            print('\n')
        goruntule = int(input("Görüntülemek istediğiniz dosya No : "))
        dosya = open(hatalar[goruntule - 1],'r')
        print(dosya.read())
        os.chdir(anlik)
        input("Devam etmek için ENTER'a basın")
        Menu()

def Menu():
    
    menu = Tk()
    menu.title("MENU")
    menu.geometry("400x400")
    
    def sorgu1():
        global sorgu
        sorgu = 1
        menu.destroy()
        sorgular()
    def sorgu2():
        global sorgu
        sorgu = 2
        menu.destroy()
        sorgular()
    def sorgu3():
        global sorgu
        sorgu = 3
        menu.destroy()
        sorgular()
    Label (menu,text = "Ne Yapmak İstiyorsunuz ?",font=("Arial",14)).pack()
    Button(menu,text = "Makine ile Paralel Çalışma",font=("Arial",12),command = sorgu1).pack()
    Button(menu,text = "Makine Verileri Sorgula",font = ("Arial",12),command = sorgu2).pack()
    Button(menu,text = "Hataları Görüntüle",font = ("Arial",12),command = sorgu3).pack()

    line(52)
    menu.mainloop()
    
Menu()


