import csv
i = 0
with open("a.csv",newline='') as file:
            spm = csv.reader(file,delimiter=' ',quotechar = '|')
            for r in spm:                 # DATA İÇERİSİNDEKİ HER BİR VERİYİ DENETLER
                    a = r[0].split(',')   # SURE VERİSİNİ AYIRIR
                    rewrite = csv.writer(a,delimeter=' ', quotechar = '|',quoting = csv.MINIMAL)
                    rewrite.writerow(
                    try:
                        if i>6:  #ilk 6 veri info satırlarıdır
                            
                            r[2] = "90"
                    
                            """
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

                            """
                    except :
                        pass
                    i+=1
            print(r[0])
            print(r[1])
            print(r)
                    


