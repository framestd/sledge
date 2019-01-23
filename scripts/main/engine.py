# Copyright 2019 Frame Studios. All rights reserved.
# Frame v1.0 python implementation by some Pane-in-the-Frame developers.
# pyFrame v1.0
# Project Manager: Caleb Adepitan
# The Frame specifications that govern this implementation can be found at:
# https://frame.github.io/spec/v1/
# Developers Indulgent Program (DIP)
# Use of this source code is licensed under the GPL 2.0 LICENSE
# which can be found in the LICENSE file.
# In attribution to Realongman, Inc.

import os, sys
from . import compiler
import re
from .compiler import Frame

nullstr = ""
status = ["Build failed", "Build successful"]
layoutFile = workshop = nullstr
ignore = ()
filter = ()
ig = ".frameignore"
fl = ".filter"
ext = ".html"
awaitLayoutFrame = None # await layout frame compilation until layout is defined by pages 
dest = nullstr
_ptrns = [r"(?:\..+)$", r"([ \t]*)\$\{FRAME::BODY\}", 
         r"[ \t]*\$\{FRAME::BODY\}", r"\$\{FRAME::TITLE\}", 
         r"\$\{FRAME::BODY\}", r"\$\{FRAME::LASTMOD\}", 
         r"\$\{FRAME::METAS::%s\}"]
n = "\n"
fr = Frame()

class MyFrame():
    def __init__(self):
        pass
    TITLE =  lambda x, f: f
    METAS = lambda x, f: ""

def cleanup():
    Frame.linkedLayoutFrame = None

def get_all_files(callback, parsedLayoutFrame, basedir, ignore=(), filter=()):
    global workshop
    allfiles = os.listdir(basedir)
    dirsOnly = os.listdir(basedir)
    temp = []
    validfiles = []
    workshop = basedir
    for eachfile in allfiles:
        if os.path.isfile(os.path.join(basedir, eachfile)) and not eachfile in ignore:
            temp.append(eachfile)
            dirsOnly.remove(eachfile)
    for i in range(len(filter)):
        for each in temp:
            if each.endswith(filter[i]):
                if(callback == None):
                    validfiles.append(each)
                else:
                    callback(basedir, each, compile(os.path.join(basedir, each)), parsedLayoutFrame)

    for eachdir in dirsOnly:
        if os.path.isdir(os.path.join(basedir, eachdir)) and not eachdir in ignore:
            get_all_files(callback, parsedLayoutFrame, os.path.join(basedir, eachdir), ignore, filter)
    del allfiles, temp

    if callback == None:
        return validfiles

def compile(framefile):
    global awaitLayoutFrame
    cf = fr.compile(framefile)
    awaitLayoutFrame = Frame.linkedLayoutFrame
    return cf

"""Using this method as a generator -- replacing the `return whatever` with `yield whatever`, 
has made things easier (check line 107). Instead of having it this way:
        ```while True:
               c = metas(MyFrame.METAS(MyFrame(), fr.CURFILE), nfc)
               if c is None:
                   break
               nfc = c```
, and `metas(...)` was just like this:
        ```def metas(x, c):
               if type(x) is str:
                   return re.sub(ptrns[6]%(r".+?"), x, c) 
               for key, value in x.items():
                   del x[key]
                   if not value:
                       return None
                   return re.sub(ptrns[6]%key, value, c)```
The way it is now; "everyone is happy"."""
def metas(x, c):
    if type(x) is str:
        yield re.sub(_ptrns[6]%(r".+?"), x, c)
        return
    for key, value in x.items():
        del x[key]
        if not value:
            yield nullstr
            return
        c = re.sub(_ptrns[6]%key, value, c)
        yield c

def build(basedir, filename, cMainFrame, cLayoutFrame):
    global dest
    dest = fr.dest
    cLayoutFrame = awaitLayoutFrame if awaitLayoutFrame is not None else cLayoutFrame # a layout frame defined on the page overrides the one set generally in the build method.
    fname = re.sub(_ptrns[0], ext, filename)
    genHTMLFile = os.path.join(dest, fname)
    tab = re.search(_ptrns[1], cLayoutFrame).group(1)
    fileo = nfc = None
    try:
        fileo = open(genHTMLFile, 'w')
        cMainFrame = doTabs(cMainFrame, tab)
        nfc = re.sub(_ptrns[2], cMainFrame, cLayoutFrame)
        nfc = re.sub(_ptrns[3], MyFrame.TITLE(MyFrame(), fr.CURFILE), nfc)
        for c in metas(MyFrame.METAS(MyFrame(), fr.CURFILE), nfc):
            nfc = c
        fileo.write(nfc)
    except IOError as ex:
        print ex.message
    except TypeError as ex:
        print ex.message
    finally:
        fileo.close()
        check = re.search(_ptrns[4], nfc)
        if check == None:
            print status[1]
        else:
            print status[0]
    cleanup()
    return 0

def doTabs(context=nullstr, tab=nullstr):
    lctx = context.split(n)
    nctx = r''
    for each in lctx:
        nctx += "%s%s\n"%(tab,each)
    return nctx.rstrip()

def buildall(workspace=os.path.dirname(__file__), layout=None):
    layoutFile = layout
    workshop = workspace
    compiledLayoutFrame = compile(layoutFile) if layout is not None else None
    igpath, flpath = os.path.join(workshop,ig), os.path.join(workshop,fl)
    ignore = open(igpath).read().split(n) if os.path.exists(igpath) else ()
    filter = open(flpath).read().split(n) if os.path.exists(flpath) else ()
    ignore = tuple(ignore)
    filter = tuple(filter)
    get_all_files(build, compiledLayoutFrame, workshop, ignore, filter)
    
