import sys
import os.path

base = os.path.dirname(os.path.abspath(sys.argv[0]))
base = os.path.join(base, 'lib/python2.6/')
sys.path.append(base)

import builder
