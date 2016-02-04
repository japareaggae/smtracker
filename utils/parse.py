#!/usr/bin/env python3

"""Functions for parsing pieces of stats."""


def highscore_stat(step, stat):
    """Returns a stat from the first HighScore of a Stats ElementTree.

    Will raise an AttributeError if a song has no <HighScore>.
    """
    return step.find("HighScoreList").find("HighScore").find(stat).text


def highscore_timings(step):
    """Receives a <Steps> ElementTree and returns a list with all timings."""
    notes = step.find("HighScoreList").find("HighScore").find("TapNoteScores")
    timings = [int(notes.find("Miss").text),
               int(notes.find("W5").text),
               int(notes.find("W4").text),
               int(notes.find("W3").text),
               int(notes.find("W2").text),
               int(notes.find("W1").text)]
    return timings

# TODO: Should we just calculate tiers and grades by hand?
# It would work better for users who switch themes frequently.
# In case we do, here's an explanation of how StepMania calculates its grades:
# https://zenius-i-vanisher.com/v5.2/viewthread.php?threadid=6582#p349466


