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

from PyQt5.QtWidgets import (QMainWindow, QComboBox, QTableWidget, QHBoxLayout,
        QVBoxLayout, QApplication, QWidget, QLabel, QTableWidgetItem)
from PyQt5.QtCore import Qt
import xml.etree.ElementTree as etree

import utils.format
import utils.parse

class Viewer(QMainWindow):

    def __init__(self, stats, mode, difficulties):
        super().__init__()
        tree = etree.parse(stats)
        self.stats = tree.getroot()
        self.ismachine = self.stats.find("GeneralData").find("IsMachine").text
        self.lastplayed = self.stats.find("GeneralData").find("LastPlayedDate").text

        if self.ismachine == "1":
            self.displayname = "(machine profile)"
        else:
            self.displayname = self.stats.find("GeneralData").find("DisplayName").text

        # Define initial gamemode on combobox
        self.mode = mode

        self.difficulties = difficulties
        self.initUI()

    def lock_cell(self, cell):
        cell.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)

    def initUI(self):
        MODES = ("dance-single", "dance-double", "pump-single", "pump-double")
        HEADER = ("Group", "Title", "Beginner", "Easy", "Medium", "Hard",
                  "Challenge")

        # Combobox for game modes
        combobox = QComboBox()
        combobox.addItems(MODES)
        combobox.setCurrentText(self.mode)
        combolabel = QLabel("Game mode:")

        # Table item prototype
        protocell = QTableWidgetItem()
        protocell.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)

        # Our table
        table = QTableWidget()
        table.setColumnCount(7)
        # Sets the header
        for head in HEADER:
            where = HEADER.index(head)
            headeritem = QTableWidgetItem()
            headeritem.setText(head)
            table.setHorizontalHeaderItem(where, headeritem)

        current_row = 0
        for song in self.stats.find("SongScores"):
            current_column = 0
            table.insertRow(current_row)

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
                            grade = utils.format.tier_to_grade_sm5(utils.parse.highscore_stat(song[step_counter], "Grade"))
                            percent = float(utils.parse.highscore_stat(song[step_counter], "PercentDP")) * 100
                            cell = QTableWidgetItem('{} ({:.2f}%)'.format(grade, percent))

                            # Get the timings for our song
                            timings = utils.parse.highscore_timings(song[step_counter])

                            # Certainly there's a better way to do this, but
                            # I couldn't find any
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

        hbox = QHBoxLayout()
        hbox.addWidget(combolabel)
        hbox.addWidget(combobox, 1)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(table)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)

        self.statusBar().showMessage('Profile: {} // Last played: {}'.format(
            self.displayname, self.lastplayed))
        self.setWindowTitle('smtracker - StepMania Score Tracker')
        self.setGeometry(48, 48, 1200, 700)
        self.show()

def run(stats, mode, difficulties):
    app = QApplication(sys.argv)
    view = Viewer(stats, mode, difficulties)
    sys.exit(app.exec_())

