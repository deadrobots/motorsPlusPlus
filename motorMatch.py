# WIP (this code has never been tested, so may need to be commented out in order to run the program)
# Also, we do not have access to JSON, so will need to find alternative

# Adjusted motor drive (needs formatting and commenting):

'''
This set of methods is supposed to find the most equal settings on each motor. To do this, it finds the time taken to rotate the wheel 'rotations' times and stores them for later use. The drive_closest method drives at the closest set of motor speeds for the given speed. To be used, the generate_motor_data function should be called in calibrate, and import_motor_data needs to be called in init. drive_closest only uses the motor data at speeds greater than 30.
'''

from motorsPlusPlus import _clear_ticks, _drive, _left_ticks, _right_ticks, INCHES_TO_TICKS
from utils import *
import time
import random
import json

tolerance = 1.0

WHEEL_CIRCUMFERENCE = 1

rotations = 10

motorTime = {"L": [], "R": []}


def _export_motor_data():
    data = open("motors.txt", "w")
    data.write(json.dumps(motorTime))
    data.close()


def import_motor_data():
    data = open("motors.txt", "r")
    global motorTime
    motorTime = json.loads(data.read())
    data.close()


def _find_closest(speed):
    rightTime = motorTime["R"][speed]
    bestLeftSpeed = speed
    bestLeftDif = abs(rightTime - motorTime["L"][speed])

    for x in range(0, 101):
        leftTime = motorTime["L"][x]
        difTime = abs(rightTime - leftTime)

        if difTime < bestLeftDif:
            bestLeftDif = difTime
            bestLeftSpeed = x

    if bestLeftDif >= tolerance:
        print str(speed) + " IS A BAD SPEED. CLOSEST IS " + str(
            bestLeftSpeed) + " ON LEFT MOTOR, BUT IS OFF BY APPROX " + str(
            bestLeftDif / rotations) + " SECONDS PER ROTATION!"


def generate_motor_data():
    for x in range(0, 30):
        motorTime["L"].append(0)
        motorTime["R"].append(0)
    for x in range(30, 101):
        _clear_ticks()
        _drive(x, 0)
        initial = seconds()
        while _left_ticks() <= WHEEL_CIRCUMFERENCE * INCHES_TO_TICKS * rotations:
            pass
        num1 = seconds() - initial

        _clear_ticks()
        _drive(0, x)
        initial = seconds()
        while _right_ticks() <= WHEEL_CIRCUMFERENCE * INCHES_TO_TICKS * rotations:
            pass
        num2 = seconds() - initial

        motorTime["L"].append(num1)
        motorTime["R"].append(num2)

    for x in range(0, 101):
        _find_closest(x)
    _export_motor_data()


def drive_closest(speed):
    if speed >= 30:
        _drive(_find_closest(speed), speed)
    else:
        _drive(speed, speed)