

from ble_connect import XiaoBLE
from monitor import Monitor
from max30101 import MAX30101
from I2C import I2C
import board
import busio
import time

Xiao_1 = XiaoBLE()
I2C = busio.I2C(board.SCL, board.SDA)
hrm = Monitor()
sensor1, ax, ay, az = hrm.setup()
sensor = MAX30101(I2C)
i = 0
print("enter")
gbpmf = []
spo2f = []
#'''
while True:
    Xiao_1.BTConnect(False)
    command = "data"

    if command == "data":
        print("running")

        while not I2C.try_lock():
            pass

        try:
            [hex(device_address) for device_address in I2C.scan()]

        finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
            I2C.unlock()

        #gbpm, irbpm, spo2, spo22, accel_x, accel_y, accel_z = hrm.run_sensor(sensor, sensor1)
        gbpm, spo2, x, y, z= hrm.run_sensor(sensor, sensor1, ax, ay, az)
        gbpmf.append(gbpm)
        spo2f.append(spo2)
        if len(gbpmf) > 4:
            gbpmf.pop(0)
            spo2f.pop(0)
        if len(gbpmf) == 4:
            bpmf = int((gbpmf[0] + gbpmf[1] + gbpmf[2] + gbpmf[3])/4)
            spo2ff = int((spo2f[0] + spo2f[1] + spo2f[2] + spo2f[3])/4)
            #data = (str(bpmf) + " " + str(spo2ff) + " " + str(x) + " " + str(y) + " " + str(z))
            data = (str(bpmf) + "w" + str(spo2ff))
            #data = (str(bpmf) + " " + str(spo2ff))
            Xiao_1.sendData("data", data)
            print(data)
        print("done")
        #data = (str(gbpm) + ", " + str(irbpm) + ", " + str(spo2) + ", " + str(spo22) + ", " + str(accel_x) + ", " + str(accel_y) + ", " + str(accel_z))


        time.sleep(0.5)


