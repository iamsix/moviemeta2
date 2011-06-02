from distutils.core import setup
import py2exe

setup(
    console=['main.py'],
    options={
        'py2exe': 
        {
            "bundle_files": 3,
            'includes': ['lxml.etree', 'lxml._elementpath', 'BeautifulSoup', 'tools', 'fetchmodules.imdb'],
            "excludes": ["pywin", "pywin.debugger", "pywin.debugger.dbgcon", "pywin.dialogs",
                          "pywin.dialogs.list", "Tkconstants", "Tkinter", "tcl"],

             "optimize": 2,
             
        }
    },
    zipfile = 'lib/libs.zip',
)
