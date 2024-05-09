AlbumsGui
=========

Desktop version of the Albums web application.

The most obvious change is the use of a selector instead of radiobuttons,
so as to make the interface a little more compact.

This repo also includes a simpler GUI interface to several similar databases
that deal with storing music data.

The databases are not included in this repo as they belong to other programs
(notably Banshee, Clementine, Strawberry and my own Albums web app (built with Django).

Another subproject included is a tool derived from the original Albums GUI,
to synchronize the data in Albums with the data in my Music Player library.
In the original version this was WinAmp,
in the current version this is Strawberry.

Usage
-----

Call ``start.py`` to fire up the main program.

Call ``start_gui.py`` to start the simple program.

The synchronize program can be started from within the main program, or by itself through ``python3 albumsmatcher.py``

Requirements
------------

- Python
- PyQt(5)

