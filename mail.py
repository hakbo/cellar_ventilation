import os
#import subprocess
import smtplib
#import socket
import datetime
#import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Accountinformationen zum Senden der E-Mail
Empfaenger = 'achim.boeckermann@gmail.com'
Absender = 'achim.boeckermann@gmx.net'
Passwort = '868Tri!!xd'
smtpserver = smtplib.SMTP('mail.gmx.net', 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo

# In Account einloggen
smtpserver.login(Absender, Passwort)

# Aktuelles Datum holen
Datum = datetime.date.today()


def send(data):
	msg = MIMEText(data)

	# Betreff + Datum
	msg['Subject'] = 'temperaturlog raspi - %s' % Datum.strftime('%b %d %Y')

	# Absender
	msg['From'] = Absender

	#Empfaenger
	msg['To'] = Empfaenger

	# E-Mail abschicken
	smtpserver.sendmail(Absender, [Empfaenger], msg.as_string())
	smtpserver.quit()


def send_attachment(files):
    msg = MIMEMultipart()#MIMEText(data)

	# Betreff + Datum
    msg['Subject'] = 'Temperatur- und Feuchteverlauf Keller - %s' % Datum.strftime('%b %d %Y')

	# Absender
    msg['From'] = Absender

	#Empfaenger
    msg['To'] = Empfaenger

	#Inhalt
    part= MIMEText('Luftfeuchteverlauf der letzten Zeit')
    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename="{}"'.format(os.path.basename(path)))
        msg.attach(part)

	# E-Mail abschicken
    smtpserver.sendmail(Absender, [Empfaenger], msg.as_string())
    smtpserver.quit()
