smtracker - StepMania Score Tracker
=====

smtracker is a simple [StepMania][sm] score tracker written in Python.
It works by parsing your Stats.xml file.

Screenshot (Qt)
-----
![A screenshot of smtracker showing scores from the default songs of
StepMania 5](http://i.imgur.com/jANOutM.png)

Requirements
-----

You will need Python 3 and PyQt5. If you're on Windows, you will need
[Python 3.4][py3] in order to install [PyQt5][pyqt5]. If you're using
GNU/Linux, just install both Python 3 and PyQt5 from your distro's
package repository.

Known Issues
-----

* The Stats.xml file does not know any information about a song, except
where it's located. This means some songs (especially songs with
Japanese titles) will not appear with the same title as in game.

[sm]: http://www.stepmania.com/
[py3]: https://www.python.org/downloads/windows/
[pyqt5]: https://riverbankcomputing.com/software/pyqt/download5
