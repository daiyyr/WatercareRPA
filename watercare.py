import rpa as r
import sys, os
from time import gmtime, strftime
from datetime import datetime
import time
# import MySQLdb  Windows is trash
import mysql.connector



dir_path = os.path.dirname(os.path.realpath(__file__))
runningLogFile = os.path.join(dir_path, 'log.running.log')
errorLogFile = os.path.join(dir_path, 'log.error.log')
configFile = os.path.join(dir_path, 'run.config')
pdfFile = os.path.join(dir_path, 'statement.pdf')
pdfFolder = os.path.join(dir_path, 'pdf')

if not os.path.exists(pdfFolder):
    os.makedirs(pdfFolder)

if not os.path.exists(runningLogFile):
    with open(runningLogFile, 'w'): 
        pass
if not os.path.exists(errorLogFile):
    with open(errorLogFile, 'w'): 
        pass

def runningLog(logStr):
    s = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " -- " + str(logStr) + "\n"
    with open(runningLogFile, "a") as myfile:
        myfile.write(s)

def errorLog(logStr):
    s = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " -- " + str(logStr) + "\n"
    with open(errorLogFile, "a") as myfile:
        myfile.write(s)

try:
    with open(configFile) as fp:
        line = fp.readline()
        while line:
            if 'dbhost:' in line:
                dbhost = line.replace('dbhost:','').replace('\n','').strip()
            elif 'dbuser:' in line:
                dbuser = line.replace('dbuser:','').replace('\n','').strip()
            elif 'dbpass:' in line:
                dbpass = line.replace('dbpass:','').replace('\n','').strip()
            elif 'dbname:' in line:
                dbname = line.replace('dbname:','').replace('\n','').strip()
            elif 'azure_account:' in line:
                azure_account = line.replace('azure_account:','').replace('\n','').strip()
            elif 'azure_key:' in line:
                azure_key = line.replace('azure_key:','').replace('\n','').strip()
            elif 'pdf_path:' in line:
                directory = line.replace('pdf_path:','').replace('\n','').strip()
            elif 'pdf_2_path:' in line:
                directory2 = line.replace('pdf_2_path:','').replace('\n','').strip()
            elif 'pdf_3_path:' in line:
                directory3 = line.replace('pdf_3_path:','').replace('\n','').strip()
            elif 'pdf_4_path:' in line:
                directory4 = line.replace('pdf_4_path:','').replace('\n','').strip()
            elif 'pdf_5_path:' in line:
                directory5 = line.replace('pdf_5_path:','').replace('\n','').strip()
            elif 'watercarelogin:' in line:
                watercarelogin = line.replace('watercarelogin:','').replace('\n','').strip()
            elif 'watercarepassword:' in line:
                watercarepassword = line.replace('watercarepassword:','').replace('\n','').strip()
            line = fp.readline()
except Exception as e:
    errorLog('Reading config file error: ' + e)

def login(robot):
    robot.url('https://www.watercare.co.nz/MyAccount/Accounts')
    while not r.present('body'):
        time.sleep(1)
    txt = robot.read('body')
    if 'As you have 3 or more accounts' in txt:
        runningLog('Already logged in')
        return True
    if 'Your session has timed out' in txt:
        robot.url('https://www.watercare.co.nz/sign-out')
        while not r.present('body'):
            time.sleep(1)
        robot.url('https://www.watercare.co.nz/MyAccount/Accounts')
        while not r.present('body'):
            time.sleep(1)
    time.sleep(1)
    txt = robot.read('//*[@id="api"]')
    if not txt:
        runningLog('Login failed: id="api" not found in MyAccount/Accounts')
    elif 'Sign in with your existing account' in txt:
        robot.type('//*[@id="logonIdentifier"]', watercarelogin)
        robot.type('//*[@id="password"]', watercarepassword+'[enter]')
        while not r.present('body'):
            time.sleep(1)
        time.sleep(2)
        txt = robot.read('body')
        if 'As you have 3 or more accounts' in txt:
            runningLog('Login succeed')
        else:
            runningLog('Login failed: "As you have 3 or more accounts" not found after enter password')
    else:
        runningLog('Login failed: "Sign in with your existing account" not found in api')
    return False

