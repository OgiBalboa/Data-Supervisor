
import os
import sys
import time

os.chdir("Datas")

date = "2019-02-07"
os.chdir(date)
class dosyabul():
    def __init__(self,):
        global b
        global dosya #Dosya listesi
        global temp  # Dosyaların sayısını geçiçi olarak tutan değişken
        dosya = os.listdir()
        temp = len(dosya)
        time.sleep(1)
        dosya = os.listdir()
        print("Check")
        if len(dosya) > temp:  # DOSYA EKLENDİĞİNDE UYARI
            print("DOSYA EKLENDI !")

