import mail
import plotten

plotten.lf()
files=[luftfeuchtelog.txt, luftfeuchtelog.png]
mail.send_attachment(files)
