#--------------------------------------------
# Name:         Data Supervisor Settings
# Author :      ogulcan@AISIN
# Date :        13.12.2019
# Licence :     <GNU GCC>
#--------------------------------------------
import os
import sys
from datetime import datetime
import linecache
class settings():
    def __init__(self,): 
        self.first_peak_value = 10          # İLK PEAK İÇİN MİN DEĞER ( Default = 14 degrees)

        self.last_peak_value = 20           # SON PEAK İÇİN MİN DEĞER ( Default = 20 degrees)

        self.min_enj_time = 5               # ENJEKSİYON SÜRESİ ( Default = 5 sec)

        self.max_pressure = 20              # MAX BASINÇ ( Default = 20 MPa)

        self.wait_for_data = 1              # Verinin oluşması için bekleme süresi (Default = 38 sec)

        self.min_angle = 10                 # ( Default = 10 degrees)

        self.max_angle = 20                 # Doğrultalacak olan veri için aralık belirtilir. ( Default = 20)

        self.amp = 20                       # 3000 ve aşağı sayıdaki veriler için genlik değeri ( Default = 20)

        self.inc_amp = 5                    # genlik değerinin makine tarafından birim arttırılma değeri
#------------------------------EK AYARLAR--------------------------------------
        self.wait_for_next_peak = 0.5         # Peak bulduktan sonra bekleme süresi(default = 1)

        self.amp1 = 100                     # 3000 den fazla veri sayısı için genlik değeri ( Default = 100)

        self.jump = 20                      # düzensiz veriler için atlanacak süre miktarı
                                            # ( Default = 20 *t. t, birim zamandır. veri sayısına göre değişir.)

        self.sample_range_start = 3         #Doğrultma için alınan örneğin başlama zamanı (30sn/veri sayısı)* range_start (Default :  1500 veri için 30. -0.06 . saniye-)

        self.sample_range_stop = 101        # Doğrultma bitiş zamanı ( Default : 1500 veri için 101 -2. saniye-)
        
        self.default_path = os.getcwd()     #Programın varsayılan çalışma dosyası.

        self.default_peak_count = 2         # Minimum peak sayısı

        self.process_time = 30              # Proses Süresi









#------------------------------PROGRAM İÇİ PARAMETRELER ( DOKUNMAYIN ! )--------------------------------------
        self.paralel_stop = None


#-------------------------------PROGRAMSAL HATA RAPORLAMA  ( DOKUNMAYIN ! ) ------------------

class bug_report():
    def __init__(self,):
        try:
            self.path = program_files()
        except :
            print("HATA ! PROGRAM FILES MODÜLÜ DOSYALARI OLUŞTURAMADI LÜTFEN MODÜLÜ KONTROL EDİNİZ !"),
            input("Çıkmak için Enter'a basın..")
            sys.exit()
    def report(self,):
        self.cur_path = os.getcwd()
        os.chdir(self.path.perrors)
        with open(str(datetime.now())[0:10]+".txt","+a") as errorlog:
            self.error = str(self.PrintException())
            errorlog.write(self.error)
            errorlog.write("\n"+"*"*100)
        os.chdir(self.cur_path)
    def PrintException(self,):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


#------------------------------PROGRAM DOSYA YOLLARINI TANITAN CLASS-------------------------------------
class program_files:
    def __init__(self,):
        self.main = os.getcwd()
        try:
            os.chdir("Datas")
        except:
            os.mkdir("Datas")
            os.chdir("Datas")
        self.datas = os.getcwd()
        os.chdir("..")
        try:
            os.chdir("Errors")
        except:
            os.mkdir("Errors")
            os.chdir("Errors")
            os.mkdir("Auto")
            os.mkdir("Manual")
        self.errors = os.getcwd()
        os.chdir("Auto")
        self.auto_errors = os.getcwd()
        os.chdir("..")
        os.chdir("Manual")
        self.manu_errors = os.getcwd()
        os.chdir(self.main)
        try:
            os.chdir("bin/Errors")
        except:
            os.mkdir("bin")
            os.chdir("bin")
            os.mkdir("Errors")
            os.chdir("Errors")
        self.perrors = os.getcwd()
        os.chdir(self.main)
            
