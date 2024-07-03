import time
import RPi.GPIO as GPIO
from config import config
from logging_config import logger  # Import the logger

class LEDStrip:
    def __init__(self, pin):
        logger.debug(f'Initializing LED Strip on pin: {pin}')
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def blink(self, duration):
        GPIO.output(self.pin, GPIO.HIGH)
        logger.debug(f'LED blinking for {duration / 2} seconds ON')
        time.sleep(duration / 2)
        GPIO.output(self.pin, GPIO.LOW)
        logger.debug(f'LED blinking for {duration / 2} seconds OFF')
        time.sleep(duration / 2)

    def start(self):
        while True:
            if config.gift_received:
                self.blink(1)  # Blinks every 1 second
            else:
                # Implement neon effect here
                pass  # You can add your neon effect logic here
            time.sleep(0.1)
