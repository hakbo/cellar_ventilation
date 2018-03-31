import Adafruit_DHT
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)            #kann muss aber nicht, um warnung aus zu blenden

###Festlegen der Konstanten
#R=8314.3 #Gaskonstante
#mw=18.016 #molare masse wasser
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

def heizenState(state):
	if (state == 0):
		res = "Heizung ist aus"
	elif (state == 1):
		res = "Heizung ist an"
	else:
		res = "Heizung ist kaputt."
	return res

###Setzen des Startwerts

GPIO.setup(27,GPIO.IN)      #status der roten LED wird auf beide parameter geschrieben
heizen = GPIO.input(27)
heizenwar = GPIO.input(27)

###Auslesen der Messwerte
Ti=T(4)
#Ta=T(10)
rFi=rF(4)
#rFa=rF(10)
###Definition der absoluten Feuchte
aFi=aF(Ti,rFi)

###Entscheidung ob heizen oder nicht
if Ti>= 7:
    heizen=0
elif Ti<=6:
    heizen=1
else:                                 #nehme an wenn kein else steht heißt das soviel wie: wenn dies dann das sonst tue nichts
    time.sleep(0.1)
#    print ("hysterese;keine Änderung bis zum Schwellwert")

###Ausgabe und Loggen der Daten
GPIO.setup(15,GPIO.OUT)             #grüne LED
GPIO.setup(27,GPIO.OUT)             #rote LED
GPIO.setup(26,GPIO.OUT)             #Relais zum Bestromen

if heizen==1:
    GPIO.output(15, GPIO.LOW)      #grüne LED ist aus
    GPIO.output(27, GPIO.HIGH)       #rote LED ist an
    if heizen-heizenwar==0:     #dann ist keine Änderung nötig
        GPIO.output(26,GPIO.HIGH)  #kein bestromen
    elif Fensterauf-Fensterwar>0:   #dann war heizung aus und muss angeschaltet werden
        GPIO.output(26,GPIO.LOW)   #Relais schaltet durch
else:
    GPIO.output(27, GPIO.LOW)      #rote LED ist aus
    GPIO.output(15, GPIO.HIGH)       #grüne LED ist an
    if heizen-heizenwar==0:     #dann ist keine Änderung nötig
        GPIO.output(26,GPIO.HIGH)  #kein bestromen
    elif Fensterauf-Fensterwar<0:   #dann war das heizung an und ausgeschaltet werden
        GPIO.output(26,GPIO.HIGH)   #Relais schaltet durch

data = [Ti, rFi, aFi]
stringData = list(map(lambda x: ("%.1f" % x).replace('.','.'), data))
stringTime = [time.strftime("%d.%m.%Y %H:%M")]
stringState = [heizenState(heizen)]
formatedData = ';'.join(stringTime+stringData+stringState)

log= open (r'/home/pi/Desktop/templog.txt',mode='a')#,encoding='utf8')
log.write(formatedData)
log.write('\n')
log.close()
