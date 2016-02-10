#!/usr/bin/python3
# Copyright (C) 2016 Renan Guilherme Lebre Ramos
# This file is a part of smtracker.
#
# smtracker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import os
import sys

import output.plain
import output.qt

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
parser.add_argument('-o', dest='output', nargs='?', default='qt',
                    const='qt',
                    help="the output to use (valid options are 'plain' and "
                    "'qt', defaults to 'qt')")
parser.add_argument('-t', dest='theme', nargs='?', default='sm5',
                    const='sm5',
                    help="what theme should be used for calculating grades "
                    "(valid options are 'sm5' and 'itg', defaults to 'sm5')")


args = parser.parse_args()
statsxml = vars(args)['file']
gamemode = vars(args)['mode']
output_type = vars(args)['output']
theme = vars(args)['theme']

if output_type == "plain":
    output.plain.report(statsxml, gamemode, DIFFICULTIES)
elif output_type == "qt":
    output.qt.run(statsxml, gamemode, DIFFICULTIES, theme)
