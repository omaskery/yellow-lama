#!/usr/bin/python3

from kettlesim import *

start_simulation("decisions")

if kettle_is_empty():
	fill_kettle()
turn_on_kettle()
wait_until_kettle_boiled()
pour_water_into_cup()
