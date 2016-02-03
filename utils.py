#import xml.etree.ElementTree as etree

def highscore_stat(step, stat):
    """Receives a <Steps> ElementTree, and returns the specified stat from it's first HighScore.

    Keyword arguments:
    step -- the <Steps> ElementTree to search
    stat -- the desired stat from the first <HighScore> on <Steps>

    Returns: string

    Raises:
    AttributeError -- if a song has no <HighScore> (raised from ElementTree)
    """
    return step.find("HighScoreList").find("HighScore").find(stat).text

def tier_to_grade_sm5(tier):
    """Receives a tier, and converts it to a grade according to SM5 default metrics."""
    grade = "F"
    if tier == "Failed":
        grade = "F"
    elif tier == "Tier07":
        grade = "D"
    elif tier == "Tier06":
        grade = "C"
    elif tier == "Tier05":
        grade = "B"
    elif tier == "Tier04":
        grade = "A"
    elif tier == "Tier03":
        grade = "AA"
    elif tier == "Tier02":
        grade = "AAA"
    elif tier == "Tier01":
        grade = "AAAA"
    return grade

