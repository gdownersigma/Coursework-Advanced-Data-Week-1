from main import parse_line, sleep_tracker
from datetime import datetime

def test_parse_line_begin_shift():
    d = datetime(1518,11,1,0,0)
    assert parse_line('[1518-11-01 00:00] Guard #10 begins shift') == [d,10]

def test_parse_line_wakes_up():
    d = datetime(1518,11,1,0,25)
    assert parse_line('[1518-11-01 00:25] wakes up') == [d,True]

def test_parse_line_falls_asleep():
    d = datetime(1518,11,1,0,25)
    assert parse_line('[1518-11-01 00:25] falls asleep') == [d,False]
    

def sleep_tracker_begin_shift():
    test_dict = {}
    d = datetime(1518,11,1,0,0)
    sleep_tracker([d,10])
    assert test_dict == {10:{}}
    

