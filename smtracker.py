#!/usr/bin/env python3
import argparse
import os

import output_plain

DIFFICULTIES = ["Beginner", "Easy", "Medium", "Hard", "Challenge"]

# Sets the default location for statsxml.
# TODO: Try to read the MachineProfile if there's no LocalProfile
# TODO: See if this works properly on both Cygwin and cmd.exe
if os.name == 'posix':
    def_statsxml = os.environ['HOME'] + "/.stepmania-5.0/Save/LocalProfiles/00000000/Stats.xml"
elif os.name == 'nt':
    def_statsxml = os.environ['APPDATA'] + "/StepMania 5/Save/LocalProfiles/00000000/Stats.xml"

# We can ask the program to read a specific file using argparse.
parser = argparse.ArgumentParser(description='A StepMania Score Tracker')
parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=def_statsxml,
        help="the Stats.xml file to read (will read from first available StepMania profile if not specified)")
args = parser.parse_args()
statsxml = vars(args)['file']

output_plain.report(statsxml, DIFFICULTIES)
