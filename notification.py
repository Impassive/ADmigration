import csv
import smtplib, ssl

def mail_notification(mailBody, to):
    port = 465  # For SSL
    login = "****"
    password = '****'
    smtp_server = "smtp.googlemail.com"
    # Create a secure SSL context
    context = ssl.create_default_context()
    print("Login as: " + login + "\n" + "Pass: " + password)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(login, password)
        server.sendmail(from_addr=login, to_addrs=to, msg=mailBody)
        print('mail has been sent')


with open('./data/mailer.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        user = (row['username'])
        clearPassword = (row['clearPassword'])
        hash = (row['ssha hash'])
        email = (row['email'])
        mailBody = "Subject: LDAP script: test email notification\n\nBelow is your new user account: " + "\n"

        mailBody += "\n" + "Username: " + user
        mailBody += "\n" + "Password: " + clearPassword
        mailBody += "\n" + "Hash: " + hash
        print(mailBody)
        mail_notification(mailBody,"***")
