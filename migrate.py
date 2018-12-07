import csv
import random
import string
from passlib.hash import ldap_salted_sha1 as ssha
import smtplib, ssl

def password_generation(length):
    count = 0
    pwd = ''
    while count != length:
        upper = [random.choice(string.ascii_uppercase)]
        lower = [random.choice(string.ascii_lowercase)]
        num = [random.choice(string.digits)]
        everything = upper + lower + num
        # Uncomment to allow symbols in passwords
        # symbol = [random.choice(string.punctuation)]
        # everything += symbol
        pwd += random.choice(everything)
        count += 1
        continue
    print(pwd)
    return pwd


# Hash Password for RFC 2307 format ssha
def hashed_password(password):
    hash = ssha.hash(password)
    print(hash)
    global u_hash
    u_hash = hash
    return hash


def mail_notification(mailBody):
    port = 465  # For SSL
    login = "mikhail.toporov@weigandt-consulting.com"
    password = 'F7hI2ZSGcpma'
    smtp_server = "smtp.googlemail.com"

    # Create a secure SSL context
    context = ssl.create_default_context()
    print("Login as: " + login + "\n" + "Pass: " + password)
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(login, password)
        server.sendmail(login, login, mailBody)
        server.quit()
        print('mail has been sent')

# Parse input csv and format to ldif
f = open("test.ldif", "w+")
with open('test.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     baseuid = 30001
     base = str(baseuid)
     mailBody = 'Next users were created: ' + "\n"
     for row in reader:
         usrstr = (row['username'])
         user = usrstr.split('.')
         givenname = user[0]
         sn = user[1]
         title = (row['title'])
         unit = (row['unit'])
         clearPassword = password_generation(12)
         sshaPassword = hashed_password(clearPassword)
         f.write("dn: cn=" + givenname.capitalize() + " " + sn.capitalize()+",ou=Konzum,ou=Projects,dc=wdt,dc=com\n"
                 "cn: " + givenname.capitalize() + " " + sn.capitalize()+"\n"
                 "gidnumber: 10000\n"
                 "givenname: " + givenname.capitalize() + "\n"
                 "homedirectory: /home/" + givenname + "." + sn + "\n"
                 "loginshell: /bin/bash\n"
                 "userpassword: " + str(sshaPassword) + "\n"
                 "mail: " + givenname + "." + sn + "@weigandt-consulting.com\n"
                 "objectclass: posixAccount\n"
                 "objectclass: inetOrgPerson\n"
                 "objectclass: organizationalPerson\n"
                 "objectclass: person\n"
                 "physicaldeliveryofficename: " + unit + "\n"
                 "sn: " + sn.capitalize() + "\n"
                 "title: " + title + "\n"
                 "uid: " + givenname + "." + sn + "\n"
                 "uidnumber: " + base + "\n\n")
         baseuid+=1
         mailBody+="\n" + "Username: " + givenname + "." + sn
         mailBody+="\n" + "Password: " + str(clearPassword)
         mailBody+="\n" + "Hash: " + str(sshaPassword)
         base = str(baseuid)
     print(mailBody)
     mail_notification(mailBody)
f.close()

