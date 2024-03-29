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

"""Initialization of smtracker and its options."""

import argparse
import os
import sys
import xml.etree.ElementTree as etree

import smtracker.output.plain as plain
import smtracker.output.qt as qt
import smtracker.output.html as html

import smtracker.utils.parse as parse

DIFFICULTIES = ["Beginner", "Easy", "Medium", "Hard", "Challenge"]


def find_stats():
    """Returns the first LocalProfile, or else returns a MachineProfile."""
    lp_folder, mp_folder = parse.get_profile_location()

    local_profile = lp_folder + "00000000/Stats.xml"
    machine_profile = mp_folder + "/Stats.xml"
    statsxml = None

    if os.path.isfile(local_profile):
        statsxml = local_profile
    elif os.path.isfile(machine_profile):
        statsxml = machine_profile
    return statsxml


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
                        help="the output to use (valid options are 'plain', "
                        "'html' and 'qt', defaults to 'qt')")
    parser.add_argument('-t', dest='theme', nargs='?', default='sm5.1',
                        const='sm5.1',
                        help="what theme should be used for calculating grades "
                        "(valid options are 'sm5', 'sm5.1', 'itg', 'supernova2' "
                        "and 'ddra', defaults to 'sm5.1')")
    parser.add_argument('-i', dest='ignore', nargs='+',
                        help="ignore the specified difficulty")
    parser.add_argument('-d', dest='dest', nargs='?', default='/tmp/sm.html',
                        help="where should the output file be saved (only for "
                        "html and plain outputs)")
    return parser

def main():
    """Runs smtracker."""
    parser = get_argparser()
    args = parser.parse_args()
    statsxml = args.file
    gamemode = args.mode
    output_type = args.output
    theme = args.theme
    dest = args.dest

    # Parse the statsxml file and return a tree for the outputs
    if statsxml is not None:
        stats = etree.parse(statsxml).getroot()

        # Check if this is a valid Stats.xml file before doing anything
        if stats.find("SongScores") is None:
            sys.exit("Error: The specified file is not a valid StepMania Stats.xml file")

    else:
        stats = None

    # Remove ignored difficulties from difficulties array
    if args.ignore:
        for diff in args.ignore:
            try:
                DIFFICULTIES.remove(diff)
            except ValueError:
                print("Warning: {} is not a valid difficulty".format(args.ignore))


    if output_type == "plain":
        plain.report(stats, gamemode, DIFFICULTIES, theme)
    elif output_type == "qt":
        qt.run(stats, gamemode, DIFFICULTIES, theme)
    elif output_type == "html":
        html.save(stats, gamemode, DIFFICULTIES, theme, dest)
