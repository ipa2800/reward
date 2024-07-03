import time
import RPi.GPIO as GPIO
from config import config
from logging_config import logger  # Import the logger

# 定义方向引脚 (DIR)、步进引脚 (STEP) 和使能引脚 (ENABLE)
DIR_PIN = 20
STEP_PIN = 21
ENABLE_PIN = 16
MODE_PINS = [14, 15, 18]  # 假设我们使用了这三个引脚来设置微步模式

class DRV8825():
    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        self.dir_pin = dir_pin
        self.step_pin = step_pin        
        self.enable_pin = enable_pin
        self.mode_pins = mode_pins
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        for pin in self.mode_pins:
            GPIO.setup(pin, GPIO.OUT)
        
    def digital_write(self, pin, value):
        if isinstance(pin, list):
            for p, v in zip(pin, value):
                GPIO.output(p, v)
        else:
            GPIO.output(pin, value)
        
    def Stop(self):
        self.digital_write(self.enable_pin, 0)
    
    def SetMicroStep(self, mode, stepformat):
        microstep = {'fullstep': (0, 0, 0),
                     'halfstep': (1, 0, 0),
                     '1/4step': (0, 1, 0),
                     '1/8step': (1, 1, 0),
                     '1/16step': (0, 0, 1),
                     '1/32step': (1, 0, 1)}

        if mode == 'software':
            self.digital_write(self.mode_pins, microstep[stepformat])
        
    def TurnStep(self, Dir, steps, stepdelay=0.005):
        if Dir == 'forward':
            self.digital_write(self.enable_pin, 1)
            self.digital_write(self.dir_pin, 0)
        elif Dir == 'backward':
            self.digital_write(self.enable_pin, 1)
            self.digital_write(self.dir_pin, 1)
        else:
            print("the dir must be : 'forward' or 'backward'")
            self.digital_write(self.enable_pin, 0)
            return

        if steps == 0:
            return
            
        for i in range(steps):
            self.digital_write(self.step_pin, True)
            time.sleep(stepdelay)
            self.digital_write(self.step_pin, False)
            time.sleep(stepdelay)

class StepperMotor:
    def __init__(self, driver):
        self.driver = driver

    def run(self, direction, steps, stepdelay, duration=None):
        self.driver.TurnStep(direction, steps, stepdelay)
        logger.debug(f'Motor running in {direction} direction for {steps} steps')
        
        if duration:
            time.sleep(duration)
            self.driver.Stop()

    def set_microstep_mode(self, mode, stepformat):
        self.driver.SetMicroStep(mode, stepformat)
        logger.debug(f'Set microstep mode to {mode} with {stepformat}')

    def stop(self):
        self.driver.Stop()
        logger.debug('Motor stopped')

if __name__ == "__main__":
    stepper_driver = DRV8825(DIR_PIN, STEP_PIN, ENABLE_PIN, MODE_PINS)
    motor = StepperMotor(stepper_driver)

    logger.info('Motor control starting...')

    try:
        print("Stepper motor test with DRV8825")
        motor.set_microstep_mode('software', 'fullstep')  # 设置为全步模式

        # 旋转操作示例
        steps = 512  # 旋转角度，根据电机的具体步数调整
        motor.run('forward', steps, 0.01)
        print("Rotation complete")

        # 可以通过配置触发条件来启动电机
        while True:
            try:
                if config.gift_received:
                    motor.run('forward', 200, 0.01)  # 每1秒运行一次
                else:
                    motor.run('forward', 200, 0.01, duration=2)  # 每2秒运行一次
                time.sleep(0.1)
            except KeyboardInterrupt:
                logger.info('Process interrupted by user')
                break
                
    except KeyboardInterrupt:
        print("Interrupted by user")
        logger.info('Process interrupted by user')
    finally:
        GPIO.cleanup()  # 清理GPIO设置
        logger.info('GPIO cleanup completed')
