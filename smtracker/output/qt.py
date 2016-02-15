#!/usr/bin/env python3
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

import sys

from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QComboBox,
                             QTableWidget, QTableWidgetItem, QHBoxLayout,
                             QVBoxLayout, QApplication)
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as etree

import smtracker.utils.format as smformat
import smtracker.utils.parse as parse


class Viewer(QMainWindow):

    def __init__(self, stats, mode, difficulties, theme):
        """Initializes basic information about the Viewer class."""
        super().__init__()

        # Define our XML tree
        tree = etree.parse(stats)
        self.stats = tree.getroot()

        # Get basic information from the stats
        self.ismachine = self.stats.find("GeneralData").find("IsMachine").text
        self.lastplayed = self.stats.find("GeneralData").find("LastPlayedDate").text
        if self.ismachine == "1":
            self.displayname = "(machine profile)"
        else:
            self.displayname = self.stats.find("GeneralData").find("DisplayName").text

        # Define initial gamemode on combobox
        self.mode = mode

        # Define the difficulties
        self.difficulties = difficulties

        self.theme = theme
        self.initUI()

    def lock_cell(self, cell):
        """Disables editing a QTableWidgetItem."""
        cell.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)

    def init_table(self):
        """Generates a table with the song scores."""
        HEADER = ("Group", "Title", "Beginner", "Easy", "Medium", "Hard",
                  "Challenge")

        if self.theme == 'sm5':
            get_grade = smformat.tier_to_grade_sm5
        elif self.theme == 'itg':
            get_grade = smformat.tier_to_grade_itg
        else:
            print("Error: " + self.theme + " is not a valid theme option")
            exit(1)

        # Create our table
        song_count = len(self.stats.find("SongScores"))
        table = QTableWidget(song_count, 7)

        # Sets the header cells
        for head in HEADER:
            where = HEADER.index(head)
            headeritem = QTableWidgetItem()
            headeritem.setText(head)
            table.setHorizontalHeaderItem(where, headeritem)

        current_row = 0
        for song in self.stats.find("SongScores"):
            current_column = 0

            # Get group and title
            location = song.attrib['Dir'].split('/')

            # Create group cell
            group = QTableWidgetItem(location[1])
            table.setItem(current_row, current_column, group)
            self.lock_cell(group)
            current_column = current_column + 1

            # Create title cell
            title = QTableWidgetItem(location[2])
            table.setItem(current_row, current_column, title)
            self.lock_cell(title)
            current_column = current_column + 1

            step_counter = 0
            for diff in self.difficulties:
                try:
                    if song[step_counter].attrib['Difficulty'] == diff and \
                       song[step_counter].attrib['StepsType'] == self.mode:
                        try:
                            grade = get_grade(parse.highscore_stat(song[step_counter], "Grade"))
                            percent = float(parse.highscore_stat(song[step_counter], "PercentDP")) * 100
                            cell = QTableWidgetItem('{} ({:.2f}%)'.format(grade, percent))

                            # Get the timings for our song
                            timings = parse.highscore_timings(song[step_counter])

                            # TODO: Figure out if there's a cleaner way of
                            # doing this
                            tooltip = """Marvelous: {}
Perfect: {}
Great: {}
Good: {}
Boo: {}
Miss: {}""".format(timings[5], timings[4], timings[3], timings[2], timings[1],
                   timings[0])
                            cell.setToolTip(tooltip)
                            self.lock_cell(cell)
                            table.setItem(current_row, current_column, cell)
                        except AttributeError:
                            cell = QTableWidgetItem()
                            self.lock_cell(cell)
                            table.setItem(current_row, current_column, cell)
                        step_counter = step_counter + 1
                    else:
                        cell = QTableWidgetItem()
                        self.lock_cell(cell)
                        table.setItem(current_row, current_column, cell)
                except IndexError:
                    cell = QTableWidgetItem()
                    self.lock_cell(cell)
                    table.setItem(current_row, current_column, cell)
                current_column = current_column + 1
            current_row = current_row + 1

        # Final table adjustments
        table.resizeColumnsToContents()
        table.setSortingEnabled(True)
        table.sortByColumn(0, Qt.AscendingOrder)
        return table


    def initUI(self):
        """Initializes the user interface."""
        #MODES = ("dance-single", "dance-double", "pump-single", "pump-double")

        # Combobox for game modes
        #combobox = QComboBox()
        #combobox.addItems(MODES)
        #combobox.setCurrentText(self.mode)
        #combolabel = QLabel("Game mode:")

        #hbox = QHBoxLayout()
        #hbox.addWidget(combolabel)
        #hbox.addWidget(combobox, 1)
        vbox = QVBoxLayout()
        #vbox.addLayout(hbox)
        vbox.addWidget(self.init_table())

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)

        self.statusBar().showMessage('Profile: {} // Last played: {}'.format(
            self.displayname, self.lastplayed))
        self.setWindowTitle('smtracker - StepMania Score Tracker')
        self.setGeometry(48, 48, 1200, 700)
        self.show()


def run(stats, mode, difficulties, theme):
    app = QApplication(sys.argv)
    view = Viewer(stats, mode, difficulties, theme)
    sys.exit(app.exec_())
