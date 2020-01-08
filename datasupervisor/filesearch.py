#-------------------------------------------------
# Name:         Data Supervisor File Search Module
# Author :      ogulcan@AISIN
# Date :        13.12.2019
# Licence :     <GNU GCC>
#-------------------------------------------------
import os,glob
import sys
import time
from datetime import datetime, date
from settings import program_files,bug_report
program_files = program_files()
bug = bug_report()
class dosyabul():
    def __init__(self,):
        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        self.fileflag = None
        self.filedate = ""
        self.search_again = None 
        self.new_file_flag = None
        self.reftime = str(datetime.now()) # TARAMAYA BAŞLAMA ZAMANI
        self.data_name = None
        self.status = "Arama Komutu Oluşturuldu"
    def findate(self,):
        self.status = "Güncel Tarihli Dosya Aranıyor "
        try:
            os.chdir(str(datetime.now())[0:10])
            self.filedate = str(datetime.now())[0:10]
            self.fileflag = True
            self.status = "Yeni Veri Bekleniyor " + " "*55
            os.chdir(program_files.datas)
        except:
            try:
                os.mkdir(str(datetime.now())[0:10])
                self.fileflag = True
                self.filedate = str(datetime.now())[0:10]
            except :
                bug.report()
                time.sleep(1)
                os.chdir(program_files.datas)
                os.chdir(str(datetime.now())[0:10])
                self.fileflag = True
                self.filedate = str(datetime.now())[0:10]
    def detect_new(self,path):
        os.chdir(path)
        self.filecount = glob.glob("*.csv")
        self.filecount.sort(key = os.path.getmtime)
        self.temp_file_count = self.filecount
        while True:
            self.filecount = glob.glob("*.csv")
            self.filecount.sort(key = os.path.getmtime)
            if len(self.filecount) > len(self.temp_file_count):
                self.data_name = self.filecount[-1]
                self.data_path = os.getcwd()
                break
            self.check_time(self.reftime)
            if self.search_again == True :
                break
    def check_time(self,reftime):
        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        date2 = str(datetime.now())
        try:
            self.diff = datetime.strptime(date2, datetimeFormat)\
            - datetime.strptime(reftime, datetimeFormat)
        except:
            pass
        if self.diff.seconds > 10:
            self.reftime = str(datetime.now())
            if self.filedate != str(datetime.now())[0:10]:
                self.search_again = True
                self.status = "Yeni Tarih Aranıyor"
                print("yeni tarihe geçiliyor")
                os.chdir(program_files.datas)
                
                try:
                    os.mkdir(str(datetime.now())[0:10])
                except :
                    bug.report()
        else:
            self.search_again = False
        
#-------------------------------ESKİ VERSİYONDAN KALAN FONKSİYONLAR-------------------
    def previous_date(self,):
            self.current_date = list(str(datetime.now())[0:10]) 
            self.findfile()
            while self.fileflag == False :
                if int(self.current_date[-1]) == 0 and int(self.current_date[-2]) == 0:
                    if int(self.current_date[-4]) > 0 :
                        self.current_date[-4] = int(self.current_date[-4]) -1
                        self.current_date[-1] = 1
                        self.current_date[-2] = 3
                        self.findfile()
                    elif int(self.current_date[-4]) == 0:
                        self.current_date[-4] = 9
                        self.current_date[-5] = int(self.current_date[-5]) - 1
                        self.current_date[-1] = 1
                        self.current_date[-2] = 3                    
                        self.findfile()
                        
                if int(self.current_date[-1]) > 0:
                    self.current_date[-1] = int(self.current_date[-1]) - 1
                    self.findfile()
                elif int(self.current_date[-1]) ==0:
                    self.current_date[-1] = 9
                    self.current_date[-2] = int(self.current_date[-2]) - 1
                    self.findfile()
            
                if self.fileflag == True :      
                    self.filedate = self.tempname
                      
                    break
    def findfile(self,):
        dosya = os.listdir()
        self.tempname = ''.join(map(str,self.current_date)) #GEÇİCİ OLARAK TARİHİ DOSYA ADINA ÇEVİRİR
        for i in dosya:
            """
            if i == "Yeni klasör": 
                return self.findfile
            """
            if i == self.tempname and len(i) == 10:
                self.fileflag = True   
            else :
                self.fileflag = False
