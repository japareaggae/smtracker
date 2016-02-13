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


def find_stats():
    """Returns the first LocalProfile, or else returns a MachineProfile."""
    lp_location = "/Save/LocalProfiles/00000000/Stats.xml"
    mp_location = "/Save/MachineProfile/Stats.xml"
    statsxml = None

    if sys.platform.startswith('linux'):
        local_profile = os.environ['HOME'] + "/.stepmania-5.0" + lp_location
        machine_profile = os.environ['HOME'] + "/.stepmania-5.0" + mp_location
    elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        local_profile = os.environ['APPDATA'] + "/StepMania 5" + lp_location
        machine_profile = os.environ['APPDATA'] + "/StepMania 5" + mp_location

    if os.path.isfile(local_profile):
        statsxml = local_profile
    elif os.path.isfile(machine_profile):
        statsxml = machine_profile
    return statsxml


# We can ask the program to read a specific file using argparse.
def get_argparser():
    """Creates an argparse parser."""
    parser = argparse.ArgumentParser(description='A StepMania Score Tracker')
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'),
                        default=find_stats(), help="the Stats.xml file to read "
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
    return parser

def main():
    args = get_argparser()
    statsxml = vars(args)['file']
    gamemode = vars(args)['mode']
    output_type = vars(args)['output']
    theme = vars(args)['theme']

    if output_type == "plain":
        output.plain.report(statsxml, gamemode, DIFFICULTIES)
    elif output_type == "qt":
        output.qt.run(statsxml, gamemode, DIFFICULTIES, theme)
