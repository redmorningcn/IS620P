# -*- coding: utf-8 -*-

"""
Module implementing ui_speed.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5      import QtCore, QtGui, QtWidgets
from IS620       import initIs620, setSpeed, getSpeed
from Ui_motor   import Ui_Form
from MdMaster  import * 
import threading
import time

class ui_speed(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ui_speed, self).__init__(parent)
        self.setupUi(self)

        serlist = getSerList()                              #初始化可用串口清单
        self.cb_com.addItems(serlist)
        
        bundlist = ['57600', '9600', '19200', '115200']
        self.cb_bund.addItems(bundlist)               #波特率
     
        self.bt_setspeed.setEnabled(False)          #设置按键状态，关
        self.bt_min.setEnabled(False)               
        self.bt_max.setEnabled(False)
        
        
        self.ser = None                                     #通许串口，先定义
        self.serflg = 0
        self.threadflg = 0
        self.show()
        #t1 = threading.Thread(target = run_thread,args = (500,))
        self.thread1 = threading.Thread(target = self.showSpeed)

    def showSpeed(self):                                #显示速度值
        node = 1
        while True:
            time.sleep(1.5)
            try:
                if self.serflg: 
                    speed = getSpeed(self.ser, node)
                    val = speed[0] 
                    if  val > 0x8000:
                        val = 65536 - val
                        
                    self.ln_speed.display(val)
            except Exception as e:
                print("速度读取错误", e)
            
    @pyqtSlot()
    def on_bt_setspeed_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            node = 1
            self.speed = int(self.le_speed.text())           #取速度值
            
            setSpeed(self.ser, node, self.speed)
            
            print("speed:", self.speed )
        except Exception as e:
            print("速度值输入错误！", e)
            
        
        # TODO: not implemented yet
        #raise NotImplementedError
    
    @pyqtSlot()
    def on_bt_opencom_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            bund = self.cb_bund.currentText()           #
            port  = self.cb_com.currentText()            #
            node = 1
            if  self.serflg == 1:                                                  #串口已定义
                self.serflg   = 0
                self.ser.close()   
                #self.thread1.join()
                
            self.ser = MdMaster(port, bund) 
            if self.ser.serflg == 1:
                self.serflg = 1
                print('port,bund:', port, bund)
                
                initIs620(self.ser, node)
                
                self.bt_setspeed.setEnabled(True)
                self.bt_min.setEnabled(True)
                self.bt_max.setEnabled(True)
                if self.threadflg == 0:
                    self.thread1.setDaemon(True)
                    self.thread1.start()
                    self.threadflg = 1
        except Exception as e:
            QMessageBox.information(self, "提示", "您没有打开串口，串口打开错误！", QMessageBox.Yes)
            print("串口有误！", e)
        # TODO: not implemented yet
        #raise NotImplementedError
        
    @pyqtSlot()
    def on_bt_min_clicked(self):
        """
        Slot documentation goes here.
        """
        node = 1
        setSpeed(self.ser, node, 20)

        # TODO: not implemented yet
        #raise NotImplementedError
    
    @pyqtSlot()
    def on_bt_max_clicked(self):
        """
        Slot documentation goes here.
        """
        node = 1
        setSpeed(self.ser, node, 3000)
        # TODO: not implemented yet
        #raise NotImplementedError



import sys
if __name__ == "__main__":
#def  main():
    app = QtWidgets.QApplication(sys.argv)
    ui = ui_speed()
    sys.exit(app.exec_())
    #while True:
    #   pass
