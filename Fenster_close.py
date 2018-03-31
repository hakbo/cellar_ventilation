import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.output(27,GPIO.HIGH)      #rote LED ist an
GPIO.output(15,GPIO.LOW)       #gruene LED ist aus
GPIO.setup(26,GPIO.OUT)
GPIO.output(26,GPIO.LOW)   #Relais bestromt das andere!
GPIO.setup(19,GPIO.OUT) 
GPIO.output(19,GPIO.LOW)  #Motor schliesst
time.sleep(20)
GPIO.output(26,GPIO.HIGH)   #Relais hoert auf zu bestromen
GPIO.output(19,GPIO.HIGH)   #Sicherstellen, dass das Motorrelais high ist   
