#!/usr/bin/env python

import sys, os
from streamlit import cli as stcli

if __name__ == '__main__':
    os.chdir('/home/manoj/${python_package}/')
    sys.argv = ["streamlit", "run", "TrackISS.py"]
    sys.exit(stcli.main())

