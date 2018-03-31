import mail
import plotten

plotten.temp()
files=['templog.txt', 'templog.png']
mail.send_attachment(files)
