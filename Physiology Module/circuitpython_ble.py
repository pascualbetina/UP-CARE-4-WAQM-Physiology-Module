from time import sleep
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
#import main_hrmonitor


ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)



counter= 0
while True:


    ble.start_advertising(advertisement)  # Advertise when not connected.
    while not ble.connected:
        counter += 1
        print("Not connected: " +str(counter) + " sec")
        sleep(1)
        pass
    print("Connected")
    counter = 0
    while ble.connected:  # Connected

        while uart_server.in_waiting:  # Check BLE commands
            packet = uart_server.read()

            print(str(packet)[2:6])
            if str(packet)[2:6] == "data":

                try:
                    uart_server.write("Insert sensor data\n")  # Transmit data
                    #uart_server.write(sen)
                except OSError:
                    pass

        sleep(.2)


