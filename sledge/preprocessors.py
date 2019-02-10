# Copyright 2019 Frame Studios. All rights reserved.
# Remarkup v1.0 python implementation.
# Sledge v1.0.
# Project Manager: Caleb Adepitan.
# The Remarkup specifications that govern this implementation can be found at:
# https://framestd.github.io/remarkup/spec/v1/
# Developers Indulgent Program (DIP)
# Use of this source code is licensed under the MIT LICENSE
# which can be found in the LICENSE file.

from __future__ import print_function
import re
import yaml
import os
import io
from . import console
FrameInst = FrameClass = None
workspace = dest = ""
exports = {
    "pane": None,
    "layout": None,
    "dest": None,
    "specific": None
}

__panenotfound__ = False
__destinationunresolved__ = False

def setFrameInst(object):
    global FrameInst
    FrameInst = object

def ExportFrameCls(object):
    global FrameClass
    FrameClass = object

def loadpane(src):
    panefile = panecontent = None
    try:
        panefile = io.open(src, encoding="utf-8")
        panecontent = panefile.read()
        console.info("status: opening \"{}\"".format(src))
    except IOError:
        console.error("Could not open pane at \"{}\"".format(src))
    finally:
        panefile.close()
        console.info("status: parsing \"{}\"".format(src))
    return yaml.load(panecontent) if not panecontent is None else None

def parsepreprocessor(frameup, cb, mode):
    import sys
    console.info("status: parsing preprocessors")
    splitframe = frameup.split('\n')
    for each in splitframe:
        pp = []
        pp = re.findall(r'^(?:@)(\w+):\s*(.*)', each)
        check = re.match(r"^\s*<![\w-]+", each)
        if check is not None and len(pp) == 0:
            continue
        elif check is None and len(pp) == 0:
            break
        else:
            pass
        for tag, attrs in pp:
            cb(tag, attrs.lstrip(), mode)
    return (exports["layout"], exports["pane"], exports["specific"], exports["dest"])

def getAttribute(attr, _collection):
    rel = ''
    rel = re.search(r'%s-\"(.*?)\"'%attr, _collection, re.I).group(1)
    return rel

def processor(tag, attr, mode):
    global __panenotfound__, __destinationunresolved__
    global exports
    if tag.lower() == "load":
        rel = getAttribute('rel', attr).lstrip().lower()
        src = ""
        if rel == "panes":
            src = getAttribute('src', attr)
            src = realpath(workspace, src)
            pane = dict()
            if os.path.isfile(src):
                pane.update(loadpane(src))
            else:
                __panenotfound__ = True
            exports["pane"] = pane
        elif rel == "dest":
            dest = getAttribute('href', attr)
            dest = realpath(workspace, dest)
            if os.path.isdir(dest):
                pass
            else:
                try:
                    os.mkdir(dest)
                except OSError as ex:
                    __destinationunresolved__ = True
            exports["dest"] = dest
        elif rel == "layout":
            if mode:
                console.error("layout cannot have a layout")
                return
            src = getAttribute('src', attr)
            src = realpath(workspace, src)
            exports["layout"] = src
        elif rel == "specific":
            src = getAttribute('src', attr)
            address = getAttribute('find', attr)
            src = realpath(workspace, src)
            pane = dict()
            if os.path.isfile(src):
                pane.update(loadpane(src))
            else:
                __panenotfound__ = True
            exports["specific"] = pane[address]
        else:
            pass
    elif tag.lower() == "import":
        src = getAttribute('src', attr)
        src = realpath(workspace, src)
        assign = getAttribute('as', attr)
        console.info("status: importing \"{}\" as \"{}\"".format(src, assign))
        from . import jobs
        jobs.add(src)
        FrameInst.getpane()[assign] = jobs.dojob()
    else:
        pass

def realpath(workspace, path):
    if not os.path.isabs(path):
        path = os.path.join(workspace, path, '')
        return os.path.normpath(path)
    else: return path