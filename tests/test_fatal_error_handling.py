"""Test that a fatal error causes the scheduler to exit.
"""
from antevents.base import *
from utils import make_test_sensor

import sys
import asyncio

class DieAfter(DefaultSubscriber):
    def __init__(self, num_events):
        self.events_left = num_events

    def on_next(self, x):
        self.events_left -= 1
        if self.events_left == 0:
            print("throwing fatal error")
            raise FatalError("this is a fatal error")

sensor = make_test_sensor(1)
sensor.subscribe(print)
sensor2 = make_test_sensor(2)
sensor2.subscribe(print)
s = Scheduler(asyncio.get_event_loop())
s.schedule_periodic(sensor, 1)
s.schedule_periodic(sensor2, 1)
sensor.subscribe(DieAfter(4))
sensor.print_downstream()
try:
    s.run_forever()
except FatalError:
    print("got to end with fatal error thrown as expected")
else:
    print("did not get a fatal error!!!")
    sys.exit(1)