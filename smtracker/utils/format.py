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
    # If we don't have the specified tier in this list, it's probably from
    # an ITG-based theme and should be handled accordingly
    try:
        return grades[tier]
    except KeyError:
        return tier_to_grade_itg(tier)


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
    # If we don't have the specified tier in this list, then we have a
    # mysterious theme in our hands
    try:
        return grades[tier]
    except KeyError:
        return "?"
