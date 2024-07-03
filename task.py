import threading
from motor import Motor
from led import LEDStrip
from display import Display
from config import config
from logging_config import logger  # Import the logger

class TaskManager:
    def __init__(self, motor_pin, led_pin):
        logger.debug('Initializing Task Manager')
        self.motor = Motor(motor_pin)
        self.led_strip = LEDStrip(led_pin)
        self.display = Display()
        
        self.start_tasks()

    def start_tasks(self):
        threading.Thread(target=self.motor.start).start()
        threading.Thread(target=self.led_strip.start).start()
        threading.Thread(target=self.display.start).start()
        logger.info("所有任务已启动")

    def handle_gift_event(self, gift_info):
        """
        This method would be called when a gift event is received from the Douyin API.
        """
        logger.info(f"收到礼物事件: {gift_info}")
        config.gift_received = True
        
        # Reset the gift status after a certain period
        threading.Timer(10, self.reset_gift_status).start()

    def reset_gift_status(self):
        config.gift_received = False
        logger.info("礼物状态已重置")

if __name__ == "__main__":
    motor_pin = 17  # Example GPIO pin number for motor control
    led_pin = 27    # Example GPIO pin number for LED control
    
    task_manager = TaskManager(motor_pin, led_pin)
