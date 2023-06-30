from time import sleep
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import supervisor
from heartrate_monitor import HeartRateMonitor

class XiaoBLE:

    def __init__(self):
        self.counter = 0
        self.word = ""
        self.ble = BLERadio()
        self.uart_server = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart_server)
        self.connState = False
        self.ble.start_advertising(self.advertisement)  # Advertise when not connected.


    def BTConnect(self,commState):


        while not self.ble.connected:
            self.connState = False
            self.counter += 1
            print("Not connected: " +str(self.counter) + " sec")
            sleep(1)
            pass
        print("Connected")
        print()
        print()
        self.counter = 0
        self.connState = True

        #print(self.ble.connected)
        #print(self.connState)

        if commState == False:
            return

        else:

            while self.ble.connected:  # Connected

                while self.uart_server.in_waiting:  # Check BLE commands

                    self.packet = self.uart_server.read()
                    #print(self.packet)
                    self.word = str(self.packet)
                    print(self.word)

                    return str(self.word[2:len(self.word)-5])




                sleep(.2)





    def sendData(self,command,data):

        #print(command)
        if command == "data":

            try:
                self.uart_server.write(str(data)+"\n")  # Transmit data
            except OSError:
                pass

        elif command == "values":


            data = data #dummy data
            try:
                self.uart_server.write(str(data)+"\n")  # Transmit data
            except OSError:
                pass


        elif command == "reset":

            data = [1,2,3,4] #dummy data
            try:
                #self.uart_server.write(str(data)+"\n")  # Transmit data
                supervisor.reload()
            except OSError:
                pass



        sleep(.2)

    def sendMsg(self,msg):
        try:
            self.uart_server.write(str(msg)+"\n")  # Transmit msg
        except OSError:
            pass


