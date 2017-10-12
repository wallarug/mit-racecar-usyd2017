#!/bin/usr/python
"""
    This script is built to read input from a joystick and at the same
    time, save a number of files while images are being captured.

    Author: @wallarug
    Date: 12/10/2017

"""

import pygame
from time import sleep
import sys

# start pygame
pygame.init()

# count how many joysticks there are...
joycount = pygame.joystick.get_count()

# check that a joystick is actually connected.
if joycount < 1:
    print("No Joystick detected!")
    sys.exit(0)

# there is atleast one joystick, let's get it.
j = pygame.joystick.Joystick(0)
j.init()

# display which joystick is being used
print("You are using the {0} controller.".format(j.get_name))

try:
    while True:
        pygame.event.pump() # keep everything current

        output = ""

        for i in range(j.numaxes()):
            output += "axis {0} {1}".format(i, j.get_axis(i))


except KeyboardInterrupt:
    j.quit()
    sys.exit("Thank you, come again!")
