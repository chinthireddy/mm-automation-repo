#! python
import sys
import getopt
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import sys
from xml.dom.minidom import parse, parseString
from robot.libraries.OperatingSystem import OperatingSystem
#import datetime
from datetime import datetime


def main(argv):
    
    reportdir = str(argv[1])
    outputxmlfilepath = 'C:\\MM_Results\\' + reportdir + '\\output.xml'
    textdatafilepath = 'C:\\Mentoring_Minds\\mysatori-qa\\Wizard_Interface\\Automation_Testsuites\\Test.txt'
    SUITENAME = 'TestDataCreation'

    xmldoc = parse(outputxmlfilepath)
    
    #Read all the test suites from output.xml file
    itemlist = xmldoc.getElementsByTagName('suite')
    print itemlist
    starttiming = ''
    endtiming = ''

    for suite in range(0,len(itemlist)-1) :
        #Read the test suite names
        suitename= itemlist[suite].attributes['name'].value
        print suitename
        #Read the starttime and end time of the given suite
        if(suitename == SUITENAME): 
            statusTgList = itemlist[suite].getElementsByTagName('status')
            starttiming = statusTgList[suite].attributes['starttime'].value
            print starttiming
            
            for val in range (0,len(statusTgList)-1):
                endtiming = statusTgList[val].attributes['endtime'].value
            print endtiming
            break

    datetimeobject = datetime.strptime(starttiming,'%Y%m%d %H:%M:%S.%f')
    startdate = datetimeobject.strftime('%m-%d-%y')
    starttime = datetimeobject.strftime('%H:%M')
    datetimeobject = datetime.strptime(endtiming,'%Y%m%d %H:%M:%S.%f')
    enddate = datetimeobject.strftime('%m-%d-%y')
    endtime = datetimeobject.strftime('%H:%M')

    print startdate
    print starttime
    print enddate
    print endtime
    
    #Read the execution time from output.xml file.

    timevalue1 = starttiming
    timevalue2 = endtiming

    print timevalue1
    print timevalue2
    
    #diffval = timevalue2 - timevalue1
    #print "diffval:"+str(diffval)
    #diffvalList = str(diffval).split(".")
    #executiontime = diffvalList[0]

    filePath = textdatafilepath
    f = open(filePath,"r");
    contents = f.read()
    schoolDct = {}
    for row in contents.split("\n"):
        if len(row.strip())>0:
            print row
            rowvalues = row.split(" = ")
            schoolDct[str(rowvalues[0])]= str(rowvalues[1])
    print schoolDct

    if(schoolDct['NewSchoolsAdded']!='True'):
        return False

        
    with open("mailText.txt", "w") as myfile:

        print schoolDct['schoolName']
        string1 = str(schoolDct['schoolName'])
        if 'School' in string1 :
            schoolnamelist = string1.split("School")
            schoolDct['schoolName'] = schoolnamelist[0]
        print schoolDct['schoolName']
        
        URL = 'http://v4.tomo.zone/mysdb_m3_sales/_design/mys/mmloginw.html#customerid:'
        
        myfile.write(schoolDct['schoolName']+' school setup completed at '+ endtime +' on '+ enddate +'.\n')
        myfile.write('\n')
        
        myfile.write('It can now be accessed here:\n')
        myfile.write(URL+schoolDct['password']+'\n')
        myfile.write('\n')
        myfile.write('Zip code:'+schoolDct['zip']+'\n')
        myfile.write('\n')
        myfile.close()

    textfile = 'mailText.txt'
    fp = open(textfile, 'r') 
    body = fp.read()
    fp.close()

    if(schoolDct['Teststatus'] == 'FAIL'):
        return False

    msg = MIMEMultipart()

    # recipients email ids
    recipients = ['rpaschburg@sdtcorp.com','omer@mysatori.com','grant.clark@mysatori.com','chad.threet@mysatori.com','shubhra.m@tenxlabs.com','munindar.c@tenxlabs.com','kishore.c@tenxlabs.com','rj@mysatori.com','jason@mysatori.com'] 
    
    # Sender email details
    me = 'mentoringminds2015@gmail.com'
    Password = "b5c183=ra"

    #SMTP server details
    smtpservername = 'smtp.gmail.com'
    
    subject = 'Sandbox complete for '+schoolDct['schoolName']+' School at Zip Code ['+schoolDct['zip']+']'
    msg['From'] = me
    msg['To'] = COMMASPACE.join(recipients)
    msg['Date'] = formatdate(localtime = True)

    # Send the message via the Gmail server.
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
    smtp = smtplib.SMTP('smtp.gmail.com',587)
      
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo
    
    smtp.login(me,Password)

    smtp.sendmail(me, recipients, msg.as_string().replace("\\",""))
    smtp.close()
    print('The email subject is "' + msg['Subject'] +'"')


main(sys.argv)
