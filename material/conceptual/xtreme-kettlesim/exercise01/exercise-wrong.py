#!/usr/bin/python3

from kettlesim import *

start_simulation("decisions")

fill_kettle()
turn_on_kettle()
wait_until_kettle_boiled()
pour_water_into_cup()
