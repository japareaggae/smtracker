import xml.etree.ElementTree as etree

import format_utils


def report(stats_xml, difficulties):
    tree = etree.parse(stats_xml)
    Stats = tree.getroot()
    DisplayName = Stats.find("GeneralData").find("DisplayName").text
    LastPlayedDate = Stats.find("GeneralData").find("LastPlayedDate").text
    try:
        print("Profile name is " + DisplayName)
    except TypeError:
        print("Profile name is unknown")

    print("Last played date was " + LastPlayedDate)

    for Song in Stats.find("SongScores"):
        Location = Song.attrib['Dir'].split('/')
        Title = Location[2]
        Group = Location[1]
        print(Group + " - " + Title)

        step_counter = 0
        for diff in difficulties:
            # IndexError is raised after we reach the final <Step> on the song
            # using step_counter
            try:
                if Song[step_counter].attrib['Difficulty'] == diff:
                    try:
                        grade = format_utils.tier_to_grade_sm5(format_utils.highscore_stat(Song[step_counter], "Grade"))
                        percent = float(format_utils.highscore_stat(Song[step_counter], "PercentDP")) * 100
                        print('+++ {:10}: {:3} ({:.2f})'.format(diff, grade, percent))
                    except AttributeError:
                        print("--- " + diff)
                    step_counter = step_counter + 1
                else:
                    print("--- " + diff)
            except IndexError:
                print("--- " + diff)
