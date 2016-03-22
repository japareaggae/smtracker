## Upcoming
### Added

* Qt: Added a menu for selecting a local profile or the machine profile
  if any of those are available in the machine
* Qt: Expose beat game modes on the game mode combobox

### Bugfixes

* Fixed the SuperNOVA2 grading system checking for the wrong difficulties
  (related to the "novice/beginner and expert/challenge" issue)

## v1.4.1 (2016-03-18)
### Changed

* Changelog and desktop file are now included in the source distribution

### Bugfixes

* Revert "Use 'Novice' and 'Expert' instead of 'Beginner' and 'Challenge'"

## v1.4.0 (2016-03-17)
### Added

* Support the SuperNOVA2 grading system ([details on RemyWiki][rw-sn2])

### Changed

* Grades are now calculated by hand instead of being parsed from the
  Stats.xml file ([details on ZIv][ziv-grades])

### Bugfixes

* Use "Novice" and "Expert" instead of "Beginner" and "Challenge"

## v1.3.0 (2016-03-08)
### Added

* Add a desktop file
* Qt: Support for opening a Stats.xml file through the Qt interface
* Qt: Add a combobox for changing grading system

### Changed

* sm5 grading system no longer falls back to itg

## v1.2.2 (2016-02-17)
### Bugfixes

* Fixed HTML templates not being installed by setup.py

## v1.2.1 (2016-02-17)
### Bugfixes

* Fixed HTML templates not being included in the source distribution

## v1.2.0 (2016-02-17)
### Added

* Qt: Added a menu bar
* Support for ignoring difficulties
* HTML output and exporting

## v1.1.0 (2016-02-14)
### Added

* Qt: Added back the game mode combobox, and made it work properly

## v1.0.1 (2016-02-14)
### Removed

* Qt: Removed non-functional game mode combobox

## v1.0.0 (2016-02-14)

* Initial release

[rw-sn2]: https://remywiki.com/DanceDanceRevolution_SuperNOVA2_Scoring_System
[ziv-grades]: https://zenius-i-vanisher.com/v5.2/viewthread.php?threadid=6582#p349466
<!-- vim: set ft=markdown: -->
