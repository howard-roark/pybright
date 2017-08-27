import sys
import requests
from locate import Location

api_key = 'WU_APIKEY_NEEDED'
api_url = 'http://api.wunderground.com/api/{k}/'.format(k=api_key)
endpoint_params = '{}{}/q/{}/{}.json'


class WU:
    def __init__(self):
        l = Location()
        self.city, self.state = l.get_city_state()

    def get_astronomy(self):
        endpoint = 'astronomy'
        return requests.get(endpoint_params.format(api_url, endpoint,
                                                   self.state, self.city))

    def get_forecast(self):
        endpoint = 'forecast'
        return requests.get(endpoint_params.format(api_url, endpoint,
                                                   self.state, self.city))

    def get_conditions(self):
        endpoint = 'conditions'
        return requests.get(endpoint_params.format(api_url, endpoint,
                                                   self.state, self.city))


if __name__ == "__main__":
    w = WU()
    print('{}:\n\t{}'.format('Astronomy', w.get_astronomy()))
    print('{}:\n\t{}'.format('Forecast', w.get_forecast()))
    print('{}:\n\t{}'.format('Conditions', w.get_conditions()))
