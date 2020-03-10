'''
作者：redmorningcn  20.02.29

模块：MdMaster (初始化:port,bount)
方法：CoilsRd  :读线圈，参数(node,addr,num),返回读取值list
方法：RegsRd   :读寄存器，参数(node,addr,num),发回读取值list
方法：CoilsWr  :写线圈，参数(node,addr,val),其中val为列表，值需为0或1
方法：RegsWr   :写寄存器，参数(node,addr,val),其中val为列表
方法：RegWr(self,node,addr,val)，val为short类型
'''
import  serial
import  modbus_tk
import  modbus_tk.defines    as         cst
from    modbus_tk               import      modbus_rtu
import serial.tools.list_ports

def getSerList():
    port_list = list(serial.tools.list_ports.comports())
    serlist = []
    if len(port_list) == 0:
        print('无可用串口')
    else:
         for i in range(0,len(port_list)):
            serlist.append(port_list[i][0])
    return serlist


class   MdMaster():
    #rbuf = []
    def __init__(self,port,baund=9600):
        try:
            self.com = serial.Serial(port=port,baudrate=baund)
            self.serflg = 0
            self.ser  = modbus_rtu.RtuMaster(self.com)  #创建modbus主机
            self.serflg = 1
            self.ser.set_timeout(1.0)   #设置超时
            self.ser.set_verbose(True)  # ??
        except Exception as e:
            print("---modbus串口打开异常---：", e)

    def CoilsRd(self,node,addr,num):        #MBM_FC01_CoilRd        读线圈
        rbuf = []
        try:
            rbuf = self.ser.execute(node, cst.READ_HOLDING_REGISTERS, addr, num)
        except Exception as e:
            print("---CoilsRd异常---：", e)
        return rbuf
    
    def RegsRd(self,node,addr,num):          #MBM_FC03_HoldingRegRd 读寄存器
        rbuf = []
        try:
            rbuf = self.ser.execute(node, cst.READ_HOLDING_REGISTERS, addr, num)
        except Exception as e:
            print("---RegsRd异常---：", e)
        return rbuf
    

    def CoilsWr(self,node,addr,val):         #MBM_FC15_CoilWr       写线圈
        try:
            self.ser.execute(node, cst.WRITE_MULTIPLE_COILS, addr,output_value=val)
        except Exception as e:
            try:
                self.ser.execute(node, cst.WRITE_MULTIPLE_COILS, addr,output_value=val)
            except:
                print("---CoilsWr异常---：", e)

    def RegWr(self,node,addr,val):
        try:
            self.ser.execute(node, cst.WRITE_SINGLE_REGISTER, addr,output_value=val)
        except Exception as e:
            try:
                self.ser.execute(node, cst.WRITE_SINGLE_REGISTER, addr,output_value=val)
            except:
                print("---RegRd异常---：", e)
        
    def RegsWr(self,node,addr,val):         #MBM_FC16_HoldingRegWrN 写寄存器
        try:
            self.ser.execute(node, cst.WRITE_MULTIPLE_REGISTERS, addr,output_value=val)
        except Exception as e:
            try:
                self.ser.execute(node, cst.WRITE_MULTIPLE_REGISTERS, addr,output_value=val)
            except:
                print("---RegsWr异常---：", e)

    def close(self):
        self.com.close()
        # 读保持寄存器
        #red = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 9)  # 这里可以修改需要读取的功能码
        #print(red)

        #send some queries
        #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))



import  time
from    ctypes import *
if  __name__ == "__main__":

    serialPort  = "COM5"                                                #串口
    baudRate    =  57600  
    master = MdMaster(serialPort,baudRate)

    node = 1
    addr = 0
#val  = (5,2,3,4)
    val = (c_uint32 * 5)(1,1,1,0,1)
    lenth = len(val)
    print(lenth,sizeof(val),val)
    while True:
        time.sleep(2)
        print("add,val")
        addr = int(input())
        val  = int(input())
        master.RegWr(node,addr,val)
        print(master.RegsRd(node, addr, 1))
    #master.CoilsWr(node,addr,val)


    




