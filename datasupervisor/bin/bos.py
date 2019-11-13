import time
from datetime import datetime
"""
errorlog = open(str(time.localtime()),'r')
errorlog.write(info)
errorlog.close()
     """
filename  = str(datetime.now())[0:10] + "_"+str(datetime.now())[11:16]
print(filename)

