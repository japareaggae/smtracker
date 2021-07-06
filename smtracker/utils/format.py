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

"""Formatting utilities used by outputs."""

import smtracker.utils.score as score

def timing_to_judgment_sm5(timing):
    timings = {'W1':   'Flawless',
               'W2':   'Perfect',
               'W3':   'Great',
               'W4':   'Good',
               'W5':   'Bad',
               'Miss': 'Miss'}
    try:
        return timings[timing]
    except KeyError:
        return "?"


def timing_to_judgment_ddra(timing):
    timings = {'W1':   'Marvelous',
               'W2':   'Perfect',
               'W3':   'Great',
               'W4':   'Good',
               'W5':   'Miss',
               'Miss': 'Miss'}
    try:
        return timings[timing]
    except KeyError:
        return "?"


def timing_to_judgment_supernova2(timing):
    timings = {'W1':   'Marvelous',
               'W2':   'Perfect',
               'W3':   'Great',
               'W4':   'Good',
               'W5':   'Boo',
               'Miss': 'Miss'}
    try:
        return timings[timing]
    except KeyError:
        return "?"


def timing_to_judgment_itg(timing):
    timings = {'W1':   'Fantastic',
               'W2':   'Excellent',
               'W3':   'Great',
               'W4':   'Decent',
               'W5':   'Way Off',
               'Miss': 'Miss'}
    try:
        return timings[timing]
    except KeyError:
        return "?"


def timing_to_judgment_iidx(timing):
    timings = {'W1':   'PGreat',
               'W2':   'Great',
               'W3':   'Good',
               'W4':   'Bad',
               'W5':   'Bad',
               'Miss': 'Poor'}
    try:
        return timings[timing]
    except KeyError:
        return "?"


def get_judgment_name(theme, timing):
    """TODO"""
    if theme == "sm5":
        return timing_to_judgment_sm5(timing)
    if theme == "ddra":
        return timing_to_judgment_ddra(timing)
    if theme == "supernova2":
        return timing_to_judgment_supernova2(timing)
    if theme == "itg":
        return timing_to_judgment_itg(timing)
    if theme == "iidx":
        return timing_to_judgment_iidx(timing)


def tier_to_grade_sm5(tier):
    """Converts a tier to a grade according to SM5 default metrics."""
    grades = {'Failed': 'F',
              'Tier07': 'D',
              'Tier06': 'C',
              'Tier05': 'B',
              'Tier04': 'A',
              'Tier03': 'AA',
              'Tier02': 'AAA',
              'Tier01': 'AAAA'}
    try:
        return grades[tier]
    except KeyError:
        return "?"


def tier_to_grade_itg(tier):
    """Converts a tier to a grade according to ITG/Simply Love metrics."""
    grades = {'Failed': 'F',
              'Tier17': 'D',
              'Tier16': 'C-',
              'Tier15': 'C',
              'Tier14': 'C+',
              'Tier13': 'B-',
              'Tier12': 'B',
              'Tier11': 'B+',
              'Tier10': 'A-',
              'Tier09': 'A',
              'Tier08': 'A+',
              'Tier07': 'S-',
              'Tier06': 'S',
              'Tier05': 'S+',
              'Tier04': '★',
              'Tier03': '★★',
              'Tier02': '★★★',
              'Tier01': '★★★★'}
    try:
        return grades[tier]
    except KeyError:
        return "?"


def tier_to_grade_supernova2(tier):
    """Converts a tier to a grade according to DDR SuperNOVA2 default metrics."""
    grades = {'Failed': 'E',
              'Tier06': 'D',
              'Tier05': 'C',
              'Tier04': 'B',
              'Tier03': 'A',
              'Tier02': 'AA',
              'Tier01': 'AAA'}
    try:
        return grades[tier]
    except KeyError:
        return "?"


def tier_to_grade_ddra(tier):
    """Converts a tier to a grade according to DDR A default metrics."""
    grades = {'Failed': 'E',
              'Tier15': 'D',
              'Tier14': 'D+',
              'Tier13': 'C-',
              'Tier12': 'C',
              'Tier11': 'C+',
              'Tier10': 'B-',
              'Tier09': 'B',
              'Tier08': 'B+',
              'Tier07': 'A-',
              'Tier06': 'A',
              'Tier05': 'A+',
              'Tier04': 'AA-',
              'Tier03': 'AA',
              'Tier02': 'AA+',
              'Tier01': 'AAA'}
    try:
        return grades[tier]
    except KeyError:
        return "?"
def tier_to_grade_iidx(tier):
    """Converts a tier to a grade according to beatmania IIDX default metrics."""
    grades = {'Failed': 'F',
              'Tier08': 'F',
              'Tier07': 'E',
              'Tier06': 'D',
              'Tier05': 'C',
              'Tier04': 'B',
              'Tier03': 'A',
              'Tier02': 'AA',
              'Tier01': 'AAA'}
    try:
        return grades[tier]
    except KeyError:
        return "?"


def highscore_grade(step, system):
    """Returns a grade for a tier, based on the defined grading system."""
    grade = "?"
    if system == "sm5":
        grade = tier_to_grade_sm5(score.calculate_tier_sm5(step))
    elif system == "itg":
        grade = tier_to_grade_itg(score.calculate_tier_itg(step))
    elif system == "supernova2":
        grade = tier_to_grade_supernova2(score.calculate_tier_supernova2(step))
    elif system == "ddra":
        grade = tier_to_grade_ddra(score.calculate_tier_ddra(step))
    elif system == "iidx":
        grade = tier_to_grade_iidx(score.calculate_tier_iidx(step))
    else:
        print("{} is not a valid grading system.".format(system))
        exit(1)
    return grade
