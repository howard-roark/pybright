"""
light_runner is the entry point for starting and updating the strip of LEDs

Usage:
    light_runner.py (--update=S | --start)

Options:
    -h --help       Show this scree
    -u --update     Run daily or hourly updates
    -s --start      Run the light for the first time
"""
import os
import time
from docopt import docopt
from crontab import CronTab
from configobj import ConfigObj
from daily_update import DailyUpdate
from hourly_update import HourlyUpdate
import pigpio


class LightSchedule:
    def __init__(self):
        self.color_config = ConfigObj('config/colors.cfg')
        self.path = os.path.realpath(__file__)
        self.ct = CronTab(user=True)

    def set_day_segment_times(self):
        daily_config = ConfigObj('config/day.cfg')

        sunrise = daily_config['SEGMENT']['sunrise']

        morning = daily_config['SEGMENT']['morning']
        midday = daily_config['SEGMENT']['midday']
        sunset = daily_config['SEGMENT']['sunset']
        evening = daily_config['SEGMENT']['evening']
        night = daily_config['SEGMENT']['night']

        sunrise_job = self.ct.new(command='python {path} --update=sunrise'.format
                                  (path=self.path))
        sunrise_job.hour(sunrise_hour)
        sunrise_job.minute(sunrise_minute)
        sunrise_job.enable()

        morning_job = self.ct.new(command='python {path} --update=morning'.format
                                  (path=self.path))
        morning_job.hour(morning_hour)
        morning_job.minute(morning_minute)
        morning_job.enable()

        midday_job = self.ct.new(command='python {path} --update=midday'.format
                                 (path=self.path))
        midday_job.hour(midday_hour)
        midday_job.minute(midday_minute)
        midday_job.enable()

        sunset_job = self.ct.new(command='python {path} --update=sunset'.format
                                 (path=self.path))
        sunset_job.hour(sunset_hour)
        sunset_job.minute(sunset_minute)
        sunset_job.enable()

        evening_job = self.ct.new(command='python {path} --update=evening'.format
                                  (path=self.path))
        evening_job.hour(evening_hour)
        evening_job.minute(evening_minute)
        evening_job.enable()

        night_job = self.ct.new(command='python {path} --update=night'.format
                                (path=self.path))
        night_job.hour(night_hour)
        night_job.minute(night_minute)
        night_job.enable()

    def start(self):
        start_color = self.color_config['CURRENT']['light_color']
        light_starter = GPIOUpdater()
        light_starter.update_light(start_color)

        self.lr.update_conditions('day')

    def update_conditions(self, job):
        du = DailyUpdate()
        if job == 'day':
            du.write_day()
            self.lr.set_day_segment_times()
        if job == 'hour':
            hu = HourlyUpdate()
            hu.update_condition()


if __name__ == "__main__":
    self.lr = LightSchedule()
    try:
        args = docopt(__doc__)
        switches = [option for option, enabled in args.iteritems() if enabled]
        if args['--update']:
            if args['--update'].lower() == 'day':
                self.lr.update_conditions('day')
            elif args['--update'].lower() == 'hour':
                self.lr.update_conditions('hour')
            else:
                print 'No valid update request passed in'
                sys.exit(1)
        elif '--start' in switches:
            self.lr.start()
            self.lr.set_day_segment_times()

            daily_cron = self.ct.new(command='python {path} --update=day'.format(path=self.path))
            daily_cron.day.every(1)
            daily_cron.enable()

            hourly_cron = self.ct.new(command='python {path} --update=hour'.format(path=self.path))
            hourly_cron.hour.during(5, 22).every(1)
            hourly_cron.enable()
        else:
            print 'No valid Args passed in'
            sys.exit(1)

    except:
        print 'Exception parsing args'
