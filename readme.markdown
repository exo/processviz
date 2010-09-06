# Process Visualisation Experiments
Jon Simpson <http://www.jonsimpson.co.uk>

This repository contains components related to visual process-oriented programming, developed as part of my PhD.

## Processes
A tool to allow the visual construction of process networks. Requires Python 2.6 with wxPython, Mako and YAML modules.

To run from python command line:
    python builder.py
    
Day-to-day testing focuses on Mac OS X, but the software has been run on Windows and Linux previously.

Drawing performance is slow on Windows due to the implementation wx uses for GraphicsContext - mitigating this is on the todo list, but it remains a known issue.
    
## Building Mac OS X app bundle
To build a Mac OS X .app for Processes, ensure you have `py2app` installed - instructions [here](http://svn.pythonmac.org/py2app/py2app/trunk/doc/index.html#installation).

Once `py2app` is installed, run it inside the app directory.
    python setup.py py2app --no-strip
    
This will produce a Process.app bundle in `dist`. Building app bundles has only been tested on 10.6 so far.

## Notes
There are other tools and code snippets in this repos which may or may not be functional.
