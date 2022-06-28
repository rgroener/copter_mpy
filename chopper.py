from machine import Pin, Timer
import st7789
import tft_config
import vga1_bold_16x32 as font
import time

tft = tft_config.config(0, options=st7789.WRAP_V)

#global variables
fuel=100
flag_fuel=0
fuelbarlen=100
flag_vpos=0
counter=0
vpos=0
ms100=0
sec=0
vspeed=2
vspeedsetting=vspeed
vspeedtop=5
fuelburn=2
fuelburnsetting=1
fuelgradient=[0xf825,0xe0e5,0xc9c4,0xaaa4,0x9383,0x7c63,0x6523,0x4e02,0x36e2,0x1fc1]




def ISR_T0(t):
    #introducing global variables
    global flag_fuel
    global flag_vpos
    global ms100
    global sec
    if ms100<=10:#every 100ms
        ms100+=1
        flag_fuel=1
        flag_vpos=1
    else:
        ms100=0
        
  
#initialise timer 0
tim0=Timer(0)
tim0.init(period=100,callback=ISR_T0)


#initialise I/O Pins
PL=Pin(35,Pin.IN,Pin.PULL_UP)#switch right
PR=Pin(0,Pin.IN,Pin.PULL_UP)#switch left
led=Pin(2,Pin.OUT)#LED

def draw_copter(vspeed):
    global vpos
    tft.fill_rect(50,vpos,32,16,st7789.BLACK)
    vpos+=vspeed
    tft.fill_rect(50,vpos,32,16,st7789.YELLOW)
    
def fuelbar(fuel):
    step=12
    for x in range (0,100):#check in 10 steps
        print(str(fuel)+'\t'+str(x))
        if int(fuel/10) >= x:
            tft.fill_rect(0,120-(x*step),10,10,fuelgradient[x])#100%
        else:
            tft.fill_rect(0,120-(x*step),10,10,st7789.BLACK)#100%
        if fuel==0:
            tft.fill_rect(0,120-(x*step),10,10,st7789.BLACK)#100%
    
        

    
def main():
    global flag_fuel
    global flag_vpos
    global fuel
    global vpos
    global vspeed
    global vspeedtop
    global vspeedsetting
    global fuelburn
    global fuelburnsetting
    t_ms100=0
    t_sec=0
    t_min=0
    
    tft.init()
    tft.fill(st7789.BLACK)
    tft.rotation(1)
    led.off()
    
    
    while True:
        #timer driven
        if flag_fuel==1:
            flag_fuel=0
            if fuel >=1:
                fuel-=1
            
        if flag_vpos==1:#only draw if position changed
            flag_vpos=0
            if vpos<=118:
                draw_copter(vspeed)
              
                
        if PR.value()==0:
            led.on()
            vspeed = -2#lift copter
            fuelburn = +1
        else:
            led.off()
            vspeed = vspeedsetting
            fuelburn = fuelburnsetting
            
        fuelbar(fuel)   
            
            
            
            
            
            
main()


   
    
