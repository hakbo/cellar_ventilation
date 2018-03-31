GPIO.output(26,GPIO.LOW)   #Relais bestromt das andere!
GPIO.setup(19,GPIO.OUT) 
GPIO.output(19,GPIO.HIGH)  #Motor öffnet
time.sleep(20)
GPIO.output(26,GPIO.HIGH)   #Relais hört auf zu bestromen
GPIO.output(19,GPIO.HIGH)   #Sicherstellen, dass das Motorrelais high ist	
