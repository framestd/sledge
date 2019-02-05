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
    
    console.info("status: parsing preprocessors")
    splitframe = frameup.split('\n')
    for each in splitframe:
        pp = re.findall(r'^(?:@)(\w+):\s*?(.*)', each)
        if pp is None: break
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