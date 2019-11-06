# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 23:37:45 2019

@author: fener_000
"""
from PIL import Image,ImageTk
class resim():
    def __init__(self,path):
        self.pic = Image.open(str(path))  
        self.render = ImageTk.PhotoImage(self.pic)