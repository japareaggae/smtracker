#!/usr/bin/env python3
import os
import xml.etree.ElementTree as etree

DIFFICULTIES = ["Beginner", "Easy", "Medium", "Hard", "Challenge"]
DEBUG = False

# TODO: Implement argparse to read a specific Stats.xml file
# TODO: Try to read the MachineProfile if there's no LocalProfile
# TODO: See if this works properly on both Cygwin and cmd.exe
if os.name == 'posix':
    statsxml = os.environ['HOME'] + "/.stepmania-5.0/Save/LocalProfiles/00000000/Stats.xml"
elif os.name == 'nt':
    statsxml = os.environ['APPDATA'] + "/StepMania 5/Save/LocalProfiles/00000000/Stats.xml"

if DEBUG:
    print("DEBUG: Stats.xml file is " + statsxml)

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
                # AutoPlayed songs don't get scores and raise AttributeErrors when fetching <HighScore>
                try:
                    grade   = Song[step_counter].find("HighScoreList").find("HighScore").find("Grade").text
                    percent = float(Song[step_counter].find("HighScoreList").find("HighScore").find("PercentDP").text) * 100
                    print("+++ {}: {} ({:.2f})".format(diff,grade,percent))
                except AttributeError:
                    print("--- " + diff)
                step_counter = step_counter + 1
            else:
                print("--- " + diff)
        except IndexError:
            print("--- " + diff)

# TODO: Implement outputs (HTML? PyQt?)
