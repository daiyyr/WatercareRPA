import rpa as r
import sys, os
from time import gmtime, strftime
from datetime import datetime


dir_path = os.path.dirname(os.path.realpath(__file__))
runningLogFile = os.path.join(dir_path, 'log.running.log')
errorLogFile = os.path.join(dir_path, 'log.error.log')
configFile = os.path.join(dir_path, 'run.config')
if not os.path.exists(runningLogFile):
    with open(runningLogFile, 'w'): 
        pass
if not os.path.exists(errorLogFile):
    with open(errorLogFile, 'w'): 
        pass

def runningLog(logStr):
    s = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " -- " + logStr 
    with open(runningLogFile, "a") as myfile:
        myfile.write(s)

def errorLog(logStr):
    s = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " -- " + logStr
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
    txt = robot.read('page')
    if 'Your session has timed out' in txt:
        robot.url('https://www.watercare.co.nz/sign-out')
        robot.url('https://www.watercare.co.nz/MyAccount/Accounts')
    txt = robot.read('//*[@id="api"]')
    if not txt:
        runningLog('Login failed: id="api" not found in MyAccount/Accounts')
    elif 'Sign in with your existing account' in txt:
        robot.type('//*[@id="logonIdentifier"]', watercarelogin)
        robot.type('//*[@id="password"]', watercarepassword+'[enter]')
        txt = robot.read('page')
        if 'As you have 3 or more accounts' in txt:
            runningLog('Login succeed')
        else:
            runningLog('Login failed: "As you have 3 or more accounts" not found after enter password')
    else:
        runningLog('Login failed: "Sign in with your existing account" not found in api')

while True:
    try:
        r.init()
        login(r)


    except Exception as e:
        errorLog(e)



r.click('//*[@id="gsr"]')
r.type('//*[@name="q"]', 'decentralization[enter]')
print(r.read('result-stats'))
r.snap('page', 'results.png')
r.close()



