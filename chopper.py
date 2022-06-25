from machine import Pin, Timer

#global variables
fuel=100
counter=0



def ISR_T0(t):
    #introducing global variables
    global fuel
    if fuel != 0:
        fuel-=1
    print(fuel)


#initialise timer 0
tim0=Timer(0)
tim0.init(period=200,callback=ISR_T0)


#initialise I/O Pins
PL=Pin(35,Pin.IN,Pin.PULL_UP)#switch right
PR=Pin(0,Pin.IN,Pin.PULL_UP)#switch left
led=Pin(2,Pin.OUT)#LED


def main():
    led.off()
    while True:
        if PR.value():
            led.on()
        else:
            led.off()
main()


   
    
