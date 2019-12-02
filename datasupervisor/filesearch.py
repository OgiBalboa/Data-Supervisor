import os
import sys
import time
from datetime import datetime
class dosyabul():
    def __init__(self,):

        self.fileflag = None
        self.filename = ""
        try: 
            os.chdir ( "Datas")
        except:
            pass
        self.data_name = None
    def findate(self,):
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
                self.filename = self.tempname    
                
                
                break

    def findfile(self,):
        dosya = os.listdir()
        self.tempname = ''.join(map(str,self.current_date)) #GEÇİCİ OLARAK TARİHİ DOSYA ADINA ÇEVİRİR
        for i in dosya:
            if i == self.tempname:
                self.fileflag = True
            else :
                self.fileflag = False
    def detect_new(self,path):
        os.chdir(path)
        self.filecount = os.listdir()
        self.temp_file_count = self.filecount
        while 1:
            self.filecount = os.listdir()
            if len(self.filecount) > len(self.temp_file_count):
                self.data_name = self.filecount[-1]
                self.data_path = os.getcwd()
                break
