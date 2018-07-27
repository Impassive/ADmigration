import csv

f = open("test.ldif", "w+")
with open('test.csv') as csvfile:
     reader = csv.DictReader(csvfile)
     baseuid = 10008
     base = str(baseuid)
     for row in reader:
         usrstr = (row['username'])
         user = usrstr.split('.')
         givenname = user[0]
         sn = user[1]
         title = (row['title'])
         unit = (row['unit'])
         f.write("dn: cn="+givenname.capitalize()+" " + sn.capitalize()+",ou=Employees,dc=wdt,dc=com\n"
                 "cn: "+givenname.capitalize()+" "+sn.capitalize()+"\n"
                 "gidnumber: 10000\n"
                 "givenname: "+givenname.capitalize()+"\n"
                 "homedirectory: /home/"+givenname+"."+sn+"\n"
                 "loginshell: /bin/bash\n"
                 "mail: "+givenname+"."+sn+"@weigandt-consulting.com\n"
                 "objectclass: posixAccount\n"
                 "objectclass: inetOrgPerson\n"
                 "objectclass: organizationalPerson\n"
                 "objectclass: person\n"
                 "physicaldeliveryofficename: "+unit+"\n"
                 "sn: "+sn.capitalize()+"\n"
                 "title: "+title+"\n" 
                 "uid: "+givenname+"."+sn+"\n"
                 "uidnumber: "+base+"\n\n")
         baseuid+=1
         base = str(baseuid)
f.close()