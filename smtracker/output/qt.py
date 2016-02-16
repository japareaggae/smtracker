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

"""A Qt-based interface for viewing your scores."""

import sys

from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QComboBox,
                             QTableWidget, QTableWidgetItem, QHBoxLayout,
                             QVBoxLayout, QAction, QMessageBox, qApp,
                             QApplication)
from PyQt5.QtCore import Qt

import smtracker
import smtracker.utils.format as smformat
import smtracker.utils.parse as parse


class Viewer(QMainWindow):
    """The main window for the application."""

    def __init__(self, stats, mode, difficulties, theme):
        """Initializes basic information about the Viewer class."""
        super().__init__()

        # Define our XML tree
        self.stats = stats

        # Get basic information from the stats
        self.displayname = parse.get_profile_name(stats)
        self.lastplayed = parse.get_last_played(stats)

        # Define initial gamemode on combobox
        self.mode = mode

        # Define the difficulties
        self.difficulties = difficulties

        # Create a skeleton table
        song_count = len(self.stats.find("SongScores"))
        self.table = QTableWidget(song_count, len(self.difficulties) + 2)

        self.theme = theme
        self.initUI()


    def lock_cell(self, cell):
        """Disables editing a QTableWidgetItem."""
        cell.setFlags(Qt.ItemIsSelectable and Qt.ItemIsEnabled)


    def init_table(self):
        """Generates a table with the song scores."""
        HEADER = ["Group", "Title"]
        HEADER.extend(self.difficulties)

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

        self.table.clearContents()
        self.table.setSortingEnabled(False)

        # Sets the header cells
        for head in HEADER:
            where = HEADER.index(head)
            headeritem = QTableWidgetItem()
            headeritem.setText(head)
            self.table.setHorizontalHeaderItem(where, headeritem)

        current_row = 0
        for song in self.stats.find("SongScores"):
            current_column = 0

            # Get the song's group and title
            location = song.attrib['Dir'].split('/')

            # Create group cell
            group = QTableWidgetItem(location[1])
            self.table.setItem(current_row, current_column, group)
            self.lock_cell(group)
            current_column = current_column + 1

            # Create title cell
            title = QTableWidgetItem(location[2])
            self.table.setItem(current_row, current_column, title)
            self.lock_cell(title)
            current_column = current_column + 1

            # step_counter will be used for traversing the scores in a song
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
                            self.table.setItem(current_row, current_column, cell)
                        # This exception is reached if a Song was played, but
                        # has no score (AutoPlay, PlayerAutoPlay)
                        except AttributeError:
                            cell = QTableWidgetItem()
                            self.lock_cell(cell)
                            self.table.setItem(current_row, current_column, cell)
                        step_counter = step_counter + 1
                    # If there are no scores for the current difficulty,
                    # add an empty cell instead
                    else:
                        cell = QTableWidgetItem()
                        self.lock_cell(cell)
                        self.table.setItem(current_row, current_column, cell)
                # This exception is reached if we already reached the last
                # score on a song (using step_counter)
                except IndexError:
                    cell = QTableWidgetItem()
                    self.lock_cell(cell)
                    self.table.setItem(current_row, current_column, cell)
                current_column = current_column + 1
            current_row = current_row + 1

        # Final table adjustments
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, Qt.AscendingOrder)


    def combobox_activated(self, combobox):
        """Sets the current game mode and regenerates the table."""
        self.mode = combobox.currentText()
        self.init_table()


    def about_box(self):
        """Shows an about box with information about smtracker."""
        QMessageBox.about(self, "About smtracker", smtracker.__description__ +
                          " (version " + smtracker.__version__ + ")")


    def init_menubar(self):
        """Generates the main window menu bar."""
        exitAction = QAction('E&xit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit smtracker')
        exitAction.triggered.connect(qApp.exit)

        exportAction = QAction('&Export', self)
        exportAction.setShortcut('Ctrl+E')
        exportAction.setStatusTip('Export table as HTML file')
        #exitAction.triggered.connect(lambda: html.output)

        aboutAction = QAction('&About smtracker...', self)
        aboutAction.triggered.connect(self.about_box)

        qtAction = QAction('About &Qt...', self)
        qtAction.triggered.connect(QApplication.aboutQt)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exportAction)
        fileMenu.addAction(exitAction)
        aboutMenu = menubar.addMenu('&About')
        aboutMenu.addAction(aboutAction)
        aboutMenu.addAction(qtAction)

    def initUI(self):
        """Initializes the user interface."""
        MODES = ("dance-single", "dance-double", "pump-single", "pump-double",
                 "pump-halfdouble")

        # Combobox for game modes
        combobox = QComboBox()
        combobox.addItems(MODES)
        combobox.setCurrentText(self.mode)
        combolabel = QLabel("Game mode:")
        combobox.activated.connect(lambda: self.combobox_activated(combobox))

        self.init_menubar()
        self.init_table()

        hbox = QHBoxLayout()
        hbox.addWidget(combolabel)
        hbox.addWidget(combobox, 1)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.table)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)

        status = 'Profile: {} // Last played: {}'.format(self.displayname,
                                                         self.lastplayed)
        self.statusBar().showMessage(status)
        container.setStatusTip(status)
        self.setWindowTitle('smtracker - StepMania Score Tracker')
        self.resize(1200, 700)
        self.show()


def run(stats, mode, difficulties, theme):
    """Runs the user interface."""
    app = QApplication(sys.argv)
    view = Viewer(stats, mode, difficulties, theme)
    sys.exit(app.exec_())
