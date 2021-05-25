"""
"""

import collections
import dataclasses
import datetime
import unittest

from utility_duration import Duration


@dataclasses.dataclass
class Event:
    """is a baseclass to treat as the same interface
    """
    start: datetime.datetime
    end: datetime.datetime
    name: str
    def __post_init__(self):
        self.duration = Duration(self.start, self.end)

    def __eq__(self, other):
        return self.name == other.name and self.duration.match_exactly(other.duration)


class TestEvent(unittest.TestCase):
    def test_equation(self):
        now = datetime.datetime.now()
        hour = datetime.timedelta(hours=1)
        event_1 = Event(name='A', start=now, end=now+1*hour)
        event_2 = Event(name='B', start=now, end=now+1*hour)
        event_3 = Event(name='A', start=now, end=now+2*hour)
        self.assertTrue(event_1 == event_1)
        self.assertFalse(event_1 == event_2)
        self.assertFalse(event_1 == event_3)


class EventQueue(collections.deque):
    """base class for classification
    """
    pass