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

from __future__ import print_function
import re
import json
import os
import io

FrameInst = FrameClass = None
workspace = dest = ""

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
    except IOError:
        print("Could not open pane at %s"%src)
    finally:
        panefile.close()
    return json.loads(panecontent, encoding="utf-8") if not panecontent is None else None

def gen(arg):
    for i in xrange(len(arg)):
        yield i

def usegen(arg):
    for i in gen(arg):
        load_pp = re.findall(r'^(?:@)(\w+?):\s*?(.*)', arg[i])
        yield load_pp

def parsepreprocessor(frameup, cb):
    splitframe = frameup.split('\n') 
    for pp in usegen(splitframe):
        for tag, attr in pp:
            cb(tag, attr.lstrip())

def getAttribute(attr, _collection):
    rel = ''
    rel = re.search(r'%s-\"(.*?)\"'%attr, _collection, re.I).group(1)
    return rel

def processor(tag, attr):
    global __panenotfound__, __destinationunresolved__
    if tag.lower() == "load":
        rel = getAttribute('rel', attr).lstrip().lower()
        src = ""
        if rel == "panes":
            src = getAttribute('src', attr)
            if not os.path.isabs(src):
                src = realpath(workspace, src)
            pane = dict()
            if os.path.isfile(src):
                pane.update(loadpane(src))
            else:
                __panenotfound__ = True
            FrameInst.storepane(pane)
        elif rel == "dest":
            dest = getAttribute('href', attr)
            if not os.path.isabs(dest):
                dest = realpath(workspace, dest)
            if os.path.isdir(dest):
                pass
            else:
                try:
                    os.mkdir(dest)
                except OSError as ex:
                    __destinationunresolved__ = True
            FrameInst.dest = dest
        elif rel == "layout":
            src = getAttribute('src', attr)
            if not os.path.isabs(src):
                src = realpath(workspace, src)
            FrameClass.linkedLayoutFrame = FrameInst.compile(src , 1, 1)
        else:
            pass

def realpath(workspace, path):
    if not os.path.isabs(path):
        path = os.path.join(workspace, path, '')
        return os.path.normpath(path)