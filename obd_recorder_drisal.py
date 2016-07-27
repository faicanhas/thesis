#!/usr/bin/env python

import obd_io_drisal
import serial
import platform
import obd_sensors_drisal
from datetime import datetime
import time
from time import strftime
import getpass

from obd_utils import scanSerial


# Add by Faisal on 29 June 2016
# Inisialisasi Kamus (Dictioanary) untuk menyimpan nilai terkini dari 5 paramter
data = {"rpm" : 0, "kecepatan" : 0, "engineload" : 0, "coolanttemp" : 0}


class OBD_Recorder():
    def __init__(self, path, log_items):
        self.port = None
        self.sensorlist = []

        waktu_log = strftime("%A %d %B %Y %H:%M:%S %Z")

        filename = path + waktu_log + ".log"
        self.log_file = open(filename, "w", 128)

        self.log_file.write("Waktu | RPM| Speed | Engine Load | Coolant Temperature\n");

        for item in log_items:
            self.add_log_item(item)

        self.gear_ratios = [34 / 13, 39 / 21, 36 / 23, 27 / 20, 26 / 21, 25 / 22]
        # log_formatter = logging.Formatter('%(asctime)s.%(msecs).03d,%(message)s', "%H:%M:%S") --> commented by faisal 240616

    def connect(self):
        portnames = scanSerial()
        # portnames = ['COM10']
        print portnames
        for port in portnames:
            self.port = obd_io_drisal.OBDPort(port, None, 2, 2)
            if (self.port.State == 0):
                self.port.close()
                self.port = None
            else:
                break

        if (self.port):
            print "Connected to " + self.port.port.name

    def is_connected(self):
        return self.port

    def add_log_item(self, item):
        for index, e in enumerate(obd_sensors_drisal.SENSORS):
            if (item == e.shortname):
                self.sensorlist.append(index)
                print "Logging item: " + e.name
                break

    def record_data(self):
        if (self.port is None):
            return None

        print "Logging started"

        while 1:
            waktu_log2 = strftime("%H:%M:%S")
            log_string = waktu_log2
            results = {}
            for index in self.sensorlist:
                (name, value, unit) = self.port.sensor(index)
                log_string = log_string + " | " + str(value)
                results[obd_sensors_drisal.SENSORS[index].shortname] = value;
#                 print results[obd_sensors_drisal.SENSORS[index].shortname]	# commented by Faisal on 29 June 2016
#                 print "index = ", index										# commented by Faisal on 29 June 2016
			
# 			Ekstraksi nilai dari parameter yang diukur ke dalam variabel		# Added by Faisal on 29 June 2016
            data_rpm = results[obd_sensors_drisal.SENSORS[0].shortname]
            data_speed = results[obd_sensors_drisal.SENSORS[1].shortname]
            # data_throttle_pos = results[obd_sensors_drisal.SENSORS[2].shortname]      # tidak dipakai, Sab 2 Jul 2016
            data_load = results[obd_sensors_drisal.SENSORS[3].shortname]
            data_temp = results[obd_sensors_drisal.SENSORS[4].shortname]

#             print "RPM = ", data_rpm
#             print "Kecepatan = ", data_speed
#             print "Throttle Position = ", data_throttle_pos
#             print "Engine Load = ", data_load
#             print "Coolant Temperature = ", data_temp
            
#           Update nilai kamus sesuai nilai parameter terkini
            data["rpm"] = data_rpm #optimum di 2500 (paper)
            data["kecepatan"] = data_speed # optimum di 60 (TA Iren dkk)
            # data["throttlepos"] = data_throttle_pos # optimum di 50 (cari lagi referensinya)
            data["engineload"] = data_load # optimum di 50 (cari lagi referensinya)
            data["coolanttemp"] = data_temp #optimum 80-90, katup coolant terbuka full, di 71-80 terbuka sebagian
            print data
            
#           Memasukkan nilai kamus ke file statusdata.txt
            file = open("statusdata.txt", "w")
            file.write(str(data))
            file.close()

            gear = self.calculate_gear(results["rpm"], results["speed"])
            log_string = log_string  # + "," + str(gear)
            self.log_file.write(log_string + "\n")

    def calculate_gear(self, rpm, speed):
        if speed == "" or speed == 0:
            return 0
        if rpm == "" or rpm == 0:
            return 0

        rps = rpm / 60
        mps = (speed * 1.609 * 1000) / 3600

        primary_gear = 85 / 46  # street triple
        final_drive = 47 / 16

        tyre_circumference = 1.978  # meters

        current_gear_ratio = (rps * tyre_circumference) / (mps * primary_gear * final_drive)

        # print current_gear_ratio
        gear = min((abs(current_gear_ratio - i), i) for i in self.gear_ratios)[1]
        return gear


username = getpass.getuser()
# logitems = ["rpm", "speed", "throttle_pos", "load", "fuel_status"]
logitems = ["rpm", "speed", "load", "temp"]
o = OBD_Recorder('/home/pi/pyobd-pi/log/', logitems)
o.connect()

if not o.is_connected():
    print "Not connected"
o.record_data()
