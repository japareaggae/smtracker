#!/usr/bin/env python3
import xml.etree.ElementTree as etree

# TODO:
# * Implement argparse
# * Implement outputs (HTML? PyQt?)

DIFFICULTIES = ["Beginner", "Easy", "Medium", "Hard", "Challenge"]
DEBUG = False

try:
    tree = etree.parse('Stats.xml')
    Stats = tree.getroot()
    if DEBUG:
        print("DEBUG: Found Stats.xml")
except FileNotFoundError:
    print("No Stats.xml found")
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
                    print("+++ " + diff + ": " + \
                            Song[step_counter].find("HighScoreList").find("HighScore").find("Grade").text + \
                            " (" + Song[step_counter].find("HighScoreList").find("HighScore").find("PercentDP").text + ")")
                except AttributeError:
                    print("--- " + diff)
                step_counter = step_counter + 1
            else:
                print("--- " + diff)
        except IndexError:
            print("--- " + diff)

