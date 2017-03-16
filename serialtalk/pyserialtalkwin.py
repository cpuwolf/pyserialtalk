# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Thu March 16 2017

@author: Wei Shuai <cpuwolf@gmail.com>
"""

import re
import serial
import Queue

import pythoncom
import wmi

from .pyserialtalk import PySerialTalk
from .pyserialtalk import PySerialTalkReadThread

class PySerialTalkWin(PySerialTalk):
    
    def __init__(self, keyword, ReadCallback):
        """ Create the object """
        PySerialTalk.__init__(self, keyword, ReadCallback)

    def _scan_interface(self, keyword):
        pythoncom.CoInitialize()
        c = wmi.WMI()
        query = "SELECT * FROM Win32_PnPEntity WHERE Name LIKE '%(COM%)'"
        coms  = c.query(query)
    
        for com in coms:
            comnum =  re.search("\(COM([0-9]+)\)", com.Name)
            if(re.search(keyword, com.Name)):
                print ">>>" + com.Name
                return comnum.group(1)
        return
    
    def _connect(self):
        comidx = self._scan_interface(self._keyword) 
        if comidx == None:
            raise Exception("cannot find com port")
        
        try:
            self.cser = serial.Serial(int(comidx)-1, 115200, timeout=1)
        except:
            print("cannot open serial port")
            raise Exception("Could not open serial port")
        
        self.in_queue = Queue.Queue()
        self._thread = PySerialTalkReadThread(self.cser, self.in_queue, self._read_callback)
        self._thread.start()  
        