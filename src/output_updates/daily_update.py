import json
import chroma
from configobj import ConfigObj
from gpio_update import GPIOUpdater
from weather_updates.wu_data import WU


class DailyUpdate:
    def __init__(self):
        self.day_config = ConfigObj('config/day.cfg')
        self.color_config = ConfigObj('config/color.cfg')
        self.light_changer = GPIOUpdater()

    def write_day(self):
        # TODO need to be able to split this into hour and minute for the cron jobs
        sunrise, sunset = self._get_sunrise_sunset()
        sunrise = sunrise.replace(':', '')
        sunset = sunset.replace(':', '')

        self.day_config['SEGMENT'] = {}
        self.day_config['SEGMENT']['sunrise'] = sunrise
        self.day_config['SEGMENT']['morning'] = str(int(sunrise) + 200)
        self.day_config['SEGMENT']['midday'] = str(int((int(sunrise)
                                                        + int(sunset)) / 2))
        self.day_config['SEGMENT']['sunset'] = sunset
        self.day_config['SEGMENT']['evening'] = str(int(sunset) + 200)
        self.day_config['SEGMENT']['night'] = '2300'
        self.day_config.write()

    def _get_sunrise_sunset(self):
        w = WU()
        astronomy = json.loads(w.get_astronomy().content)

        rise_hour = astronomy['sun_phase']['sunrise']['hour']
        rise_minute = astronomy['sun_phase']['sunrise']['minute']
        set_hour = astronomy['sun_phase']['sunset']['hour']
        set_minute = astronomy['sun_phase']['sunset']['minute']

        sunrise = '{}:{}'.format(rise_hour, rise_minute)
        sunset = '{}:{}'.format(set_hour, set_minute)
        return (sunrise, sunset)

    def get_condition_color(self, condition):
        condition_color = self.color_config['CONDITION_COLOR_MAP'][condition]
        condition_rgb = tuple(map(int,
                                  self.color_config['COLORS'][condition_color]))
        return chroma.Color((condition_rgb), 'RGB256')

    def get_current_color(self):
        current_config_color = tuple(
            map(int, self.color_config['CURRENT']['light_color']))
        return chroma.Color((current_config_color), 'RGB256')

    def update_segment(self, segment):
        current_color = self.get_current_color()

        if segment == 'sunrise':
            new_color = current_color - get_condition_color('night')
        elif segment == 'morning':
            new_color = current_color - get_condition_color('sunrise')
        elif segment == 'midday':
            new_color = current_color - get_condition_color('morning')
        elif segment == 'sunset':
            new_color = current_color - get_condition_color('midday')
        elif segment == 'evening':
            new_color = current_color - get_condition_color('sunset')
        elif segment == 'night':
            new_color = current_color - get_condition_color('evening')

        new_color = new_color + self.get_current_color(segment)
        self.color_config['CURRENT']['light_color'] = new_color.rgb256
        self.color_config.write()
        self.light_changer.update_light(new_color.rgb256)


if __name__ == "__main__":
    du = DailyUpdate()
    du.write_day()
