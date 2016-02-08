smtracker - StepMania Score Tracker
=====

smtracker is a simple [StepMania][sm] score tracker written in Python.
It works by parsing your Stats.xml file.

Screenshot (Qt)
-----
![A screenshot of smtracker showing scores from the default songs of
StepMania 5](http://i.imgur.com/jANOutM.png)

Running
-----

* **On Windows**: Install [Python 3][py3]. Optionally, install [PyQt5][pyqt5]
if you want to use the graphical interface.
* **On GNU/Linux**: Install Python 3 using your distribution's package
manager. Optionally, install PyQt5 if you want to use the graphical
interface.

Known Issues
-----

* The Stats.xml file does not know any information about a song, except
where it's located. This means some songs (especially songs with
Japanese titles) will not appear with the same title as in game.

[sm]: http://www.stepmania.com/
[py3]: https://www.python.org/downloads/windows/
[pyqt5]: https://riverbankcomputing.com/software/pyqt/download5
