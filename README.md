smtracker - StepMania Score Tracker
=====

smtracker is a simple [StepMania][sm] score tracker written in Python.
It works by parsing your Stats.xml file.

Screenshot (Qt interface)
-----
![A screenshot of smtracker showing scores from the default songs of
StepMania 5](http://i.imgur.com/8vgRkx7.png)

Screenshot (HTML report)
-----
![A screenshot from a HTML report generated by smtracker](http://i.imgur.com/PWXrLNd.png)

Requirements
-----

* Python 3
* PyQt5
* Jinja2

Windows Tips
-----

You can install PyQt5 for Windows from [Riverbank's website][pyqt5].
It was built against Python 3.4, so make sure to download the correct
version on the [Python website][py3].

Known Issues
-----

* The Stats.xml file does not know any information about a song, except
where it's located. This means some songs (especially songs with
Japanese titles) will not appear with the same title as in game.

License
-----

smtracker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

smtracker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with smtracker.  If not, see <http://www.gnu.org/licenses/>.

[sm]: http://www.stepmania.com/
[py3]: https://www.python.org/downloads/windows/
[pyqt5]: https://riverbankcomputing.com/software/pyqt/download5
