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

"""Functions for calculating scores and grades."""

import smtracker.utils.parse as parse

# TODO: These calculate_tier functions are somewhat naive and may display
# values that don't match with what you see on your game. However, they may be
# useful to convert grades from one system to another, and they prevent issues
# regarding grading systems having a different quantity of tiers.
# Maybe there should be a "don't calculate tier" option that just uses the
# tier on the Stats.xml file.

def calculate_tier_sm5(step):
    """Calculates a tier for the first HighScore in a Steps ElementTree, using
    StepMania 5's default metrics.

    Arguments:
    step -- the Steps ElementTree to search
    """
    # Here's an explanation of how StepMania calculates its grades:
    # https://zenius-i-vanisher.com/v5.2/viewthread.php?threadid=6582#p349466

    # If the file says we failed, then we failed
    if parse.highscore_stat(step, "Grade") == "Failed":
        return "Failed"

    # Values for each timing
    note_values = {'Miss': -8,
                   'W5': -4,
                   'W4': 0,
                   'W3': 1,
                   'W2': 2,
                   'W1': 2}

    # Calculate our grades
    timings = parse.highscore_timings(step)

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
    if parse.highscore_stat(step, "Grade") == "Failed":
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
    timings = parse.highscore_timings(step)
    hold_timings = parse.highscore_holds(step)

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
    elif points >= 0.76:
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

# Here's how SuperNOVA2 calculates scores and grades:
# https://remywiki.com/DanceDanceRevolution_SuperNOVA2_Scoring_System

def calculate_ddr_stepvalue(timings, hold_timings):
    """Calculates the value of a note in a chart using DDR metrics."""

    note_count = (timings['Miss'] + timings['W5'] + timings['W4'] + timings['W3'] +
                  timings['W2'] + timings['W1'] + hold_timings['Held'] +
                  hold_timings['LetGo'])

    # How much each step is worth
    return (1000000 / note_count)


def calculate_score_supernova2(step):
    """Calculates a score for the first HighScore in a Steps ElementTree, using
    DDR SuperNOVA2's scoring system.

    Arguments:
    step -- the Steps ElementTree to search
    """

    # Calculate our grades
    timings = parse.highscore_timings(step)
    hold_timings = parse.highscore_holds(step)

    step_value = calculate_ddr_stepvalue(timings, hold_timings)

    # Calculate the player's score
    score = (step_value * (timings['W1'] + hold_timings['Held']) +
             (step_value - 10) * timings['W2'] +
             ((step_value / 2) - 10) * timings['W3'])

    # Round scores to multiples of 10
    score = int(10 * round(score/10))
    return score


def calculate_score_ddra(step):
    """Calculates a score for the first HighScore in a Steps ElementTree, using
    DDR A's scoring system.

    Arguments:
    step -- the Steps ElementTree to search
    """

    # Calculate our grades
    timings = parse.highscore_timings(step)
    hold_timings = parse.highscore_holds(step)

    step_value = calculate_ddr_stepvalue(timings, hold_timings)

    # Calculate the player's score
    score = (step_value * (timings['W1'] + hold_timings['Held']) +
             (step_value - 10) * timings['W2'] +
             ((step_value / (5/3)) - 10) * timings['W3'] +
             ((step_value / 5) - 10) * timings['W4'])

    # Round scores to multiples of 10
    score = int(10 * round(score/10))
    return score


def calculate_tier_supernova2(step):
    """Calculates a tier for the first HighScore in a Steps ElementTree, using
    DDR SuperNOVA2's scoring system.

    Arguments:
    step -- the Steps ElementTree to search
    """
    # If the file says we failed, then we failed
    if parse.highscore_stat(step, "Grade") == "Failed":
        return "Failed"

    # Get our score
    score = calculate_score_supernova2(step)

    # AAA and AA are always 990000 and 950000, respectively
    if score >= 990000:
        tier = "Tier01"
    elif score >= 950000:
        tier = "Tier02"
    else:
        # Tiers from A to C have flexible score requirements, depending on the
        # difficulty of a chart.
        if (step.attrib['Difficulty'] == "Hard" or
                step.attrib['Difficulty'] == "Challenge"):
            if score >= 900000:
                tier = "Tier03"
            elif score >= 800000:
                tier = "Tier04"
            elif score >= 700000:
                tier = "Tier05"
            else:
                tier = "Tier06"
        elif step.attrib['Difficulty'] == "Medium":
            if score >= 850000:
                tier = "Tier03"
            elif score >= 750000:
                tier = "Tier04"
            elif score >= 600000:
                tier = "Tier05"
            else:
                tier = "Tier06"
        elif (step.attrib['Difficulty'] == "Beginner" or
              step.attrib['Difficulty'] == "Easy"):
            if score >= 800000:
                tier = "Tier03"
            elif score >= 700000:
                tier = "Tier04"
            elif score >= 500000:
                tier = "Tier05"
            else:
                tier = "Tier06"
    return tier


