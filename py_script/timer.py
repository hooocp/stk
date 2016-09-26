import time
import os

while True:
    time.sleep(3600*24)
    os.system('hive -f blacklist.sql')


