#!/usr/bin/python

import motorsPlusPlus as m

def main():
    print "change the INCHES_TO_TICKS constant in motorsPlusPlus to edit the drive distance."
    print "change the lAdjust constant if the robot is drifting."
    # drive 36 inches at 50% power
    m.drive_speed(36, 50)
    # rotate cc 90 degrees at 50% power
    m.rotate(90, 50)
    print "done"

if __name__ == "__main__":
    main()