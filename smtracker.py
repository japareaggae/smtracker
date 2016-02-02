#!/usr/bin/env python3
import argparse
import os
import xml.etree.ElementTree as etree

DIFFICULTIES = ["Beginner", "Easy", "Medium", "Hard", "Challenge"]

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

# Sets the default location for statsxml.
# TODO: Try to read the MachineProfile if there's no LocalProfile
# TODO: See if this works properly on both Cygwin and cmd.exe
if os.name == 'posix':
    def_statsxml = os.environ['HOME'] + "/.stepmania-5.0/Save/LocalProfiles/00000000/Stats.xml"
elif os.name == 'nt':
    def_statsxml = os.environ['APPDATA'] + "/StepMania 5/Save/LocalProfiles/00000000/Stats.xml"

# We can ask the program to read a specific file using argparse.
parser = argparse.ArgumentParser(description='A StepMania Score Tracker')
parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=def_statsxml,
        help="the Stats.xml file to read (will read from first available StepMania profile if not specified)")
args = parser.parse_args()
statsxml = vars(args)['file']

try:
    tree = etree.parse(statsxml)
    Stats = tree.getroot()
except FileNotFoundError:
    print("ERROR: No Stats.xml found")
    exit(1)

DisplayName    = Stats.find("GeneralData").find("DisplayName").text
LastPlayedDate = Stats.find("GeneralData").find("LastPlayedDate").text
print("Profile name is " + DisplayName)
print("Last played date was " + LastPlayedDate)

for Song in Stats.find("SongScores"):
    Location = Song.attrib['Dir'].split('/')
    Title = Location[2]
    Group = Location[1]
    print(Group + " - " + Title)

    step_counter = 0
    for diff in DIFFICULTIES:
        # IndexError is raised after we reach the final <Step> on the song using step_counter
        try:
            if Song[step_counter].attrib['Difficulty'] == diff:
                try:
                    grade   = highscore_stat(Song[step_counter], "Grade")
                    percent = float(highscore_stat(Song[step_counter], "PercentDP")) * 100
                    print("+++ {}: {} ({:.2f})".format(diff,grade,percent))
                except AttributeError:
                    print("--- " + diff)
                step_counter = step_counter + 1
            else:
                print("--- " + diff)
        except IndexError:
            print("--- " + diff)

# TODO: Implement outputs (HTML? PyQt?)
