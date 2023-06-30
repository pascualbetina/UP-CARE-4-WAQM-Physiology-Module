
from time import sleep
import board
import busio
from I2C import I2C

# register addresses
REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01

REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03

REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08

REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C

REG_LED2_PA = 0x0D
REG_LED3_PA = 0x0E
REG_PILOT_PA = 0x10 #proximity
REG_MULTI_LED_CTRL1 = 0x11 #SLOTS 2 AND 1
REG_MULTI_LED_CTRL2 = 0x12 #SLOTS 4 and 3

REG_TEMP_INTR = 0x1F
REG_TEMP_FRAC = 0x20
REG_TEMP_CONFIG = 0x21
REG_PROX_INT_THRESH = 0x30
REG_REV_ID = 0xFE
REG_PART_ID = 0xFF


class MAX30101:
    def __init__(self, wire):
        self.address = 0x57
        self.channel = 1
        self.i2c = wire

        sleep(1)  # wait 1 sec
        self.setup()
        # read & clear interrupt register (read 1 byte)
        while not self.i2c.try_lock():
            pass

        buffer = bytearray(1)
        self.i2c.writeto_then_readfrom(self.address, bytes([REG_INTR_STATUS_1]), buffer)
        reg_data = buffer



        self.i2c.unlock()


    def shutdown(self):

        while not self.i2c.try_lock():
            pass
        self.i2c.writeto(self.address, bytes([REG_MODE_CONFIG] + [0x80]))

        self.i2c.unlock()

    def reset(self):


        while not self.i2c.try_lock():
            pass

        self.i2c.writeto(self.address, bytes([REG_MODE_CONFIG] + [0x40]))

        self.i2c.unlock()

    def sleep(self):

        while not self.i2c.try_lock():
            pass

        self.i2c.writeto(self.address, bytes([REG_LED1_PA] + [0x0]))
        self.i2c.writeto(self.address, bytes([REG_LED2_PA] + [0x0]))
        self.i2c.writeto(self.address, bytes([REG_LED3_PA] + [0x19]))

        self.i2c.unlock()

    def set_LED(self):
        while not self.i2c.try_lock():
            pass

        self.i2c.writeto(self.address, bytes([REG_LED1_PA] + [0x2f]))
        self.i2c.writeto(self.address, bytes([REG_LED2_PA] + [0x2f]))
        self.i2c.writeto(self.address, bytes([REG_LED3_PA] + [0x1f]))

        self.i2c.unlock()



    def setup(self, led_mode=0x07):

        while not self.i2c.try_lock():
            pass

        self.i2c.writeto(self.address, bytes([REG_INTR_ENABLE_1] + [0xc0]))
        self.i2c.writeto(self.address, bytes([REG_INTR_ENABLE_1] + [0x00]))
        self.i2c.writeto(self.address, bytes([REG_FIFO_WR_PTR] + [0x00]))
        #print(bytes([REG_FIFO_WR_PTR] + [0x00]))
        self.i2c.writeto(self.address, bytes([REG_OVF_COUNTER] + [0x00]))
        self.i2c.writeto(self.address, bytes([REG_FIFO_RD_PTR] + [0x00]))
        #print(bytes([REG_FIFO_RD_PTR] + [0x00]))
        self.i2c.writeto(self.address, bytes([REG_FIFO_CONFIG] + [0x4f]))
        self.i2c.writeto(self.address, bytes([REG_MODE_CONFIG] + [0x07]))
        self.i2c.writeto(self.address, bytes([REG_SPO2_CONFIG] + [0x27]))
        self.i2c.writeto(self.address, bytes([REG_LED1_PA] + [0x35]))
        self.i2c.writeto(self.address, bytes([REG_LED2_PA] + [0x35]))
        self.i2c.writeto(self.address, bytes([REG_LED3_PA] + [0x21]))
        self.i2c.writeto(self.address, bytes([REG_PILOT_PA] + [0x3f]))
        self.i2c.writeto(self.address, bytes([REG_MULTI_LED_CTRL1] + [0x21]))
        self.i2c.writeto(self.address, bytes([REG_MULTI_LED_CTRL2] + [0x03]))


        self.i2c.unlock()

    def set_config(self, reg, value):

        while not self.i2c.try_lock():
            pass

        self.i2c.writeto(self.address, bytes(reg + value))

        self.i2c.unlock()


    def get_data_present(self):

        while not self.i2c.try_lock():
            pass

        buffer1= bytearray(2)
        buffer2 = bytearray(2)
        self.i2c.writeto_then_readfrom(self.address, bytes([REG_FIFO_RD_PTR]), buffer1)
        self.i2c.writeto_then_readfrom(self.address, bytes([REG_FIFO_WR_PTR]), buffer2)
        read_ptr = (buffer1)[1]
        write_ptr = (buffer2)[1]

        if read_ptr == write_ptr:
            self.i2c.unlock()
            return 0
        else:
            num_samples = write_ptr - read_ptr

            if num_samples < 0:
                num_samples += 32
            self.i2c.unlock()
            return num_samples



    def read_fifo(self):

        while not self.i2c.try_lock():
            pass

        red_led = None
        ir_led = None
        green_led = None


        buffer1 = bytearray(1)
        buffer2 = bytearray(1)
        self.i2c.writeto_then_readfrom(self.address, bytes([REG_INTR_STATUS_1]), buffer1)
        self.i2c.writeto_then_readfrom(self.address, bytes([REG_INTR_STATUS_2]), buffer2)
        #print("buffer")
        #print(bytes([REG_INTR_STATUS_2]))
        reg_INTR1 = buffer1
        reg_INTR2 = buffer2


        buffer3 = bytearray(9)
        self.i2c.writeto_then_readfrom(self.address, bytes([REG_FIFO_DATA]), buffer3)
        d = buffer3

        red_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF
        ir_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF
        green_led = (d[6] << 16 | d[7] << 8 | d[8]) & 0x03FFFF

        self.i2c.unlock()

        return red_led, ir_led, green_led

    def read_sequential(self, amount=102):

        while not self.i2c.try_lock():
            pass

        red_buf = []
        ir_buf = []
        green_buf = []
        count = amount
        while count > 0:
            num_bytes = self.get_data_present()
            while num_bytes > 0:
                red, ir, green = self.read_fifo()

                red_buf.append(red)
                ir_buf.append(ir)
                green_buf.append(green)
                num_bytes -= 1
                count -= 1

        self.i2c.unlock()

        return red_buf, ir_buf, green_buf
