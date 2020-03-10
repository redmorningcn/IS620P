#IS620 电机速度控制
#
#包：
#
#方法：

from MdMaster import *  

		
ADDR_MOD_SET		            = 0x0200            # 地址：0-速度模式；1-位置模式；2转矩模式 	 	*/
MOD_SPEED                        = 0                    #速度模式

ADDR_SPEED_CODE_SOURCE  = 0x0602            #速度指令来源：0，主速度指令A；1，辅助速度指令B；2，A+B；3，A|B；4，通讯给定
#SPEED_COM_SET                 = 4                    #速度值，串口通讯给定
SPEED_COM_SET                 = 0                    #速度值，串口通讯给定  0603给定

ADDR_SPEED_ADD_TIME        = 0x0605            #加速度时间地址
SPEED_ADD_TIME                 = 10000             #加速时间10s

ADDR_SPEED_REDUCE_TIME   = 0x0606            #减速时间地址
SPEED_REDUCE_TIME            = 10000             #减速时间10s

ADDR_SPEED_READ               = 0x0B00            #读取速度值

#ADDR_SPEED_SET                = 0x3109            #通讯给定速度的地址
ADDR_SPEED_SET                = 0x0603            #通讯给定速度的地址

def initIs620(master, node):
    master.RegWr(node,ADDR_MOD_SET,MOD_SPEED)                           #选择速度模式
    master.RegWr(node,ADDR_SPEED_CODE_SOURCE, SPEED_COM_SET)   #通过串口设置速度
    
    #速度加减变化时间
    master.RegWr(node,ADDR_SPEED_ADD_TIME, SPEED_ADD_TIME)
    master.RegWr(node, ADDR_SPEED_REDUCE_TIME, SPEED_REDUCE_TIME)
    

def setSpeed(master,node,speed):
   master.RegWr(node, ADDR_SPEED_SET, speed)                                #设置转速
   
def getSpeed(master,node):
    speed = master.RegsRd(node, ADDR_SPEED_READ, 1)                                #设置转速
    return speed
   
if  __name__ == "__main__":
    port = "COM4"
    baud = 57600
    node = 1
    ser       =  MdMaster(port,baud)                      #创建切换装置对象
    number = 1
    initIs620(ser, node)
    
    while True:
        print(getSpeed(ser, node))
        print("请输入设置转速值：")
        speed = int(input())
        setSpeed(ser, node, speed)

    
