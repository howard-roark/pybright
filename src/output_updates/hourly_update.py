import json
import nltk
import chroma
from configobj import ConfigObj
from gpio_update import GPIOUpdater
from weather_updates.wu_data import WU


class HourlyUpdate:
    def __init__(self):
        self.w = WU()
        self.conditions = json.loads(self.w.get_conditions().content)
        self.light_changer = GPIOUpdater()
        self.color_config = ConfigObj('config/colors.cfg')

    def get_weather(self):
        return str(self.conditions['current_observation']['weather'])

    def get_condition_color(self):
        weather_tokens = nltk.word_tokenize(self.get_weather())
        pos_tags = ['JJ', 'JJR', 'JJS', 'NN', 'NNP', 'NNPS', 'NNS', 'VB']
        conditions = [cond for cond, tag in nltk.pos_tag(weather_tokens)
                      if tag in pos_tags]

        cc_map_keys = self.color_config['CONDITION_COLOR_MAP'].keys()
        light_color_rgb = tuple(map(int,
                                    self.color_config['CURRENT']['light_color']))
        light_color = chroma.Color(light_color_rgb, 'RGB256')
        for condition in conditions:
            if condition in cc_map_keys:
                condition_color_rgb = tuple(self.color_config['COLORS']
                                            [condition])
                condition_color = chroma.Color(condition_color_rgb, 'RGB256')
                light_color = light_color + condition_color

        return light_color

    def update_condition(self):
        light_color = self.get_condition_color()
        self.color_config['CURRENT']['light_color'] = light_color.rgb256
        self.color_config.write()
        self.light_changer.update_light(light_color.rgb256)
