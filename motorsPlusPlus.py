'''
Created on Aug 7, 2016
@author: graysonelias
'''

'''
This module tries to provide more accurate motor commands.
It requires boolean "isClone", integer "LMOTOR", and integer "RMOTOR" from a "constants" module.
These values refer to prime/clone status, the left motor's port, and the right motor's port respectively.
'''

from constants import isClone
from constants import LMOTOR
from constants import RMOTOR

from math import pi

from wallaby import ao
from wallaby import clear_motor_position_counter
from wallaby import freeze
from wallaby import get_motor_position_counter
from wallaby import get_servo_position
from wallaby import motor
from wallaby import msleep
from wallaby import seconds
from wallaby import set_servo_position

# Drive Constants
INCHES_TO_TICKS = 169   #205 - 161     #156#127#50 cm #265
WHEEL_DISTANCE = 4.25 #205 - 4.25  # Distance between the two wheels

lAdjust = 1.07 # adjust left wheel counter to fix drift

if isClone:
    INCHES_TO_TICKS = 190


# Motor Control #

def _drive(left, right):  # Moves the robot using motor commands.
    motor(LMOTOR, left)
    motor(RMOTOR, right)


def _stop():  # Turns off all the motors.
    ao()


def freeze_motors():  # Locks the motors to reduce drift.
    freeze(LMOTOR)
    freeze(RMOTOR)


def _right_ticks():  # Returns the right motor's tick count.
    return abs(get_motor_position_counter(RMOTOR))


def _left_ticks():  # Returns the left motor's tick count.
    return abs(get_motor_position_counter(LMOTOR)* lAdjust)


def _clear_ticks():  # Clears the motor ticks.
    clear_motor_position_counter(RMOTOR)
    clear_motor_position_counter(LMOTOR)


def calibrate(dist=0, num=0):  # WIP: Used to calibrate the constants for this module. Run as "calibrate()" to begin.
    if dist is 0:
        _clear_ticks()
        _drive(30, 30)
        msleep(3000)
        freeze_motors()
        print "Run the calibrate method again, but pass the distance traveled (inch) and the following number in:"
        print (_right_ticks() + _left_ticks()) / 2
    elif num is 0:
        drive_speed(6, 30)
        print "did it go " + str(dist) + " inches? If not, make slight adjustments to INCHES_TO_TICKS until it does."
    else:
        print "enter " + str(int(num / dist)) + " as INCHES_TO_TICKS. run calibrate again, but as calibrate(" + str(
            dist) + ", 0)"
    exit(0)


def arc_radius(angle, turnRadius, speed):  # Turns the robot "angle" degrees by arcing about "turnRadius".
    smallCircRadius = turnRadius - (WHEEL_DISTANCE / 2)
    largeCircRadius = turnRadius + (WHEEL_DISTANCE / 2)
    smallCircum = pi * 2 * smallCircRadius
    largeCircum = pi * 2 * largeCircRadius
    smallCircSeg = (angle / 360.0) * smallCircum
    largeCircSeg = (angle / 360.0) * largeCircum
    if turnRadius < 0:
        speed = -speed
    _clear_ticks()
    smallTicks = abs(INCHES_TO_TICKS * smallCircSeg)
    largeTicks = abs(INCHES_TO_TICKS * largeCircSeg)
    if angle > 0:
        smallSpeed = int(speed * (smallTicks / largeTicks))
        largeSpeed = int(speed)
        print smallTicks
        print largeTicks
        print smallTicks / largeTicks
        print smallSpeed
        print largeSpeed
        while _right_ticks() <= largeTicks:
            if (_right_ticks() / largeTicks) == (_left_ticks() / smallTicks):
                _drive(smallSpeed, largeSpeed)
            if (_right_ticks() / largeTicks) > (_left_ticks() / smallTicks):
                _drive(smallSpeed, int(largeSpeed / 1.3))
            if (_left_ticks() / smallTicks) > (_right_ticks() / largeTicks):
                _drive(int(smallSpeed / 1.3), largeSpeed)
    freeze_motors()
    print smallTicks
    print largeTicks
    print get_motor_position_counter(RMOTOR)


