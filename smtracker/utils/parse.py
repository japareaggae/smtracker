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

import sys
import os
import datetime

def get_profile_location():
    """Returns the directories containing the local and machine profiles."""
    lp_location = "/Save/LocalProfiles/"
    mp_location = "/Save/MachineProfile/"

    if sys.platform.startswith('linux'):
        if os.path.isdir(os.environ['HOME'] + "/.stepmania-5.3"):
            local_profile = os.environ['HOME'] + "/.stepmania-5.3" + lp_location
            machine_profile = os.environ['HOME'] + "/.stepmania-5.3" + mp_location
        elif os.path.isdir(os.environ['HOME'] + "/.stepmania-5.1"):
            local_profile = os.environ['HOME'] + "/.stepmania-5.1" + lp_location
            machine_profile = os.environ['HOME'] + "/.stepmania-5.1" + mp_location
        else:
            local_profile = os.environ['HOME'] + "/.stepmania-5.0" + lp_location
            machine_profile = os.environ['HOME'] + "/.stepmania-5.0" + mp_location

    elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        if os.path.isdir(os.environ['APPDATA'] + "StepMania 5.3"):
            local_profile = os.environ['APPDATA'] + "/StepMania 5.3" + lp_location
            machine_profile = os.environ['APPDATA'] + "/StepMania 5.3" + mp_location
        elif os.path.isdir(os.environ['APPDATA'] + "StepMania 5.1"):
            local_profile = os.environ['APPDATA'] + "/StepMania 5.1" + lp_location
            machine_profile = os.environ['APPDATA'] + "/StepMania 5.1" + mp_location
        else:
            local_profile = os.environ['APPDATA'] + "/StepMania 5.0" + lp_location
            machine_profile = os.environ['APPDATA'] + "/StepMania 5.0" + mp_location

    return (local_profile, machine_profile)


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


def get_session_seconds(stats):
    """Gets the TotalGameplaySeconds from the Stats tree and makes it pretty."""
    return datetime.timedelta(seconds=int(stats.find("GeneralData").find("TotalGameplaySeconds").text))


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
