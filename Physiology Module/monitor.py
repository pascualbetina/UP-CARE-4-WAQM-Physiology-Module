#
from max30101 import MAX30101
import hr_spo2
import time
from ulab import numpy as np

#gyro
from busio import I2C
from board import IMU_PWR, IMU_SCL, IMU_SDA
from time import sleep

from digitalio import DigitalInOut, Direction

from adafruit_lsm6ds.lsm6ds3 import LSM6DS3
from ulab import numpy as np


class Monitor(object):

    DEVICE_NAME = "XIAO nRF52840 Sense"
    INTERVAL = 0.1
    SENSITIVITY = 0.01

    def __init__(self,):
        self.gbpm = 0
        self.irbpm = 0
        self.spo2 = 0
        self.spo22 = 0
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 0
        #if print_raw is True:
            #print("IR, Red")



    def read_sensor(self, sensor, sensor1):
        #sensor = MAX30102()
        #sensor = MAX30105()
        ir_data = []
        red_data = []
        green_data = []
        bpms = []
        spo2s = []
        data_length = 200
        run = 1

        # Turn on IMU and wait 50 ms; gyro
        #imu_pwr = DigitalInOut(IMU_PWR)
        #imu_pwr.direction = Direction.OUTPUT
        #imu_pwr.value = True
        #sleep(0.05)

        #i2c_bus = I2C(IMU_SCL, IMU_SDA)
        #sensor1 = LSM6DS3(i2c_bus)
        run = 1

        #'''
        while run < 5:
            num_bytes = sensor.get_data_present()
            if num_bytes > 0:
                # grab all the data and stash it into arrays
                while num_bytes > 0:

                    red, ir, green = sensor.read_fifo()
                    num_bytes -= 1
                    #with open("/Data.txt", "a") as fp:

                    ir_data.append(ir)
                    red_data.append(red)
                    green_data.append(green)
                    #accel_x, accel_y, accel_z = sensor1.acceleration
                        #fp.write(str(red) + ", " + str(ir) + "\n")

                    print(ir)
                    print(red)
                    print(green)

                    if len(ir_data) % 100 == 1:
                        run = run + 1
                    #print(accel_x)
                    #print(accel_y)
                    #print(accel_z)
        #'''
        print("--")

    def setup(self):
        #sensor = MAX30102()
        acc_x = []
        acc_y = []
        acc_z = []
        i = 0

        imu_pwr = DigitalInOut(IMU_PWR)
        imu_pwr.direction = Direction.OUTPUT
        imu_pwr.value = True
        sleep(0.05)

        i2c_bus = I2C(IMU_SCL, IMU_SDA)
        sensor1 = LSM6DS3(i2c_bus)

        while i < 50:
            accel_x, accel_y, accel_z = sensor1.acceleration
            acc_x.append(accel_x)
            acc_y.append(accel_y)
            acc_z.append(accel_z)
            i = i + 1

        acc_x = np.mean(acc_x)
        acc_y = np.mean(acc_y)
        acc_z = np.mean(acc_z)

        return sensor1, acc_x, acc_y, acc_z

    def run_sensor(self, sensor, sensor1, x, y, z):


        #print("run")
        #sensor.set_LED()
        #print("led")
        #sensor = MAX30102()

        ir_data = []
        red_data = []
        green_data = []
        accel_x_data = []
        accel_y_data = []
        accel_z_data = []
        data_length = 75
        #run = 1
        gbpm_fin = []
        #irbpm_fin = []
        spo2_fin = []
        #spo22_fin = []
        ir_mean = 0
        green_mean = 0
        red_mean = 0
        enough = False

        while enough == False:
            #print("start")
            # check if any data is available
            num_bytes = sensor.get_data_present()

            #print(num_bytes)

            if num_bytes > 0:
                # grab all the data and stash it into arrays
                #print(num_bytes)
                while len(ir_data) < data_length + 5:
                #while num_bytes > 0:
                    #print("num_bytes>0")
                    red, ir, green = sensor.read_fifo()
                    #print("reading fifo")
                    #accel_x, accel_y, accel_z = sensor1.acceleration
                    num_bytes -= 1

                    ir_data.append(ir)
                    red_data.append(red)
                    green_data.append(green)
                    ir_mean = ir_mean + ir
                    green_mean = green_mean + green
                    red_mean = red_mean + red
                    #accel_x_data.append(accel_x)
                    #accel_y_data.append(accel_y)
                    #accel_z_data.append(accel_z)

                while len(ir_data) > data_length:
                    ir_mean = ir_mean - ir_data[0]
                    green_mean = green_mean - green_data[0]
                    red_mean = red_mean - red_data[0]
                    ir_data.pop(0)
                    red_data.pop(0)
                    green_data.pop(0)

                if len(ir_data) == data_length:
                    #bpm, valid_bpm, spo2, valid_spo2 = hrcalc.calc_hr_and_spo2(ir_data, red_data)
                    green_mean = green_mean / data_length
                    red_mean = red_mean / data_length
                    ir_mean = ir_mean / data_length
                    if green_mean > 1000 and red_mean > 100000 and ir_mean > 100000:
                        try:
                            bpm, spo2 = hr_spo2.run_sensor(ir_data, red_data, green_data, green_mean, red_mean, ir_mean)
                        except:
                            print("error main")
                    else:
                        bpm = []
                        spo2 = []
                    ir_data.clear()
                    green_data.clear()
                    red_data.clear()
                    print("still running " + str(len(bpm)) + str(len(spo2)) + " " + str(bpm) + str(spo2))
                    if len(bpm) > 0:
                        gbpm_fin.append(np.mean(bpm))
                        ax, ay, az = sensor1.acceleration
                        accel_x_data.append(ax - x)
                        accel_y_data.append(ay - y)
                        accel_z_data.append(az - z)
                    if len(spo2) > 0:
                        spo2_fin.append(np.mean(spo2))
                        ax, ay, az = sensor1.acceleration
                        accel_x_data.append(ax - x)
                        accel_y_data.append(ay - y)
                        accel_z_data.append(az - z)
                    if len(gbpm_fin) > 3 and len(spo2_fin) > 3:
                        enough = True

            time.sleep(0.05)
        #print(gbpm_fin)
        self.gbpm = int(np.mean(gbpm_fin))
        self.spo2 = int(np.mean(spo2_fin))
        self.accel_x = round(np.mean(accel_x_data), 2)
        self.accel_y = round(np.mean(accel_y_data), 2)
        self.accel_z = round(np.mean(accel_z_data), 2)
        '''
        self.gbpm = int(np.mean(bpm))
        self.irbpm = int(np.mean(ir_bpm))
        self.spo2 = int(np.mean(spo2))
        self.spo22 = int(np.mean(spo2_met2))
        '''
        '''
        print("Green HR: " + str(self.gbpm) + str(bpm)) #+ str(fin_bpm))
        print("IR HR: " + str(self.irbpm) + str(ir_bpm))
        print("SpO2: " + str(self.spo2) + str(spo2))
        print("SpO2_Met2: " + str(self.spo22) + str(spo2_met2))
        #print("Accel_X: " + str(np.mean(accel_x_data)))
        print("shutting down")
        '''
        #return (self.gbpm, self.irbpm, self.spo2, self.spo22)
        return(self.gbpm, self.spo2, self.accel_x, self.accel_y, self.accel_z)
        #sensor.sleep()
        #sensor.reset()
        #sensor.shutdown()



