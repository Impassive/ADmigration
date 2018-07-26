import csv

f = open("test.ldif", "w+")
with open('test.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     baseuid = 10008
     base = str(baseuid)
     for row in reader:
         string = (row['username'])
         user = string.split('.')
         givenname = user[0]
         sn = user[1]
         f.write("dn: cn="+givenname+" " + sn+",ou=Employees,dc=wdt,dc=com\n"
                 "cn: "+givenname+" "+sn+"\n"
                 "gidnumber: 10000\n"
                 "givenname: "+givenname+"\n"
                 "homedirectory: /home/"+givenname+"."+sn+"\n"
                 "loginshell: /bin/bash\n"
                 "objectclass: posixAccount\n"
                 "objectclass: inetOrgPerson\n"
                 "objectclass: organizationalPerson\n"
                 "objectclass: person\n"
                 "sn: "+sn+"\n"
                 "uid: "+givenname+"."+sn+"\n"
                 "uidnumber: "+base+"\n\n")
         baseuid+=1
         base = str(baseuid)
f.close()
