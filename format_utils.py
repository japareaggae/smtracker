
def highscore_stat(step, stat):
    """Receives a <Steps> ElementTree, and returns the specified stat from it's first HighScore.

    May raise a AttributeError if a song has no <HighScore> (raised from ElementTree)
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


def tier_to_grade_sm5(tier):
    """Receives a tier, and converts it to a grade according to SM5 default metrics."""
    grades = {'Failed': 'F',
            'Tier07': 'D',
            'Tier06': 'C',
            'Tier05': 'B',
            'Tier04': 'A',
            'Tier03': 'AA',
            'Tier02': 'AAA',
            'Tier01': 'AAAA'}
    return grades[tier]

def tier_to_grade_itg(tier):
    """Receives a tier, and converts it to a grade according to ITG/Simply Love metrics."""
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
    return grades[tier]

