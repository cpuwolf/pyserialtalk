# -*- coding: utf-8 -*-
"""
Created on Thu March 16 2017

@author: Wei Shuai <cpuwolf@gmail.com>
"""

import serial
import threading
import Queue

class PySerialTalk:
    
    def __init__(self, keyword, ReadCallback):
        """ Create the object """
        self.cser = None
        self.in_queue = None
        self._thread = None
        self._keyword = keyword
        self._read_callback = ReadCallback
        
        self._connect()
    
    def _scan_interface(self, keyword):
        """ scan intefaces """
    
    def _connect(self):
        try:
            self.cser = serial.Serial(self._keyword, 115200, timeout=1)
        except:
            print("Cannot Open Serial Port")
            raise Exception("Could not Open Serial Port")
        
        self.in_queue = Queue.Queue()
        self._thread = PySerialTalkReadThread(self.cser, self.in_queue, self._read_callback)
        self._thread.start()  
        
    def close(self):
        self._thread.stop()    
        if self.cser:
            self.cser.close()
            
    def send(self, data):
        self.cser.write(data)
    
    def read(self):
        return self.in_queue.get(True)
        

class PySerialTalkReadThread(threading.Thread):
    """
    Read thread of serial driver. """

    def __init__(self, cser, inQueue, ReadCallback):
        """ Create the object """
        threading.Thread.__init__(self)
        self.cser = cser
        self.in_queue = inQueue
        self.sp = False
        self.read_callback = ReadCallback
        

    def stop(self):
        """ Stop the thread """
        self.sp = True
        try:
            self.join()
        except Exception:
            pass

    def run(self):
        """ Run the receiver thread """
        
        while(True):
            if (self.sp):
                break
            try:
                # Blocking until serial port data available
                datatmp = self.cser.read(1)
                # test only
                if len(datatmp) > 0:
                    self.read_callback(datatmp, self.in_queue)
                #else:
                    # drop invalid package
                    #print("timeout")
            except Exception as e:
                import traceback
                print("Error communicating"
                                         " ,it has probably been unplugged!\n"
                                         "Exception:%s\n\n%s" % (e,
                                         traceback.format_exc()))
    
