smtracker - StepMania Score Tracker
=====

smtracker is a simple [StepMania][sm] score tracker written in Python.
It works by parsing your Stats.xml file.

In the future, it will show your stats as a HTML page, or in a PyQt GUI.

Known Issues
-----

* The Stats.xml file does not know any information about a song, except
where it's located. This means some songs (especially songs with
Japanese titles) will not appear with the same title as in game.

[sm]: http://www.stepmania.com/
