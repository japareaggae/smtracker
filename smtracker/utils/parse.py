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

"""Functions for parsing pieces of stats."""

def get_profile_name(stats):
    """Gets a profile name from the Stats tree."""
    is_machine = stats.find("GeneralData").find("IsMachine").text
    profile_name = "(unknown)"
    if is_machine == "1":
        profile_name = "(machine profile)"
    else:
        profile_name = stats.find("GeneralData").find("DisplayName").text
    return profile_name


def get_last_played(stats):
    """Gets the LastPlayedDate from the Stats tree."""
    return stats.find("GeneralData").find("LastPlayedDate").text


def highscore_stat(step, stat):
    """Returns a stat from the first HighScore of a Steps ElementTree.

    Arguments:
    step -- the Steps ElementTree to search
    stat -- the stat to return (e.g.: Name, Grade, Modifiers...)

    Will raise an AttributeError if a song has no <HighScore>.
    """
    return step.find("HighScoreList").find("HighScore").find(stat).text


def highscore_timings(step):
    """Returns a list with the timings of the first HighScore of a Steps ElementTree.

    Arguments:
    step -- the Steps ElementTree to search
    """
    notes = step.find("HighScoreList").find("HighScore").find("TapNoteScores")
    timings = {'Miss': int(notes.find("Miss").text),
               'W5': int(notes.find("W5").text),
               'W4': int(notes.find("W4").text),
               'W3': int(notes.find("W3").text),
               'W2': int(notes.find("W2").text),
               'W1': int(notes.find("W1").text)}
    return timings

# TODO: Should we just calculate tiers and grades by hand?
# It would work better for users who switch themes frequently.
# In case we do, here's an explanation of how StepMania calculates its grades:
# https://zenius-i-vanisher.com/v5.2/viewthread.php?threadid=6582#p349466
