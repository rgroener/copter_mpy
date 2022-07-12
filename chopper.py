'''
Copter
A simple helicopter game to test and use TTGO T Display board.

GRN Juni 2022

'''

from machine import Pin, Timer
import st7789
import tft_config
import vga1_bold_16x32 as font
import time
import copter_bitmaps

tft = tft_config.config(0, options=st7789.WRAP_V)

#global variables
fuel=10
tick_fuel=0
fuelbarlen=100
flag_vpos=0
counter=0
vpos=0
ms100=0
sec=0
vspeed=2
vspeedsetting=vspeed
vspeedtop=3
fuelburn=2
fuelburnsetting=fuelburn
gravity=2#value > 0 falling, value < 0 lifting
tastflag=0


fuelgradient=[0xf825,0xe0e5,0xc9c4,0xaaa4,0x9383,0x7c63,0x6523,0x4e02,0x36e2,0x1fc1,0x1fc1,0x1fc1,0x1fc1]
isr_tick=0

def ISR_T0(t):
    #introducing global variables
    global isr_tick
    isr_tick=1
   
#initialise timer 0
tim0=Timer(0)
tim0.init(period=50,callback=ISR_T0)

#initialise I/O Pins
PL=Pin(35,Pin.IN,Pin.PULL_UP)#switch right
PR=Pin(0,Pin.IN,Pin.PULL_UP)#switch left
led=Pin(2,Pin.OUT)#LED

def draw_copter(lift,gravity):
    global vpos
    tft.fill_rect(50,vpos,32,16,st7789.BLACK)
    vpos += gravity + lift
    tft.bitmap(copter_bitmaps,50,vpos)
    
    
def fuelbar(fuel,autorot, autorotenergy):
    global fuelgradient
    step=12
    if autorot==1:
        for x in range (0,100):#check in 10 steps
            if int(autorotenergy/10) >= x:
                tft.fill_rect(0,120-(x*step),10,10,st7789.BLUE)#100%
            else:
                tft.fill_rect(0,120-(x*step),10,10,st7789.BLACK)                
    elif fuel==0:#draw black if fuel is zero
        tft.fill_rect(0,20,10,110,st7789.BLACK)
    else:
        for x in range (0,100):#check in 10 steps
            if int(fuel/10) >= x:
                tft.fill_rect(0,120-(x*step),10,10,fuelgradient[x])#100%
            else:
                tft.fill_rect(0,120-(x*step),10,10,st7789.BLACK)
    
        

    
def main():
    global tick_fuel
    global flag_vpos
    global fuel
    global vpos
    global vspeed
    global vspeedtop
    global vspeedsetting
    global fuelburn
    global fuelburnsetting
    global flag_fuel
    global flag_vpos
    global isr_tick
    global ms100
    global sec
    global gravity
    
    lift=0
    fuelburnmax=10
    tick_vpos=0
    tastflag=0
    liftmax=-5
    liftmin=2
    freefall=2
    tick_lag=0
    autorot=0#if out of fuel enter autorotation status
    autorotenergy=0


    tft.init()
    tft.fill(st7789.BLACK)
    tft.rotation(1)
    led.off()
       
    while True:
        #timer driven
        if isr_tick==1:
            isr_tick=0
            tick_fuel+=1
            tick_vpos+=1
            tick_lag+=1
            #check / decrement fuel
            fuelbar(fuel,autorot, autorotenergy)#draw fuelbar
         
            if fuel >= 0 and autorot==0:#normal operation on fuel
                autorot=0#normal operation autorotation flag off
                if tick_fuel > (20-fuelburn):
                    tick_fuel=0
                    fuel-=1
                #lag for power/lift reaction
                #increase tick_lag value to increase lag
                if tick_lag > 2:
                    tick_lag=0
                    if tastflag == 1:
                        tastflag=0
                        if lift > liftmax:
                            lift -= 1#lift copter
                    else:
                        if lift < liftmin:
                             lift +=1#
            else:#no fuel, autorotation on 
                autorot=1
                #lag for power/lift reaction
                #increase tick_lag value to increase lag
                if tick_lag > 4:
                    tick_lag=0
                    if tastflag == 1:
                        tastflag=0
                        if autorotenergy>0:
                            autorotenergy-=8
                        if lift > liftmax and autorotenergy > 0:
                            lift -= 1#lift copter
                        else:
                            if lift < liftmin:
                                lift +=1#accelerate falling
                        print(lift)   
                    else:
                        if lift < liftmin:
                            lift +=1#accelerate falling
                        if vpos < 118:#building up energy for autorotation
                            autorotenergy+=5

                
                
            #check / move vertical copter position
            if tick_vpos > 1:
                tick_vpos=0
                flag_vpos=0
                if vpos > 118:#copter on bottom of screen
                    vpos=118
                elif vpos < 0:#copter at top of screen
                    vpos=0
                draw_copter(lift, gravity)
           
        tft.text(font,str(autorotenergy), 80, 0, st7789.YELLOW, st7789.BLACK)#print cdl_open price
   
                
        if PR.value()==0:
            led.on()
            tastflag=1
            if fuelburn <= fuelburnmax:
                fuelburn+=5

        else:
            led.off()
            fuelburn=fuelburnsetting

            
          
            
            
            
            
            
            
main()


   
    
