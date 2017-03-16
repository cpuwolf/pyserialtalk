# -*- coding: utf-8 -*-
"""
Created on Thu March 16 2017

@author: Wei Shuai <cpuwolf@gmail.com>
"""

import re
import time

from serialtalk.pyserialtalkwin import PySerialTalkWin

class myATCommandclass():
    
    winser = None
    SerData = ""
    
    def __init__(self):
        
        self.winser = PySerialTalkWin("acm2", self.SerialReadCallBack)

        self.winser.send('at\r') 
        self.winser.read()
        
        self.winser.send('at\r') 
        self.winser.read()
        
        print "you have only 8 seconds"
        time.sleep(8)
        
        self.winser.close()
    
    def SerialReadCallBack(self, c, rxqueue):
        self.SerData += c
                        
        if(re.search("OK", self.SerData)):
            print self.SerData        
            rxqueue.put(self.SerData)
            self.SerData = ""
        elif(re.search("ERR", self.SerData)):
            print self.SerData
            rxqueue.put(self.SerData)
            self.SerData = ""
    
myapp = myATCommandclass();
