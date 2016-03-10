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
    """Returns a dict with the timings of the first HighScore of a Steps
    ElementTree.

    Arguments:
    step -- the Steps ElementTree to search
    """
    notes = step.find("HighScoreList").find("HighScore").find("TapNoteScores")
    timings = {'Miss': int(notes.find("Miss").text),
               'W5': int(notes.find("W5").text),
               'W4': int(notes.find("W4").text),
               'W3': int(notes.find("W3").text),
               'W2': int(notes.find("W2").text),
               'W1': int(notes.find("W1").text),
               'HitMine': int(notes.find("HitMine").text)}
    return timings


def highscore_holds(step):
    """Returns a dict with the HoldNoteScores of the first HighScore of a
    Steps ElementTree.

    Arguments:
    step -- the Steps ElementTree to search
    """
    notes = step.find("HighScoreList").find("HighScore").find("HoldNoteScores")
    timings = {'Held': int(notes.find("Held").text),
               'LetGo': int(notes.find("LetGo").text)}
    return timings


def calculate_tier_sm5(step):
    """Calculates a tier for the first HighScore in a Steps ElementTree, using
    StepMania 5's default metrics.

    Arguments:
    step -- the Steps ElementTree to search
    """
    # Here's an explanation of how StepMania calculates its grades:
    # https://zenius-i-vanisher.com/v5.2/viewthread.php?threadid=6582#p349466

    # If the file says we failed, then we failed
    if highscore_stat(step, "Grade") == "Failed":
        return "Failed"

    # Values for each timing
    note_values = {'Miss': -8,
                   'W5': -4,
                   'W4': 0,
                   'W3': 1,
                   'W2': 2,
                   'W1': 2}

    # Calculate our grades
    timings = highscore_timings(step)

    # Notecount for a song
    note_count = (timings['Miss'] + timings['W5'] + timings['W4'] + timings['W3'] +
                  timings['W2'] + timings['W1'])

    # Maximum amount of points we can score on a song
    max_points = note_values['W1'] * note_count

    # How many points we scored on a song
    point_count = (timings['Miss'] * note_values['Miss'] +
                   timings['W5'] * note_values['W5'] +
                   timings['W4'] * note_values['W4'] +
                   timings['W3'] * note_values['W3'] +
                   timings['W2'] * note_values['W2'] +
                   timings['W1'] * note_values['W1'])

    points = point_count/max_points

    if points >= 1.0:
        # AAAA is Marvelous Full Combo, AAA is Perfect Full Combo
        if timings['W2'] >= 1:
            tier = "Tier02"
        else:
            tier = "Tier01"
    elif points >= 0.93:
        tier = "Tier03"
    elif points >= 0.80:
        tier = "Tier04"
    elif points >= 0.65:
        tier = "Tier05"
    elif points >= 0.45:
        tier = "Tier06"
    else:
        tier = "Tier07"
    return tier


def calculate_tier_itg(step):
    """Calculates a tier for the first HighScore in a Steps ElementTree, using
    ITG/Simply Love's default metrics.

    Arguments:
    step -- the Steps ElementTree to search
    """
    # If the file says we failed, then we failed
    if highscore_stat(step, "Grade") == "Failed":
        return "Failed"

    # Values for each timing
    note_values = {'Miss': -12,
                   'W5': -6,
                   'W4': 0,
                   'W3': 2,
                   'W2': 4,
                   'W1': 5,
                   'Held': 5,
                   'LetGo': 0,
                   'HitMine': -6}

    # Calculate our grades
    timings = highscore_timings(step)
    hold_timings = highscore_holds(step)

    # Notecount for a song
    note_count = (timings['Miss'] + timings['W5'] + timings['W4'] + timings['W3'] +
                  timings['W2'] + timings['W1'] + hold_timings['Held'] +
                  hold_timings['LetGo'])

    # Maximum amount of points we can score on a song
    max_points = note_values['W1'] * note_count

    # How many points we scored on a song
    point_count = (timings['Miss'] * note_values['Miss'] +
                   timings['W5'] * note_values['W5'] +
                   timings['W4'] * note_values['W4'] +
                   timings['W3'] * note_values['W3'] +
                   timings['W2'] * note_values['W2'] +
                   timings['W1'] * note_values['W1'] +
                   timings['HitMine'] * note_values['HitMine'] +
                   hold_timings['Held'] * note_values['Held'] +
                   hold_timings['LetGo'] * note_values['LetGo'])

    points = point_count/max_points

    if points >= 1.00:
        tier = "Tier01"
    elif points >= 0.99:
        tier = "Tier02"
    elif points >= 0.98:
        tier = "Tier03"
    elif points >= 0.96:
        tier = "Tier04"
    elif points >= 0.94:
        tier = "Tier05"
    elif points >= 0.92:
        tier = "Tier06"
    elif points >= 0.89:
        tier = "Tier07"
    elif points >= 0.86:
        tier = "Tier08"
    elif points >= 0.83:
        tier = "Tier09"
    elif points >= 0.80:
        tier = "Tier10"
    elif points >= 0.96:
        tier = "Tier11"
    elif points >= 0.72:
        tier = "Tier12"
    elif points >= 0.68:
        tier = "Tier13"
    elif points >= 0.64:
        tier = "Tier14"
    elif points >= 0.60:
        tier = "Tier15"
    elif points >= 0.55:
        tier = "Tier16"
    else:
        tier = "Tier17"
    return tier
