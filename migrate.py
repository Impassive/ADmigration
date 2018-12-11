import csv
import random
import string
from passlib.hash import ldap_salted_sha1 as ssha

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
    return pwd


# Hash Password for RFC 2307 format ssha
def hashed_password(password):
    hash = ssha.hash(password)
    return hash




# Parse input csv and format to ldif
f = open("./data/test.ldif", "w+")
# Open another file to save email notification info
mail = open('./data/mailer.csv', mode='w')
with open('./data/test.csv') as csvfile:
     writer = csv.writer(mail, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
     writer.writerow(["username", "clearPassword", "ssha hash", "email"])
     reader = csv.DictReader(csvfile)
     baseuid = 30001
     base = str(baseuid)
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
         base = str(baseuid)
         writer.writerow([givenname.lower() + "." + sn.lower(), str(clearPassword), str(sshaPassword), ""])

mail.close()
f.close()

