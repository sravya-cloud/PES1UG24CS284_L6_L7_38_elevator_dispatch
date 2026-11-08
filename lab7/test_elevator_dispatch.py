from hypothesis import given, strategies as st
from elevator_dispatch import parse_request, total_travel, load_percent

@given(st.text() | st.none())
def test_parse_request_no_crash(s):

@given(st.text() | st.none())
def test_total_travel_no_crash(s):

@given(st.text() | st.none())
def test_load_percent_no_crash(s):
