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
        raise PathException("The two paths dont follow the same branch")
        return
    if not posdiff == nullstr:
        print(posdiff, "p")
        dif[pos] = posdiff
        dif[neg] = None
    else:
        print(negdiff, "n")
        dif[neg] = negdiff
        dif[pos] = None
    return dif

def add( filename):
    job[1] = dict()
    job[1]["tocompile"] = filename

def dojob():
    fr = _compiler.Frame()
    return fr.compile(job[1]["tocompile"], 1)
    
#path_diff("C:\\Users\\Adepitan", "C:\\Users\\Adepitan\\MyPrograms\\WebAidBox")['positive']