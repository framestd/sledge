import sys
import os
import main
from main import engine

workspace = os.path.abspath(sys.argv[1])
print
titles = dict()
metas = dict()
"""If your specific frames would be large, you'd better use .json
external file, load it and parse it, and return what is needed as
done below"""
titles["index"] = "Time Frame Panes"
metas["index"] = dict()
metas["index"]["desc"] = "Hello, world. This is Frame"
metas["index"]["author"] = "Adepitan Caleb"
def setTitle(self, fname):
    return titles[fname]
def setMetas(self, fname):
    return metas[fname]
"""Whatever method is set to override the `TITLE` and `METAS` function 
of the MyFrame class should have room enough for two parameters.
Which are:
    (1) the MyFrame instance -- self
        and 
    (2) the relative path of the currently processed file -- fname
        e.g /users/frame/getstarted[.frame]->
        Note: the extension as in the bracket will be removed"""
engine.MyFrame.TITLE = setTitle
engine.MyFrame.METAS = setMetas
engine.buildall(workspace)
