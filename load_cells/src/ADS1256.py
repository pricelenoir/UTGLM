# Description: This file defines a Python class and associated constants for interacting with the ADS1256, an analog-to-digital converter (ADC).
from src import config
import RPi.GPIO as GPIO

class ADS1256:
    ScanMode = 0 # Tracks the scanning mode (single-ended/differential)

    # Gain channel
    GAIN_E = {'GAIN_1' : 0,
              'GAIN_2' : 1,
              'GAIN_4' : 2,
              'GAIN_8' : 3,
              'GAIN_16' : 4,
              'GAIN_32' : 5,
              'GAIN_64' : 6,
            }
    
    # Data rate
    DATA_RATE_E = { '30000SPS' : 0xF0,   # Reset the default values
                    '15000SPS' : 0xE0,
                    '7500SPS' : 0xD0,
                    '3750SPS' : 0xC0,
                    '2000SPS' : 0xB0,
                    '1000SPS' : 0xA1,
                    '500SPS' : 0x92,
                    '100SPS' : 0x82,
                    '60SPS' : 0x72,
                    '50SPS' : 0x63,
                    '30SPS' : 0x53,
                    '25SPS' : 0x43,
                    '15SPS' : 0x33,
                    '10SPS' : 0x20,
                    '5SPS' : 0x13,
                    '2d5SPS' : 0x03
                }
    
    # Registration definition
    REG_E = {'STATUS' : 0, # x1H
            'MUX' : 1,     # 01H
            'ADCON' : 2,   # 20H
            'DRATE' : 3,   # F0H
            'IO' : 4,      # E0H
            'OFC0' : 5,    # xxH
            'OFC1' : 6,    # xxH
            'OFC2' : 7,    # xxH
            'FSC0' : 8,    # xxH
            'FSC1' : 9,    # xxH
            'FSC2' : 10,   # xxH
            }
    
    # Command definitions
    CMD = { 'WAKEUP' : 0x00,     # Completes SYNC and Exits Standby Mode 0000  0000 (00h)
            'RDATA' : 0x01,      # Read Data 0000  0001 (01h)
            'RDATAC' : 0x03,     # Read Data Continuously 0000   0011 (03h)
            'SDATAC' : 0x0F,     # Stop Read Data Continuously 0000   1111 (0Fh)
            'RREG' : 0x10,       # Read from REG rrr 0001 rrrr (1xh)
            'WREG' : 0x50,       # Write to REG rrr 0101 rrrr (5xh)
            'SELFCAL' : 0xF0,    # Offset and Gain Self-Calibration 1111    0000 (F0h)
            'SELFOCAL' : 0xF1,   # Offset Self-Calibration 1111    0001 (F1h)
            'SELFGCAL' : 0xF2,   # Gain Self-Calibration 1111    0010 (F2h)
            'SYSOCAL' : 0xF3,    # System Offset Calibration 1111   0011 (F3h)
            'SYSGCAL' : 0xF4,    # System Gain Calibration 1111    0100 (F4h)
            'SYNC' : 0xFC,       # Synchronize the A/D Conversion 1111   1100 (FCh)
            'STANDBY' : 0xFD,    # Begin Standby Mode 1111   1101 (FDh)
            'RESET' : 0xFE,      # Reset to Power-Up Values 1111   1110 (FEh)
        }
        
    # Initializes the chip select (CS), reset (RST), and data ready (DRDY) pins using config.py
    def __init__(self):
        self.rst_pin = config.RST_PIN
        self.cs_pin = config.CS_PIN
        self.drdy_pin = config.DRDY_PIN

    # Resets the ADS1256 by toggling the reset pin.
    def reset(self):
        config.digital_write(self.rst_pin, GPIO.HIGH)
        config.delay_ms(200)
        config.digital_write(self.rst_pin, GPIO.LOW)
        config.delay_ms(200)
        config.digital_write(self.rst_pin, GPIO.HIGH)
    
    # Sends a command to the ADS1256
    def write_cmd(self, reg):
        config.digital_write(self.cs_pin, GPIO.LOW) # cs  0
        config.spi_writebyte([reg])
        config.digital_write(self.cs_pin, GPIO.HIGH) # cs 1
    
    # Writes a value to a specific register
    def write_register(self, reg, data):
        config.digital_write(self.cs_pin, GPIO.LOW) # cs  0
        config.spi_writebyte([self.CMD['WREG'] | reg, 0x00, data])
        config.digital_write(self.cs_pin, GPIO.HIGH) # cs 1
    
    # Reads data from a specified register
    def read_register(self, reg):
        config.digital_write(self.cs_pin, GPIO.LOW) # cs  0
        config.spi_writebyte([self.CMD['RREG'] | reg, 0x00])
        data = config.spi_readbytes(1)
        config.digital_write(self.cs_pin, GPIO.HIGH) # cs 1
        return data
    
    # Waits for the DRDY pin to indicate data availability
    def wait_DRDY(self):
        for i in range(0,400000,1):
            if(config.digital_read(self.drdy_pin) == 0):
                break
        if(i >= 400000):
            print ("Time Out ...\r\n")
        
    # Reads the chip ID from the status register
    def read_chipID(self):
        self.wait_DRDY()
        id = self.read_register(self.REG_E['STATUS'])
        id = id[0] >> 4
        return id
        
     # Configure ADC with specified gain and data rate
    def config_ADC(self, gain, drate):
        self.wait_DRDY()
        buf = [0, 0, 0, 0, 0, 0, 0, 0]
        buf[0] = (0 << 3) | (1 << 2) | (0 << 1)
        buf[1] = 0x08
        buf[2] = (0 << 5) | (0 << 3) | (gain << 0)
        buf[3] = drate

        config.digital_write(self.cs_pin, GPIO.LOW)  # cs  0
        config.spi_writebyte([self.CMD['WREG'] | 0, 0x03])
        config.spi_writebyte(buf)

        config.digital_write(self.cs_pin, GPIO.HIGH)  # cs 1
        config.delay_ms(1)

    # Selects a specific single-ended channel
    def set_channel(self, channel):
        if channel > 7:
            return 0
        self.write_register(self.REG_E['MUX'], (channel<<4) | (1<<3))

    # Selects a differential channel pair
    def set_diff_channel(self, channel):
        if channel == 0:
            self.write_register(self.REG_E['MUX'], (0 << 4) | 1) # AIN0-AIN1
        elif channel == 1:
            self.write_register(self.REG_E['MUX'], (2 << 4) | 3) # AIN2-AIN3
        elif channel == 2:
            self.write_register(self.REG_E['MUX'], (4 << 4) | 5) # AIN4-AIN5
        elif channel == 3:
            self.write_register(self.REG_E['MUX'], (6 << 4) | 7) # AIN6-AIN7

    # Sets the scanning mode
    def set_mode(self, Mode):
        ScanMode = Mode

    # Initializes the ADS1256, resets it, and configures it with gain and data rate
    def initialize(self):
        if (config.module_init() != 0):
            return -1
        self.reset()
        id = self.read_chipID()
        if id != 3:
            print("ID Read failed")
            return -1
        # Correctly setting the gain to 8
        self.config_ADC(self.GAIN_E['GAIN_8'], self.DATA_RATE_E['3750SPS'])
        return 0
    
    # Reads raw data from ADC
    def read_ADC_data(self):
        self.wait_DRDY()
        config.digital_write(self.cs_pin, GPIO.LOW)  # cs  0
        config.spi_writebyte([self.CMD['RDATA']])

        buf = config.spi_readbytes(3)
        config.digital_write(self.cs_pin, GPIO.HIGH)  # cs 1
        read = (buf[0] << 16) & 0xff0000
        read |= (buf[1] << 8) & 0xff00
        read |= (buf[2]) & 0xff
        if read & 0x800000:
            read |= 0xFF000000  # Extend sign bit if negative
        return read
    
    # Reads the value from a differential channel pair.
    def get_diff_channel_value(self, channel_pair):
        self.set_diff_channel(channel_pair)
        self.write_cmd(self.CMD['SYNC'])
        self.write_cmd(self.CMD['WAKEUP'])
        return self.read_ADC_data()
    
    # Adjust gain and and channel settings to calibrate the load cell
    def calibrate(self):
        self.config_ADC(self.GAIN_E['GAIN_4'], self.DATA_RATE_E['ADS1256_30000SPS'])
        self.get_diff_channel_value(self, 2)
        return