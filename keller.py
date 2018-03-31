import Adafruit_DHT
import time
import mail # für das versenden von mail funktion "mail.send(daten als string)"
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)            #kann muss aber nicht, um warnung aus zu blenden

###Festlegen der Konstanten
R=8314.3 #Gaskonstante
mw=18.016 #molare masse wasser
#Ti=17 #Temperatur innen
#rFi=80 #relative Feuchte innen
#Ta=25 #Temperatur außen
#rFa=99 #relative Feuchte außen

###Definition der Funktionen
def rF(gpio):
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    time.sleep(2)
    while humidity>100:
        time.sleep(2)
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    return humidity

def T(gpio):
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    time.sleep(2)
    while humidity>100:
        time.sleep(2)
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    return temperature

def aF(T,rF):
    if T>=0:
        a, b=7.5, 237.3
    else:
        a, b=7.6, 240.7
    TK=T+273.15
    return 10**5*mw/R/TK*rF/100*6.1078*10**((a*T)/(b+T))  #g/m^3 Luft

def FensterState(state):
	if (state == 0):
		res = "Fenster ist zu."
	elif (state == 1):
		res = "Fenster ist auf."
	else:
		res = "Fenster ist kaputt."
	return res

##def Luefternachlauf(sekunden):
##    GPIO.setup(15,GPIO.IN)
##    if GPIO.input(15)==GPIO.HIGH:             #hier wird geschaut ob der pin noch an war
##        return Fensterauf=0    #dann soll das fenster zu und
##        return time.sleep(sekunden)             #ein timer gesetzt werden
##        print("Nachlauf Lüfter beendet")	#dieser verzögert den nächsten schritt
###       GPIO.output(x, GPIO.LOW)   #danach dann soll ein ventilator ausgehen
##    else:
##        Fensterauf=0

###Setzen des Startwerts
#Fensterauf=0
GPIO.setup(15,GPIO.IN)
Fensterauf = GPIO.input(15)
Fensterwar = GPIO.input(15)

###Auslesen der Messwerte
Ti=T(4)
Ta=T(10)
rFi=rF(4)
rFa=rF(10)

###Definition der absoluten Feuchte
aFi=aF(Ti,rFi)
aFa=aF(Ta,rFa)

###Entscheidung ob lüften oder nicht
if aFi-aFa<= 0.3:
    Fensterauf=0

elif rFi<=50:
    Fensterauf=0

elif aFi-aFa>= 1:
    if Ti<=14:
        if Ti-Ta<=0:
               Fensterauf=0
        else:
    		Fensterauf=1
	else:
		Fensterauf=1

else:                                 #nehme an wenn kein else steht heißt das soviel wie: wenn dies dann das sonst tue nichts
    time.sleep(0.1)
#    print ("hysterese;keine Änderung bis zum Schwellwert")

###Ausgabe und Loggen der Daten
#print(aFi,aFa,(aFi-aFa))
data = [Ti, rFi, aFi, Ta, rFa, aFa]
stringData = list(map(lambda x: ("%.1f" % x).replace('.',','), data))
stringTime = [time.strftime("%d.%m.%Y %H:%M")]
stringState = [FensterState(Fensterauf)]
formatedData = ';'.join(stringTime+stringData+stringState)

GPIO.setup(15,GPIO.OUT)             #grüne LED
GPIO.setup(27,GPIO.OUT)             #rote LED
GPIO.setup(26,GPIO.OUT)             #Relais zum Bestromen
#GPIO.setup(19,GPIO.OUT)             #Relais für die Richtungswahl öffnen oder schließen
if Fensterauf==1:
    GPIO.output(15, GPIO.HIGH)      #grüne LED ist an
    GPIO.output(27, GPIO.LOW)       #rote LED ist aus
    if Fensterauf-Fensterwar==0:     #dann ist keine Änderung nötig
        GPIO.output(26,GPIO.HIGH)  #kein Strom zum Betreiben des Motors
    elif Fensterauf-Fensterwar>0:   #dann war das Fenster geschlossen und muss geöffnet werden
        mail.send(formatedData)
        GPIO.output(26,GPIO.LOW)   #Relais bestromt das andere!
        GPIO.setup(19,GPIO.OUT)
        GPIO.output(19,GPIO.HIGH)  #Motor öffnet
        time.sleep(20)
	GPIO.output(26,GPIO.HIGH)   #Relais hört auf zu bestromen
	GPIO.output(19,GPIO.HIGH)   #Sicherstellen, dass das Motorrelais high ist
else:
    GPIO.output(27, GPIO.HIGH)      #rote LED ist an
    GPIO.output(15, GPIO.LOW)       #grüne LED ist aus
    if Fensterauf-Fensterwar==0:     #dann ist keine Änderung nötig
        GPIO.output(26,GPIO.HIGH)  #kein Strom zum Betreiben des Motors
    elif Fensterauf-Fensterwar<0:   #dann war das Fenster offen und muss geschlossen werden
	mail.send(formatedData)
        GPIO.output(26,GPIO.LOW)   #Relais bestromt das andere!
        GPIO.setup(19,GPIO.OUT)
        GPIO.output(19,GPIO.LOW)  #Motor schließt
        time.sleep(20)
	GPIO.output(26,GPIO.HIGH)   #Relais hört auf zu bestromen
        GPIO.output(19,GPIO.HIGH)   #Sicherstellen, dass das Motorrelais high ist



log= open (r'/home/pi/Desktop/luftfeuchtelog.txt',mode='a')#,encoding='utf8')
log.write(formatedData)
log.write('\n')
log.close()
