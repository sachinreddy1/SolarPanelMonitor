from setuptools import setup

APP = ['SolarPanelMonitor.py']
DATA_FILES = ['sync.png']
OPTIONS = {
 'iconfile':'logoapp.icns',
 'argv_emulation': True,
 'packages': ['certifi'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