try:
    conn = mysql.connector.connect(host= dbhost,
                user=dbuser,
                passwd=dbpass,
                db=dbname)
    readingCur = conn.cursor()
    readingCur.execute("SELECT accountnumber FROM useraccount where bccode is not null")
    accountNumberRows = readingCur.fetchall()

    # r.init(visual_automation = True) 
    r.init()
    while True:
        try:
            loginSucceed = False
            while not loginSucceed:
                loginSucceed = login(r)

            account1boxid = 'p_lt_WebPartZone3_MasterPageWebPartZone_pageplaceholder_p_lt_WebPartZone2_SectionContentWidgetZone_AccountsOverview_wcAccountSearch_accountNumberPart1'
            account2boxid = 'p_lt_WebPartZone3_MasterPageWebPartZone_pageplaceholder_p_lt_WebPartZone2_SectionContentWidgetZone_AccountsOverview_wcAccountSearch_accountNumberPart2'
            searchbuttonid = 'p_lt_WebPartZone3_MasterPageWebPartZone_pageplaceholder_p_lt_WebPartZone2_SectionContentWidgetZone_AccountsOverview_wcAccountSearch_accountSearchBtn'
            account1boxid_hist = 'p_lt_WebPartZone3_MasterPageWebPartZone_pageplaceholder_p_lt_WebPartZone2_SectionContentWidgetZone_BillingHistorySelector_BillingHistoryAccountSearch_accountNumberPart1'
            account2boxid_hist = 'p_lt_WebPartZone3_MasterPageWebPartZone_pageplaceholder_p_lt_WebPartZone2_SectionContentWidgetZone_BillingHistorySelector_BillingHistoryAccountSearch_accountNumberPart2'
            searchbuttonid_hist = 'p_lt_WebPartZone3_MasterPageWebPartZone_pageplaceholder_p_lt_WebPartZone2_SectionContentWidgetZone_BillingHistorySelector_BillingHistoryAccountSearch_accountSearchBtn'

            i = 0
            for row in accountNumberRows:
                acc = row[0].split('-')

                try:
                    while True:
                        i+=1
                        if i == 1:
                            account1box = account1boxid
                            account2box = account2boxid
                            searchbutton = searchbuttonid
                        else:
                            account1box = account1boxid_hist
                            account2box = account2boxid_hist
                            searchbutton = searchbuttonid_hist
                        

                        #enter account number
                        if not r.exist('//*[@id="'+account1box+'"]'):
                            i+=1
                            continue

                        r.type('//*[@id="'+account1box+'"]', "[clear]")
                        r.type('//*[@id="'+account1box+'"]', acc[0])
                        r.type('//*[@id="'+account2box+'"]', "[clear]")
                        r.type('//*[@id="'+account2box+'"]', acc[1])
                        
                        #click search
                        r.click('//*[@id="'+searchbutton+'"]')
                        while r.present('//*[@class="busy-load-container"'):
                            time.sleep(2)
                        time.sleep(2)

                        #click last bill
                        if i == 1:
                            r.click('Latest bill')
                        time.sleep(1)
                        while r.present('//*[@class="busy-load-container"'):
                            time.sleep(2)
                        if i == 1:
                            time.sleep(2)
                        txt = r.read('body')
                        if 'As you have 3 or more accounts' not in txt:
                            login(r)
                            continue

                        #click download
                        r.click('//td/a/span')
                        time.sleep(5)
                        targetfile = os.path.join(dir_path, pdfFolder, row[0] +'-'+ datetime.now().strftime("%Y%m%d") + '.pdf')
                        if os.path.exists(targetfile):
                            os.remove(targetfile)
                        os.rename(pdfFile, targetfile)
                        break


                except Exception as e:
                    errorLog(e)
        except Exception as e:
            errorLog(e)
        time.sleep(60*60*8)
except Exception as e:
    errorLog(e)




