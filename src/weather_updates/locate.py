import sys
import json
import requests


class Location:
    def __init__(self):
        self.url = "http://ipinfo.io"
        r = requests.get(self.url)
        self.content = json.loads(r.content)

    def get_ipinfo_io(self):
        return self.content

    def get_latlong(self):
        lat_long = self.content['loc'].split(',')
        return (lat_long[0], lat_long[1])

    def get_city_state(self):
        city = str(self.content['city'])
        state = str(self.content['region'])
        return (city, state)


if __name__ == "__main__":
    l = Location()
    print(l.get_ipinfo_io())
