from configobj import ConfigObj
import pigpio


class GPIOUpdater:
    def __init__(self):
        self.color_config = ConfigObj('config/colors.cfg')
        self.red_pin = int(self.color_config['PINS']['red'])
        self.green_pin = int(self.color_config['PINS']['green'])
        self.blue_pin = int(self.color_config['PINS']['blue'])

    def update_light(self, rgb_color):
        pi_io = pigpio.pi()

        pi_io.set_PWM_dutycycle(self.red_pin, rgb_color[0])
        pi_io.set_PWM_dutycycle(self.green_pin, rgb_color[1])
        pi_io.set_PWM_dutycycle(self.blue_pin, rgb_color[2])
