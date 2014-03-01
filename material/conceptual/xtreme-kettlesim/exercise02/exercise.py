#!/usr/bin/python3

from kettlesim import *

start_simulation("repetitions")

if kettle_is_empty():
	fill_kettle()
turn_on_kettle()
while not kettle_is_boiled():
	twiddle_thumbs()
pour_water_into_cup()
