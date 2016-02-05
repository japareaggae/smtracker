#!/usr/bin/env python3
import argparse
import os
import sys

import output.plain

DIFFICULTIES = ["Beginner", "Easy", "Medium", "Hard", "Challenge"]
LP_LOCATION = "/Save/LocalProfiles/00000000/Stats.xml"
MP_LOCATION = "/Save/MachineProfile/Stats.xml"

# Sets the default location for statsxml.
if sys.platform.startswith('linux'):
    LINUX_LOCALPROFILE = os.environ['HOME'] + "/.stepmania-5.0" + LP_LOCATION
    LINUX_MACHINEPROFILE = os.environ['HOME'] + "/.stepmania-5.0" + MP_LOCATION
    if os.path.isfile(LINUX_LOCALPROFILE):
        def_statsxml = LINUX_LOCALPROFILE
    elif os.path.isfile(LINUX_MACHINEPROFILE):
        def_statsxml = LINUX_MACHINEPROFILE
    else:
        def_statsxml = None
elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    NT_LOCALPROFILE = os.environ['APPDATA'] + "/StepMania 5" + LP_LOCATION
    NT_MACHINEPROFILE = os.environ['APPDATA'] + "/StepMania 5" + MP_LOCATION
    if os.path.isfile(NT_LOCALPROFILE):
        def_statsxml = NT_LOCALPROFILE
    elif os.path.isfile(NT_MACHINEPROFILE):
        def_statsxml = NT_MACHINEPROFILE
    else:
        def_statsxml = None

# We can ask the program to read a specific file using argparse.
parser = argparse.ArgumentParser(description='A StepMania Score Tracker')
parser.add_argument('file', nargs='?', type=argparse.FileType('r'),
                    default=def_statsxml, help="the Stats.xml file to read "
                    "(will read first available StepMania profile if not "
                    "specified)")
parser.add_argument('-m', dest='mode', nargs='?', default='dance-single',
                    const='dance-single',
                    help="the game mode to print scores from (defaults to "
                    "'dance-single')")
args = parser.parse_args()
statsxml = vars(args)['file']
gamemode = vars(args)['mode']

output.plain.report(statsxml, gamemode, DIFFICULTIES)
