import rpa as r
import sys, os
from time import gmtime, strftime
from datetime import datetime
import time
# import MySQLdb  Windows is trash
import mysql.connector
import shutil

el = 'test2'


r.init(visual_automation = True)
# r.init()
r.url('http://localhost:8080/')
while True:
    s = datetime.now().strftime('%S')
    size = int(int(s) / 6 * 10)
    r.type('//*[@id="'+el+'"]', "[clear]")
    # r.type('//*[@id="'+el+'"]', str(size))
    # r.type('//*[@id="'+el+'"]', str(size))
    r.keyboard(str(size))