def calculate_tier_ddra(step):
    """Calculates a tier for the first HighScore in a Steps ElementTree, using
    DDR A's scoring system.

    Arguments:
    step -- the Steps ElementTree to search
    """
    # If the file says we failed, then we failed
    if parse.highscore_stat(step, "Grade") == "Failed":
        return "Failed"

    # Get our score
    score = calculate_score_ddra(step)
    if score >= 990000:   # AAA
        tier = "Tier01"
    elif score >= 950000: # AA+
        tier = "Tier02"
    elif score >= 900000: # AA
        tier = "Tier03"
    elif score >= 890000: # AA-
        tier = "Tier04"
    elif score >= 850000: # A+
        tier = "Tier05"
    elif score >= 800000: # A
        tier = "Tier06"
    elif score >= 790000: # A-
        tier = "Tier07"
    elif score >= 750000: # B+
        tier = "Tier08"
    elif score >= 700000: # B
        tier = "Tier09"
    elif score >= 690000: # B-
        tier = "Tier10"
    elif score >= 650000: # C+
        tier = "Tier11"
    elif score >= 600000: # C
        tier = "Tier12"
    elif score >= 590000: # C-
        tier = "Tier13"
    elif score >= 550000: # D+
        tier = "Tier14"
    else:                 # D
        tier = "Tier15"
    return tier

# Some information on how IIDX calculates its grades (section III.B.):
# http://www.gamefaqs.com/ps2/932320-beatmania-iidx-11-iidx-red/faqs/42900
# Also on RemyWiki:
# https://remywiki.com/IIDX_General_Info

def calculate_score_iidx(step):
    """Calculates the EX score for the first HighScore in a Steps ElementTree,
    using beatmania IIDX's grading system.

    Arguments:
    step -- the Steps ElementTree to search
    """
    # Get the timings for the high score
    timings = parse.highscore_timings(step)

    # Get the EX Score
    # TODO: IIDX only defines 5 timing windows, and so does BeatFreeX. Should
    # we merge W1 and W2 and use W3 as the 'worth 1 point' timing window?
    return timings['W1'] * 2 + timings['W2']


def calculate_tier_iidx(step):
    """Calculates a tier for the first HighScore in a Steps ElementTree, using
    beatmania IIDX's grading system.
    This may not be arcade-accurate for songs with hold notes, as IIDX has
    lift notes at the end of each hold note, while StepMania does not (at
    least as of 5.0.11).

    Arguments:
    step -- the Steps ElementTree to search
    """
    # Get the timings for the high score
    timings = parse.highscore_timings(step)

    # Get the EX Score
    ex_score = calculate_score_iidx(step)

    # Maximum EX Score possible in a song
    max_points = 2 * (timings['Miss'] + timings['W5'] + timings['W4'] + timings['W3'] +
                      timings['W2'] + timings['W1'])

    # Calculate percentage
    percentage = ex_score / max_points

    # Calculate tiers
    # You may notice that there's no Failed tier here. This is because in IIDX,
    # passing and failing is largely irrelevant: the arcade will give you a grade
    # even if you fail a song, unlike DDR which always gives you an E.
    if percentage >= 8/9:
        tier = "Tier01"
    elif percentage >= 7/9:
        tier = "Tier02"
    elif percentage >= 6/9:
        tier = "Tier03"
    elif percentage >= 5/9:
        tier = "Tier04"
    elif percentage >= 4/9:
        tier = "Tier05"
    elif percentage >= 3/9:
        tier = "Tier06"
    elif percentage >= 2/9:
        tier = "Tier07"
    else:
        tier = "Tier08"

    return tier
