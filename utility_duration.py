"""
"""

import dataclasses
import datetime
import functools
import unittest

@dataclasses.dataclass
@functools.total_ordering
class Duration:
    start: datetime.datetime
    end: datetime.datetime

    def __post_init__(self):
        assert self.start < self.end, 'start should be before its end'

    def __str__(self):
        return 'start: {}, end: {}'.format(self.start, self.end)

    def __lt__(self, other) -> bool:
        """self is faster than other and they are not overlap
        """
        return self.end < other.start

    def __gt__(self, other) -> bool:
        """self is later than other and they are not overlap
        """
        return other.end < self.start

    def __eq__(self, other) -> bool:
        """judge self & other overlapping
        """
        return not (self < other or other < self)

    def match_exactly(self, other) -> bool:
        return self.start == other.start and self.end == other.end


class Test_Duration(unittest.TestCase):
    """test class of Duration
    """
    def setUp(self):
        now = datetime.datetime.now()
        hour = datetime.timedelta(hours=1)
        self.dur_0_1 = Duration(now + 0*hour, now + 1*hour)
        self.dur_1_2 = Duration(now + 1*hour, now + 2*hour)
        self.dur_2_3 = Duration(now + 2*hour, now + 3*hour)
        self.dur_0_3 = Duration(now + 1*hour, now + 3*hour)
        self.dur_1_4 = Duration(now + 0*hour, now + 4*hour)

    def test_reflect(self):
        """for an identical entity
            0   1   2   3   4
        A:  |---|
        B:  |---|
        """
        A = self.dur_0_1
        B = self.dur_0_1
        self.assertTrue(A == B)
        self.assertFalse(A < B)
        self.assertFalse(A > B)
        self.assertTrue(A <= B)
        self.assertTrue(A >= B)
        self.assertTrue(A.match_exactly(B))

    def test_separated(self):
        """for time-sepalated entities
            0   1   2   3   4
        A:  |---|
        B:          |---|
        """
        A = self.dur_0_1
        B = self.dur_2_3
        self.assertFalse(A == B)
        self.assertTrue(A < B)
        self.assertFalse(A > B)
        self.assertTrue(A <= B)
        self.assertFalse(A >= B)
        self.assertFalse(A.match_exactly(B))

    def test_included(self):
        """for an entity including another
            0   1   2   3   4
        A:  |-----------|
        B:      |---|
        """
        A = self.dur_0_3
        B = self.dur_1_2
        self.assertTrue(A == B)
        self.assertFalse(A < B)
        self.assertFalse(A > B)
        self.assertTrue(A <= B)
        self.assertTrue(A >= B)
        self.assertFalse(A.match_exactly(B))

    def test_borderlap(self):
        """for two entities on boarder their start&end
            0   1   2   3   4
        A:  |---|
        B:      |---|
        """
        A = self.dur_0_1
        B = self.dur_1_2
        self.assertTrue(A == B)
        self.assertFalse(A < B)
        self.assertFalse(A > B)
        self.assertTrue(A <= B)
        self.assertTrue(A >= B)
        self.assertFalse(A.match_exactly(B))

    def test_overlap(self):
        """for two entities overlappinig
            0   1   2   3   4
        A:  |-----------|
        B:      |-----------|
        """
        A = self.dur_0_3
        B = self.dur_1_4
        self.assertTrue(A == B)
        self.assertFalse(A < B)
        self.assertFalse(A > B)
        self.assertTrue(A <= B)
        self.assertTrue(A >= B)
        self.assertFalse(A.match_exactly(B))

