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

[sm]: http://www.stepmania.com/
[py3]: https://www.python.org/downloads/windows/
[pyqt5]: https://riverbankcomputing.com/software/pyqt/download5
