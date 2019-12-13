#--------------------------------------------
# Name:         Data Supervisor Settings
# Author :      ogulcan@AISIN
# Date :        13.12.2019
# Licence :     <GNU GCC>
#--------------------------------------------
import os
class settings():
    def __init__(self,): # DEFAULT AYARLAR
        self.source_count = 2 # KAYNAK SAYISI
        self.first_peak_value = 14.5 # İLK PEAK İÇİN MİN DEĞER
        self.last_peak_value = 75 # SON PEAK İÇİN MİN DEĞER
        self.min_enj_time = 5 # ENJEKSİYON SÜRESİ
        self.max_pressure = 20 # MAX BASINÇ
        self.default_peak_count = 2 # DEFAULT PAEK SAYISI
        self.default_path = os.getcwd()
        self.wait_for_data = 1 #Verinin oluşması için bekleme süresi
        self.min_angle = 14.5
        self.amp = 20 # Açı hesaplamada zaman verisini genişletme değeri

        
    def gotofile(self,filename):  # PROGRAMIN DOSYALAR ARASINDA DOLAŞMASI İÇİN FONKSİYON
        os.chdir(os.getcwd)
        if filename == Datas:
            try:
                os.chdir("Datas")
                self.path = os.getcwd()
            except Exception as e: #BU KOD SAYESİNDE HATA ALIRSA PROGRAM DURMAZ.
                print("HATA ! : ",e)
        if filename == Errors:
            try:
                os.chdir("Errors")
                self.path = os.getcwd()
            except Exception as e:
                print("HATA ! : ",e)
        if filename == Manual:
            try:
                os.chdir("Errors")
                os.chdir("Manual")
                self.path = os.getcwd()
            except Exception as e:
                print("HATA ! : ",e)        

