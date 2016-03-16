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
import xml.etree.ElementTree as etree

from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QComboBox,
                             QTableWidget, QTableWidgetItem, QHBoxLayout,
                             QVBoxLayout, QAction, QMessageBox, QFileDialog,
                             QAbstractItemView, qApp, QApplication)
from PyQt5.QtCore import Qt

import smtracker
import smtracker.utils.format as smformat
import smtracker.utils.parse as parse
import smtracker.output.html as html


class Viewer(QMainWindow):
    """The main window for the application."""

    def __init__(self, stats, mode, difficulties, theme):
        """Initializes basic information about the Viewer class."""
        super().__init__()

        # Define our XML tree
        self.stats = stats

        # Define initial gamemode on combobox
        self.mode = mode

        # Define the difficulties
        self.difficulties = difficulties

        # Create a skeleton table
        if self.stats is not None:
            song_count = len(self.stats.find("SongScores"))
            self.table = QTableWidget(song_count, len(self.difficulties) + 2)
        else:
            self.table = QTableWidget(0, len(self.difficulties) + 2)

        table_header = ["Group", "Title"]
        table_header.extend(self.difficulties)

        # Sets the header cells
        for head in table_header:
            where = table_header.index(head)
            headeritem = QTableWidgetItem()
            headeritem.setText(head)
            self.table.setHorizontalHeaderItem(where, headeritem)

        self.theme = theme
        self.init_ui()


    def init_table(self):
        """Generates a table with the song scores."""

        # Prepare table for inserting items
        self.table.clearContents()
        self.table.setSortingEnabled(False)

        # Current table row
        current_row = 0
        for song in self.stats.find("SongScores"):
            # Current table row
            current_column = 0

            # Get the song's group and title
            # location[0] should always be "Songs"
            location = song.attrib['Dir'].split('/')

            # Create group cell
            group = QTableWidgetItem(location[1])
            self.table.setItem(current_row, current_column, group)
            current_column = current_column + 1

            # Create title cell
            title = QTableWidgetItem(location[2])
            self.table.setItem(current_row, current_column, title)
            current_column = current_column + 1

            # step_counter will be used for traversing the scores in a song
            step_counter = 0
            for diff in self.difficulties:
                try:
                    if song[step_counter].attrib['Difficulty'] == diff and \
                       song[step_counter].attrib['StepsType'] == self.mode:
                        try:
                            grade = smformat.highscore_grade(song[step_counter], self.theme)
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
Miss: {}""".format(timings['W1'], timings['W2'], timings['W3'], timings['W4'],
                   timings['W5'], timings['Miss'])
                            cell.setToolTip(tooltip)
                            self.table.setItem(current_row, current_column, cell)
                        # This exception is reached if a Song was played, but
                        # has no score (AutoPlay, PlayerAutoPlay)
                        except AttributeError:
                            cell = QTableWidgetItem()
                            self.table.setItem(current_row, current_column, cell)
                        step_counter = step_counter + 1
                    # If there are no scores for the current difficulty,
                    # add an empty cell instead
                    else:
                        cell = QTableWidgetItem()
                        self.table.setItem(current_row, current_column, cell)
                # This exception is reached if we already reached the last
                # score on a song (using step_counter)
                except IndexError:
                    cell = QTableWidgetItem()
                    self.table.setItem(current_row, current_column, cell)
                current_column = current_column + 1
            current_row = current_row + 1

        # Final table adjustments
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(0, Qt.AscendingOrder)


    def combobox_activated(self, combobox):
        """Sets the current game mode and regenerates the table."""
        self.mode = combobox.currentText()
        self.init_table()


    def themebox_activated(self, combobox):
        """Sets the current grading system and regenerates the table."""
        self.theme = combobox.currentText()
        self.init_table()


    def about_box(self):
        """Shows an about box with information about smtracker."""

        blurb = "<p>{} (version {})</p>".format(smtracker.__description__,
                                                smtracker.__version__)
        gpl = "<p>Released under the terms of the " + \
              "<a href=\"http://www.gnu.org/licenses/gpl-3.0.html\">GNU " + \
              "General Public License, version 3 or later</a></p>"
        url = "<a href=\"{}\">{}</a></p>".format(smtracker.__url__,
                                                 smtracker.__url__)
        text = blurb + url + gpl
        QMessageBox.information(self, "About smtracker", text)


    def export_html(self):
        """Saves an HTML report using QFileDialog to set a location."""
        filetuple = QFileDialog.getSaveFileName(self, "Save HTML report as",
                                                None, "HTML file (*.html)")

        if filetuple[0]:
            if filetuple[0].endswith(".html"):
                filename = filetuple[0]
            else:
                filename = filetuple[0] + ".html"

            html.save(self.stats, self.mode, self.difficulties, self.theme,
                      filename)


    def open_file(self):
        """Sets a new Stats.xml file and regenerates the table."""
        filetuple = QFileDialog.getOpenFileName(self, "Select Stats.xml file "
                                                "to open", None, "StepMania stats "
                                                "files (*.xml)")
        if filetuple[0]:
            tempstats = etree.parse(filetuple[0]).getroot()
            if tempstats.find("SongScores") is None:
                QMessageBox.critical(self, "Error parsing file", "The selected "
                                     "file is not a valid StepMania Stats.xml "
                                     "file.")
            else:
                self.stats = tempstats
                self.table.setRowCount(len(self.stats.find("SongScores")))
                self.init_table()
                self.set_statusbar()


    def set_statusbar(self):
        """Resets the application statusbar."""
        displayname = parse.get_profile_name(self.stats)
        lastplayed = parse.get_last_played(self.stats)
        status = 'Profile: {} // Last played: {}'.format(displayname,
                                                         lastplayed)
        self.setStatusTip(status)


    def init_menubar(self):
        """Generates the main window menu bar."""
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit smtracker')
        exit_action.triggered.connect(qApp.exit)

        export_action = QAction('&Export...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.setStatusTip('Export table as HTML file')
        export_action.triggered.connect(self.export_html)

        open_action = QAction('&Open...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open a Stats.xml file')
        open_action.triggered.connect(self.open_file)

        about_action = QAction('&About smtracker...', self)
        about_action.triggered.connect(self.about_box)

        qt_action = QAction('About &Qt...', self)
        qt_action.triggered.connect(QApplication.aboutQt)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(export_action)
        file_menu.addAction(exit_action)
        about_menu = menubar.addMenu('&About')
        about_menu.addAction(about_action)
        about_menu.addAction(qt_action)

    def init_ui(self):
        """Initializes the user interface."""
        modes = ("dance-single", "dance-double", "pump-single", "pump-double",
                 "pump-halfdouble")
        themes = ("sm5", "itg")

        # Combobox for game modes
        combobox = QComboBox()
        combobox.addItems(modes)
        combobox.setCurrentText(self.mode)
        combolabel = QLabel("Game mode:")
        combobox.activated.connect(lambda: self.combobox_activated(combobox))

        themebox = QComboBox()
        themebox.addItems(themes)
        themebox.setCurrentText(self.theme)
        themelabel = QLabel("Grading system:")
        themebox.activated.connect(lambda: self.themebox_activated(themebox))

        self.init_menubar()

        if self.stats is not None:
            self.init_table()

        hbox = QHBoxLayout()
        hbox.addWidget(combolabel)
        hbox.addWidget(combobox, 1)
        hbox.addWidget(themelabel)
        hbox.addWidget(themebox, 1)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.table)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)

        self.statusBar()
        if self.stats is not None:
            self.set_statusbar()
        else:
            self.setStatusTip("No Stats.xml file loaded")
        self.setWindowTitle('smtracker - StepMania Score Tracker')
        self.resize(1200, 700)
        self.show()


def run(stats, mode, difficulties, theme):
    """Runs the user interface."""
    app = QApplication(sys.argv)
    Viewer(stats, mode, difficulties, theme)
    sys.exit(app.exec_())
