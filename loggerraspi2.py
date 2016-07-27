from datetime import datetime, date, time
from time import gmtime, strftime, sleep

import time
import requests
import struct
import json
import urllib
import urllib2
import datetime
import base64
import ast

#ambil blok dari obd
android_id = '1234567890'
# rpm = 1
# kecepatan = 2
# engineload = 3
# coolanttemp = 4



## Added by Faisal on Rabu, 27 Juli 2016 11.46
# baca data parameter diambil dari file statusdata.txt dalam bentuk Python dictionary
file = open('statusdata.txt', 'r')
bacadata = file.read()  # masih dalam bentuk string
data = ast.literal_eval(bacadata)  # sudah dalam bentuk dict

rpm = data["rpm"]
kecepatan = data["kecepatan"]
engineload = data["engineload"]
coolanttemp = data["coolanttemp"]



#array data per menit
menit = {}
timestamp = strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#array data dari device
device = {}
device['android_id'] = android_id
device['rpm'] = rpm
device['kecepatan'] = kecepatan
device['engineload'] = engineload
device['coolanttemp'] = coolanttemp

menit[0] = device
    
#Blok persiapan kirim data ke server
data = {}
data['gateway'] = menit
json_data = json.dumps(data)
print json_data

golive = base64.b64encode(json_data)
print golive


#kirim data ke server
params = urllib.urlencode({'data': golive})
f = urllib.urlopen("http://enigmaofficials.com/raspberrylogger/raspberryapix", params)
print f.read()
sleep(1)
    
