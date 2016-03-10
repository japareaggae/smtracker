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

"""Functions for generating and saving HTML reports using Jinja."""

from collections import namedtuple

from jinja2 import Environment, PackageLoader

import smtracker.utils.format as smformat
import smtracker.utils.parse as parse


def generate(stats, mode, difficulties, theme):
    """Generates an HTML file with all the scores from the Stats file.

    Arguments:
    stats        -- an pre-rooted ElementTree of the Stats.xml file
                    (as in 'stats = etree.parse(statsxml).getroot()
    mode         -- the game mode to output scores from
    difficulties -- the difficulties which should be printed
    theme        -- which metrics should be used for printing grades
    """

    if theme == "sm5":
        get_tier = parse.calculate_tier_sm5
        get_grade = smformat.tier_to_grade_sm5
    elif theme == "itg":
        get_tier = parse.calculate_tier_itg
        get_grade = smformat.tier_to_grade_itg
    else:
        print("Error: {} is not a valid theme option".format(theme))
        exit(1)

    # Get profile name from tree
    profile_name = parse.get_profile_name(stats)
    last_played = parse.get_last_played(stats)

    songs = []
    song_tuple = namedtuple('Song', ['group', 'title', 'scores'])
    score_tuple = namedtuple('Score', ['diff', 'grade', 'perc', 'W1', 'W2',
                                       'W3', 'W4', 'W5', 'Miss'])

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
                        grade = get_grade(get_tier(song[step_counter]))
                        percent = "{:.2f}%".format(float(parse.highscore_stat(
                            song[step_counter], "PercentDP")) * 100)
                        timings = parse.highscore_timings(song[step_counter])

                        scores.append(score_tuple(
                            diff=diff,
                            grade=grade,
                            perc=percent,
                            W1=timings['W1'],
                            W2=timings['W2'],
                            W3=timings['W3'],
                            W4=timings['W4'],
                            W5=timings['W5'],
                            Miss=timings['Miss']))

                    except AttributeError:
                        scores.append({'diff': diff})
                    step_counter = step_counter + 1
                else:
                    scores.append({'diff': diff})
            except IndexError:
                scores.append({'diff': diff})

        songs.append(song_tuple(group, title, scores))

    env = Environment(loader=PackageLoader('smtracker', 'templates'))
    template = env.get_template('template.html')
    return(template.render(name=profile_name,
                           last_played=last_played,
                           difficulties=difficulties,
                           songs=songs))

def save(stats, mode, difficulties, theme, dest='/tmp/sm.html'):
    """Saves an HTML file generated with the generate function.

    Arguments:
    stats        -- an pre-rooted ElementTree of the Stats.xml file
                    (as in 'stats = etree.parse(statsxml).getroot()
    mode         -- the game mode to output scores from
    difficulties -- the difficulties which should be printed
    theme        -- which metrics should be used for printing grades
    dest         -- where should the file be saved
    """
    with open(dest, 'w') as filename:
        filename.write(generate(stats, mode, difficulties, theme))

