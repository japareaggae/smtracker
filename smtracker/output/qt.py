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
import os
import xml.etree.ElementTree as etree
import functools
from importlib.resources import files, as_file

from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QComboBox, QLineEdit,
                             QTableWidget, QTableWidgetItem, QHBoxLayout,
                             QVBoxLayout, QAction, QMessageBox, QFileDialog,
                             QAbstractItemView, qApp, QApplication)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

import smtracker
import smtracker.utils.format as smformat
import smtracker.utils.parse as parse
import smtracker.utils.score as score
import smtracker.output.html as html

from smtracker.images import itg, sm5, sm51


class Viewer(QMainWindow):
    """The main window for the application."""

    def __init__(self, stats, mode, difficulties, theme):
        """Initializes basic information about the Viewer class."""
        super().__init__()

        ### Initialize parameters passed from smtracker.py
        self.stats = stats                 # XML tree
        self.mode = mode                   # Gamemode
        self.difficulties = difficulties   # Tracked difficulties
        self.filter = None

        ### Initialize interface options
        self.icons_enabled = True          # Icons

        ### Create an empty table
        if self.stats is not None:
            song_count = len(self.stats.find("SongScores"))
            self.table = QTableWidget(song_count, len(self.difficulties) + 2)
        else:
            self.table = QTableWidget(0, len(self.difficulties) + 2)

        # Set some basic table attributes
        self.table.setIconSize(QSize(32, 32))
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)

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

            if self.filter is not None and self.filter.lower() not in location[2].lower():
                continue

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
                    if (song[step_counter].attrib['Difficulty'] == diff and
                        song[step_counter].attrib['StepsType'] == self.mode):
                        try:
                            grade = smformat.highscore_grade(song[step_counter], self.theme)
                            percent = float(parse.highscore_stat(song[step_counter], "PercentDP")) * 100

                            has_icon = False
                            if self.theme == "sm5" and self.icons_enabled is True:
                                source = files(sm5).joinpath(grade + ".png")
                                has_icon = True
                            elif self.theme == "sm5.1" and self.icons_enabled is True:
                                source = files(sm51).joinpath(grade + ".png")
                                has_icon = True
                            elif self.theme == "itg" and self.icons_enabled is True:
                                source = files(itg).joinpath(grade + ".png")
                                has_icon = True

                            if has_icon is True:
                                cell = QTableWidgetItem('{:.2f}%'.format(percent))
                                with as_file(source) as image:
                                    cell.setIcon(QIcon(str(image)))
                            else:
                                cell = QTableWidgetItem('{} ({:.2f}%)'.format(grade, percent))

                            # Get the timings for our song
                            timings = parse.highscore_timings(song[step_counter])

                            # Generate tooltip
                            tooltip = """{w1}: {w1_count}
{w2}: {w2_count}
{w3}: {w3_count}
{w4}: {w4_count}
{w5}: {w5_count}
{miss}: {miss_count}
Modifiers: {modifiers}
Played: {played}""".format(
        w1=smformat.get_judgment_name(self.theme, 'W1'), w1_count=timings['W1'],
        w2=smformat.get_judgment_name(self.theme, 'W2'), w2_count=timings['W2'],
        w3=smformat.get_judgment_name(self.theme, 'W3'), w3_count=timings['W3'],
        w4=smformat.get_judgment_name(self.theme, 'W4'), w4_count=timings['W4'],
        w5=smformat.get_judgment_name(self.theme, 'W5'), w5_count=timings['W5'],
        miss=smformat.get_judgment_name(self.theme, 'Miss'), miss_count=timings['Miss'],
        modifiers=parse.highscore_stat(song[step_counter], "Modifiers"),
        played=parse.highscore_stat(song[step_counter], "DateTime"))

                            if self.theme == "supernova2":
                                tooltip = tooltip + "\nDDR SN2 Score: {}".format(score.calculate_score_supernova2(song[step_counter]))
                            if self.theme == "ddra":
                                tooltip = tooltip + "\nDDR A Score: {}".format(score.calculate_score_ddra(song[step_counter]))
                            if self.theme == "iidx":
                                tooltip = tooltip + "\nIIDX EX Score: {}".format(score.calculate_score_iidx(song[step_counter]))


                            cell.setToolTip(tooltip)
                            self.table.setItem(current_row, current_column, cell)
                        # This exception is reached if a Song was played, but
                        # has no score (AutoPlay, PlayerAutoPlay)
                        except AttributeError:
                            cell = QTableWidgetItem('[no score]')
                            cell.setTextAlignment(Qt.AlignCenter)
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


    def filterbox_activated(self, filterbox):
        """Filters the table based on the contents of the filterbox."""
        self.filter = filterbox.text()
        self.init_table()


    def about_box(self):
        """Shows an about box with information about smtracker."""

        text = ("<p>{desc} (version {vers})</p>"
                "<p>Released under the terms of the <a href=\"http://www.gnu.org"
                "/licenses/gpl-3.0.html\">GNU General Public License"
                ", version 3 or later</a></p>"
                "<p>Icons provided by <a href=\"http://stepmania.com\">"
                "StepMania</a> under the <a href=\"https://github.com/stepmania"
                "/stepmania/blob/master/Docs/Licenses.txt\">MIT license</a></p>"
                "<p><a href=\"{url}\">{url}</a></p>").format(
                    desc=smtracker.__description__,
                    vers=smtracker.__version__,
                    url=smtracker.__url__)
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


    def set_statusbar(self):
        """Resets the application statusbar."""
        displayname = parse.get_profile_name(self.stats)
        lastplayed = parse.get_last_played(self.stats)
        timeplayed = parse.get_session_seconds(self.stats)
        status = 'Profile: {} // Last played: {} // Total time played: {}'.format(
                displayname, lastplayed, timeplayed)
        self.setStatusTip(status)


    def set_stats(self, stats):
        """Sets a new Stats.xml file and regenerates the UI."""
        self.stats = stats
        self.table.setRowCount(len(self.stats.find("SongScores")))
        self.init_table()
        self.set_statusbar()


    def open_file(self):
        """Opens a QFileDialog to set a new Stats.xml file."""
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
                self.set_stats(tempstats)


    def toggle_icons(self, state):
        """Sets icons_enabled and regenerates the table."""
        self.icons_enabled = state
        self.init_table()

    def init_menubar(self):
        """Generates the main window menu bar."""

        # Creates the actions for the main menu
        ### 'File' menu
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

        ### 'Options' menu
        icons_action = QAction('Enable &icons', self)
        icons_action.setCheckable(True)
        icons_action.setChecked(self.icons_enabled)
        icons_action.triggered.connect(lambda: self.toggle_icons(icons_action.isChecked()))

        ### 'About' menu
        about_action = QAction('&About smtracker...', self)
        about_action.triggered.connect(self.about_box)

        qt_action = QAction('About &Qt...', self)
        qt_action.triggered.connect(QApplication.aboutQt)

        # Creates the menu bar and starts adding items to it
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_action)

        # Create the profile submenu and add the machine profile item
        profile_menu = file_menu.addMenu('Open &profile')
        mp_action = profile_menu.addAction('Machine Profile')

        # Define the location for profiles
        profile_folder, mp_folder = parse.get_profile_location()

        # Check if the machine profile exists
        if os.path.isfile(mp_folder + "Stats.xml") is True:
            no_mp = False
            mp_action.setStatusTip('Open this machine\'s profile')
            machine_profile = etree.parse(mp_folder + "Stats.xml").getroot()
            mp_action.triggered.connect(lambda: self.set_stats(machine_profile))
        else:
            no_mp = True
            mp_action.setEnabled(False)

        # Check if there's any local profiles
        if os.path.isdir(profile_folder) is True:
            no_lp = False
            profile_menu.addSeparator()
            for profile in os.listdir(profile_folder):
                try:
                    tempstats = etree.parse(profile_folder + profile + "/Stats.xml").getroot()
                except FileNotFoundError:
                    continue
                tempname = parse.get_profile_name(tempstats)
                if tempname is None:
                    tempname = "Unknown Name ({path})".format(path=profile)
                action = profile_menu.addAction(tempname)
                function = functools.partial(self.set_stats, tempstats)
                action.triggered.connect(function)
        else:
            no_lp = True

        # If there are no profiles at all, disable profile menu
        if no_mp is True and no_lp is True:
            profile_menu.setEnabled(False)

        # Add the rest of the actions to the menubar
        file_menu.addAction(export_action)
        file_menu.addAction(exit_action)

        options_menu = menubar.addMenu('&Options')
        options_menu.addAction(icons_action)

        about_menu = menubar.addMenu('&About')
        about_menu.addAction(about_action)
        about_menu.addAction(qt_action)

    def init_ui(self):
        """Initializes the user interface."""
        modes = ("dance-single", "dance-double", "pump-single", "pump-double",
                 "pump-halfdouble", "bm-single7", "bm-double7")
        themes = ("sm5", "sm5.1", "itg", "supernova2", "ddra", "iidx")

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

        # Filter text box
        filterlabel = QLabel("Filter titles:")
        filterbox = QLineEdit()
        filterbox.editingFinished.connect(lambda: self.filterbox_activated(filterbox))

        self.init_menubar()

        if self.stats is not None:
            self.init_table()

        hbox = QHBoxLayout()
        hbox.addWidget(combolabel)
        hbox.addWidget(combobox, 1)
        hbox.addWidget(themelabel)
        hbox.addWidget(themebox, 1)

        filterhbox = QHBoxLayout()
        filterhbox.addWidget(filterlabel)
        filterhbox.addWidget(filterbox, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(filterhbox)
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
