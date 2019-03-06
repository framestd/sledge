# Copyright (c) 2019 Caleb Adepitan. All rights reserved.
# Remarkup for HTML, python implementation.
# Sledge v1.0.0.
# Author(s): Caleb Pitan.
# The Remarkup guides that govern this implementation can be found at:
# https://framestd.github.io/sledge/remarkup/
# Developers Indulgent Program (DIP)
# Use of this source code is licensed under the MIT LICENSE
# which can be found in the LICENSE file.

from __future__ import print_function
import os
from . import _compiler
from . import console
nullstr = ""
workspace = nullstr
job = dict()

class PathException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.message = msg
    def log(self):
        print(self.msg)

def path_diff(path, _path):
    drive, path = os.path.splitdrive(path)
    path = os.path.normpath(path).split(os.sep)
    _drive, _path = os.path.splitdrive(_path)
    _path = os.path.normpath(_path).split(os.sep)
    dif = dict()
    pos = "positive"
    neg = "negative"
    posdiff = os.sep.join([
        diff for diff in _path if not diff in path
    ])
    negdiff = os.sep.join([
        diff for diff in path if not diff in _path
    ])
    if posdiff != nullstr and negdiff != nullstr:
        #raise PathException("The two paths don't follow the same branch '%s' '%s'"%(posdiff, negdiff))
        #return
        pass
    if not posdiff == nullstr:
        dif[pos] = posdiff + os.sep
        dif[neg] = None
    else:
        dif[neg] = negdiff + os.sep
        dif[pos] = None
    return dif

def add( filename):
    job[1] = dict()
    job[1]["tocompile"] = filename

def dojob():
    fr = _compiler.Compiler()
    # compile imports
    # imports should have the same mode as layout
    # imports are considered to be a part of the page's layout
    return fr.compile(job[1]["tocompile"], _compiler.Frame.LAYOUT_MODE) # build imports.
    
#path_diff("C:\\Caleb, 
#       "C:\\Caleb\\MyPrograms\\jumper")['positive'] = 
#       'MyPrograms\\jumper'