def drive_speed(inches, speed):  # Drives an exact distance in inches.
    print "driving exact distance"
    if inches < 0:
        speed = -speed
    _clear_ticks()
    ticks = abs(INCHES_TO_TICKS * inches)
    while _right_ticks() <= ticks:
        if _right_ticks() == _left_ticks():
            _drive(speed, speed)
        if _right_ticks() > _left_ticks():
            _drive(speed, int(speed / 1.3))
        if _left_ticks() > _right_ticks():
            _drive(int(speed / 1.3), speed)
    freeze_motors()
    print ticks
    print get_motor_position_counter(RMOTOR)


def drive_timed(lmotor, rmotor, time):
    print "driving timed"
    _clear_ticks()
    end = seconds() + time
    if lmotor == 0 or rmotor == 0:
        print "please use pivot instead!"

    elif abs(rmotor) <= abs(lmotor):
        mod = rmotor / (lmotor * 1.0)
        newLeftSpeed = lmotor
        newRightSpeed = int(mod * lmotor)
    elif abs(lmotor) < abs(rmotor):
        mod = (lmotor * 1.0) / rmotor
        newLeftSpeed = int(mod * rmotor)
        newRightSpeed = rmotor
    while seconds() <= end:
        if int(_right_ticks() / mod) == int(_left_ticks() / mod):
            _drive(newLeftSpeed, newRightSpeed)
        if int(_right_ticks() / mod) > int(_left_ticks() / mod):
            _drive(newLeftSpeed, int(newRightSpeed / 1.3))
        if int(_left_ticks() / mod) > int(_right_ticks() / mod):
            _drive(int(newLeftSpeed / 1.3), newRightSpeed)
    freeze_motors()
    print get_motor_position_counter(RMOTOR)


def drive_condition(lmotor, rmotor, testFunction,
                    state=True):  # Drives while "testFunction" returns "state" | an example would be: x.drive_condition(50, 50, x.getWait)
    print "driving under condition"
    _clear_ticks()
    if lmotor == 0 or rmotor == 0:
        print "please use pivot instead!"

    elif abs(rmotor) <= abs(lmotor):
        mod = rmotor / (lmotor * 1.0)
        newLeftSpeed = lmotor
        newRightSpeed = int(mod * lmotor)
    elif abs(lmotor) < abs(rmotor):
        mod = (lmotor * 1.0) / rmotor
        newLeftSpeed = int(mod * rmotor)
        newRightSpeed = rmotor
    while testFunction() is state:
        if int(_right_ticks() / mod) == int(_left_ticks() / mod):
            _drive(newLeftSpeed, newRightSpeed)
        if int(_right_ticks() / mod) > int(_left_ticks() / mod):
            _drive(newLeftSpeed, int(newRightSpeed / 1.3))
        if int(_left_ticks() / mod) > int(_right_ticks() / mod):
            _drive(int(newLeftSpeed / 1.3), newRightSpeed)
    freeze_motors()
    print get_motor_position_counter(RMOTOR)


def rotate(deg, speed):  # Rotates by using both wheels equally.
    if deg < 0:
        speed = -speed
        deg = -deg
    angle = deg / 360.0
    circ = pi * WHEEL_DISTANCE
    inches = angle * circ
    print circ
    print inches
    ticks = int(INCHES_TO_TICKS * inches)
    _clear_ticks()
    _drive(-speed, speed)
    while _right_ticks() <= ticks:
        pass
    freeze_motors()
    print get_motor_position_counter(RMOTOR)


def pivot_right(deg, speed):  # Pivots by moving the right wheel.
    if deg < 0:
        speed = -speed
        deg = -deg
    angle = deg / 360.0
    circ = pi * WHEEL_DISTANCE * 2
    inches = angle * circ
    ticks = int(INCHES_TO_TICKS * inches)
    _clear_ticks()
    _drive(0, speed)
    while _right_ticks() <= ticks:
        pass
    freeze_motors()


def pivot_left(deg, speed):  # Pivots by moving the left wheel.
    if deg < 0:
        speed = -speed
        deg = -deg
    angle = deg / 360.0
    circ = pi * WHEEL_DISTANCE * 2
    inches = angle * circ
    ticks = int(INCHES_TO_TICKS * inches)
    _clear_ticks()
    _drive(speed, 0)
    while _left_ticks() <= ticks:
        pass
    freeze_motors()

