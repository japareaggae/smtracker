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

"""A plain text interface for visualizing your scores."""

import smtracker.utils.format as smformat
import smtracker.utils.parse as parse


def report(stats, mode, difficulties):
    """Prints the plain text report."""
    displayname = parse.get_profile_name(stats)
    lastplayed = parse.get_last_played(stats)
    print("Profile name is " + displayname)
    print("Last played date was " + lastplayed)

    for song in stats.find("SongScores"):
        location = song.attrib['Dir'].split('/')
        title = location[2]
        group = location[1]
        print(group + " - " + title)

        step_counter = 0
        for diff in difficulties:
            # IndexError is raised after we reach the final <Step> on the song
            # using step_counter
            try:
                if (song[step_counter].attrib['Difficulty'] == diff and
                        song[step_counter].attrib['StepsType'] == mode):
                    try:
                        grade = smformat.tier_to_grade_sm5(parse.highscore_stat \
                                (song[step_counter], "Grade"))
                        percent = float(parse.highscore_stat(song[step_counter],
                                                             "PercentDP")) * 100
                        print('+++ {:10}: {:3} ({:.2f})'.format(diff, grade, percent))
                    except AttributeError:
                        print("--- " + diff)
                    step_counter = step_counter + 1
                else:
                    print("--- " + diff)
            except IndexError:
                print("--- " + diff)
