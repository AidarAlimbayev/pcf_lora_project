import time
import smtplib

TO='ameyrkhan@gmail.com' #all of the credentials
GMAIL_USER="pcf.kazatu@gmail.com"
# PASS= 'baor nlvb dtbn falz'
PASS= 'californicatioN'

SUBJECT = 'Alarm'
TEXT = 'Hello'
 

def send_mail(): #the texting portion
    print ("Sending text")
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(GMAIL_USER,PASS)
    header = 'To: ' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
    print (header)
    msg = header + '\n' + TEXT + '\n\n'
    server.sendmail(GMAIL_USER,TO,msg)
    server.quit()
    time.sleep(1)
    print ("Text sent")

send_mail()

