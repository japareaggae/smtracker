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

from collections import namedtuple

from jinja2 import Environment, PackageLoader

import smtracker.utils.format as smformat
import smtracker.utils.parse as parse


def main(stats, mode, difficulties, theme):
    # Get profile name from tree
    profile_name = parse.get_profile_name(stats)
    last_played = parse.get_last_played(stats)

    songs = []
    song_tuple = namedtuple('Song', ['group', 'title', 'scores'])
    score_tuple = namedtuple('Score', ['grade', 'perc', 'W1', 'W2', 'W3', 'W4',
                                       'W5', 'Miss'])

    for song in stats.find("SongScores"):
        location = song.attrib['Dir'].split('/')
        group = location[1]
        title = location[2]

        scores = []
        step_counter = 0
        for diff in difficulties:
            try:
                if song[step_counter].attrib['Difficulty'] == diff and \
                   song[step_counter].attrib['StepsType'] == mode:
                    try:
                        tier = parse.highscore_stat(song[step_counter], "Grade")
                        grade = smformat.tier_to_grade_sm5(tier)
                        percent = parse.highscore_stat(song[step_counter],
                                                       "PercentDP")
                        timings = parse.highscore_timings(song[step_counter])

                        scores.append(score_tuple(
                            grade = grade,
                            perc = percent,
                            W1 = timings['W1'],
                            W2 = timings['W2'],
                            W3 = timings['W3'],
                            W4 = timings['W4'],
                            W5 = timings['W5'],
                            Miss = timings['Miss']))

                    except AttributeError:
                        scores.append("")
                    step_counter = step_counter + 1
                else:
                    scores.append("")
            except IndexError:
                scores.append("")

        songs.append(song_tuple(group, title, scores))

    env = Environment(loader=PackageLoader('smtracker', 'templates'))
    template = env.get_template('template.html')
    print(template.render(
          name = profile_name,
          last_played = last_played,
          difficulties = difficulties,
          songs = songs))

