import board
import busio

class I2C:


    def __init__(self):

        self.wire = busio.I2C(board.SCL, board.SDA)


