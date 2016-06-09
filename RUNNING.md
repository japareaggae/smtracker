Step 1: Get the source code
-----

You can either download a stable release from the [releases page][rels],
or clone the development repository using Git:

`git clone https://github.com/japareaggae/smtracker.git`

Step 2: Install the requirements
-----

smtracker's requirements are [PyQt5][pyqt5] and [Jinja2][jinja2].

On Debian, \*buntu and most derivatives (Substitute `apt` with
`apt-get` if needed):

`apt install python3-pyqt5 python3-jinja2`

On Fedora:

`dnf install python3-qt5 python3-jinja2`

On Windows, first download and install [Python 3.5][pywin], then
download and install [PyQt5][pyqt5-d]. Finally, open a Command Prompt
with Administrator Rights, navigate to the repository root, and ask
pip to install the rest of the requirements (Jinja2):

`pip install -r requirements.txt`

Step 3: Run the program
-----

You should now be able to run smtracker by running the `smtracker.py`
script on the repository root.

[rels]: https://github.com/japareaggae/smtracker/releases
[pyqt5]: https://www.riverbankcomputing.com/software/pyqt/intro
[jinja2]: http://jinja.pocoo.org/
[pywin]: https://www.python.org/downloads/windows/
[pyqt5-d]: https://riverbankcomputing.com/software/pyqt/download5
