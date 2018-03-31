import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.output(27,GPIO.LOW)      #rote LED ist aus
GPIO.output(15,GPIO.HIGH)       #gruene LED ist an
GPIO.setup(26,GPIO.OUT)
GPIO.output(26,GPIO.LOW)   #Relais bestromt das andere!
GPIO.setup(19,GPIO.OUT) 
GPIO.output(19,GPIO.HIGH)  #Motor oeffnet
time.sleep(20)
GPIO.output(26,GPIO.HIGH)   #Relais hoert auf zu bestromen
GPIO.output(19,GPIO.HIGH)   #Sicherstellen, dass das Motorrelais high ist	
