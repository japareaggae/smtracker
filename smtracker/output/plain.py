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

import xml.etree.ElementTree as etree

import utils.format
import utils.parse


def report(stats_xml, mode, difficulties):
    tree = etree.parse(stats_xml)
    Stats = tree.getroot()
    IsMachine = Stats.find("GeneralData").find("IsMachine").text
    LastPlayedDate = Stats.find("GeneralData").find("LastPlayedDate").text

    if IsMachine == "1":
        DisplayName = "(machine profile)"
    else:
        DisplayName = Stats.find("GeneralData").find("DisplayName").text

    try:
        print("Profile name is " + DisplayName)
    except TypeError:
        print("Profile name is unknown")

    print("Last played date was " + LastPlayedDate)

    for Song in Stats.find("SongScores"):
        Location = Song.attrib['Dir'].split('/')
        Title = Location[2]
        Group = Location[1]
        print(Group + " - " + Title)

        step_counter = 0
        for diff in difficulties:
            # IndexError is raised after we reach the final <Step> on the song
            # using step_counter
            try:
                if Song[step_counter].attrib['Difficulty'] == diff and Song[step_counter].attrib['StepsType'] == mode:
                    try:
                        grade = utils.format.tier_to_grade_sm5(utils.parse.highscore_stat(Song[step_counter], "Grade"))
                        percent = float(utils.parse.highscore_stat(Song[step_counter], "PercentDP")) * 100
                        print('+++ {:10}: {:3} ({:.2f})'.format(diff, grade, percent))
                    except AttributeError:
                        print("--- " + diff)
                    step_counter = step_counter + 1
                else:
                    print("--- " + diff)
            except IndexError:
                print("--- " + diff)
