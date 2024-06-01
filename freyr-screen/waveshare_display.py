import framebuf
from machine import SPI, Pin
from utime import sleep

BLACK: int = 0x00
WHITE: int = 0xFF

WIDTH: int = 128
HEIGHT: int = 296

DC_PIN = 8
CS_PIN = 9
RESET_PIN = 12
BUSY_PIN = 13

# region Lut Configs
FULL_LUT = [
    0x80,
    0x66,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x40,
    0x0,
    0x0,
    0x0,
    0x10,
    0x66,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x20,
    0x0,
    0x0,
    0x0,
    0x80,
    0x66,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x40,
    0x0,
    0x0,
    0x0,
    0x10,
    0x66,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x20,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x14,
    0x8,
    0x0,
    0x0,
    0x0,
    0x0,
    0x2,
    0xA,
    0xA,
    0x0,
    0xA,
    0xA,
    0x0,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x14,
    0x8,
    0x0,
    0x1,
    0x0,
    0x0,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x44,
    0x44,
    0x44,
    0x44,
    0x44,
    0x44,
    0x0,
    0x0,
    0x0,
    0x22,
    0x17,
    0x41,
    0x0,
    0x32,
    0x36,
]

PARTIAL_LUT = [
    0x0,
    0x40,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x80,
    0x80,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x40,
    0x40,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x80,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0A,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x1,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x22,
    0x22,
    0x22,
    0x22,
    0x22,
    0x22,
    0x0,
    0x0,
    0x0,
    0x22,
    0x17,
    0x41,
    0xB0,
    0x32,
    0x36,
]
# endregion


class DisplayLandscape(framebuf.FrameBuffer):
    def __init__(self) -> None:
        self.reset_pin = Pin(RESET_PIN, Pin.OUT)

        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = WIDTH
        self.height = HEIGHT

        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.height, self.width, framebuf.MONO_VLSB)
        self.init()

    def digital_write(self, pin: Pin, value: int) -> None:
        pin.value(value)

    def digital_read(self, pin: Pin) -> int:
        return pin.value()

    def delay_ms(self, delaytime: int) -> None:
        sleep(delaytime / 1000.0)

    def spi_writebyte(self, data: list[int]) -> None:
        self.spi.write(bytearray(data))

    def module_exit(self) -> None:
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self) -> None:
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)

    def send_command(self, command: int) -> None:
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data: int) -> None:
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)

    def send_buffer(self, buffer: list[int]) -> None:
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buffer))
        self.digital_write(self.cs_pin, 1)

    def read_busy(self) -> None:
        print("e-Paper busy")
        while self.digital_read(self.busy_pin) == 1:  # 0: Idle, 1: Busy
            self.delay_ms(10)
        print("e-Paper busy release")

    def turn_on_display(self) -> None:
        self.send_command(0x22)  # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0xC7)
        self.send_command(0x20)  # MASTER_ACTIVATION
        self.read_busy()

    def turn_on_display_partial(self) -> None:
        self.send_command(0x22)  # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0x0F)
        self.send_command(0x20)  # MASTER_ACTIVATION
        self.read_busy()

    def lut(self, lut: list[int]) -> None:
        self.send_command(0x32)
        self.send_buffer(lut[0:153])
        self.read_busy()

    def set_lut(self, lut: list[int]) -> None:
        self.lut(lut)
        self.send_command(0x3F)
        self.send_data(lut[153])
        self.send_command(0x03)  # gate voltage
        self.send_data(lut[154])
        self.send_command(0x04)  # source voltage
        self.send_data(lut[155])  # VSH
        self.send_data(lut[156])  # VSH2
        self.send_data(lut[157])  # VSL
        self.send_command(0x2C)  # VCOM
        self.send_data(lut[158])

    def set_window(self, x_start: int, y_start: int, x_end: int, y_end: int) -> None:
        self.send_command(0x44)  # SET_RAM_X_ADDRESS_START_END_POSITION
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x_start >> 3) & 0xFF)
        self.send_data((x_end >> 3) & 0xFF)
        self.send_command(0x45)  # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(y_start & 0xFF)
        self.send_data((y_start >> 8) & 0xFF)
        self.send_data(y_end & 0xFF)
        self.send_data((y_end >> 8) & 0xFF)

    def set_cursor(self, x: int, y: int) -> None:
        self.send_command(0x4E)  # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(x & 0xFF)

        self.send_command(0x4F)  # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(y & 0xFF)
        self.send_data((y >> 8) & 0xFF)
        self.read_busy()

    def init(self) -> int:
        # EPD hardware init start
        self.reset()

        self.read_busy()
        self.send_command(0x12)  # SWRESET
        self.read_busy()

        self.send_command(0x01)  # Driver output control
        self.send_data(0x27)
        self.send_data(0x01)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x07)

        self.set_window(0, 0, self.width - 1, self.height - 1)

        self.send_command(0x21)  #  Display update control
        self.send_data(0x00)
        self.send_data(0x80)

        self.set_cursor(0, 0)
        self.read_busy()

        self.set_lut(FULL_LUT)
        # EPD hardware init end
        return 0

    def display(self, image: bytearray) -> None:
        if image is None:
            return
        self.send_command(0x24)  # WRITE_RAM
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(self.height):
                self.send_data(image[i + j * self.height])
        self.turn_on_display()

    def display_base(self, image: bytearray) -> None:
        if image is None:
            return
        self.send_command(0x24)  # WRITE_RAM
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(self.height):
                self.send_data(image[i + j * self.height])

        self.send_command(0x26)  # WRITE_RAM
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(self.height):
                self.send_data(image[i + j * self.height])

        self.turn_on_display()

    def display_partial(self, image: bytearray) -> None:
        if image is None:
            return

        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(2)

        self.set_lut(PARTIAL_LUT)
        self.send_command(0x37)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x40)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x3C)  # BorderWaveform
        self.send_data(0x80)

        self.send_command(0x22)
        self.send_data(0xC0)
        self.send_command(0x20)
        self.read_busy()

        self.set_window(0, 0, self.width - 1, self.height - 1)
        self.set_cursor(0, 0)

        self.send_command(0x24)  # WRITE_RAM
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(self.height):
                self.send_data(image[i + j * self.height])
        self.turn_on_display_partial()

    def clear(self, color: int) -> None:
        self.send_command(0x24)  # WRITE_RAM
        self.send_buffer([color] * self.height * int(self.width / 8))
        self.send_command(0x26)  # WRITE_RAM
        self.send_buffer([color] * self.height * int(self.width / 8))
        self.turn_on_display()

    def sleep(self) -> None:
        self.send_command(0x10)  # DEEP_SLEEP_MODE
        self.send_data(0x01)

        self.delay_ms(2000)
        self.module_exit()
