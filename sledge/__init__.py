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
from . import _compiler as compiler
from . import console
import os, re, sys

__version__ = 1.0
__all__ = ["render", "hammer", "get_all_files"]
__remarkup_version__ = 'Remarkup X.0'
console.aware("SLEDGE -- NAIL IT ALL!")

nullstr = ""
basespace = workshop = nullstr
ignore = ()
_filter = ()
conf = ".framerc"
fl = ".filter"
ext = ".html"
n = "\n"
status = ["I'm sorry it failed. Check to see if you left \
some nails in your pocket", "you nailed it all!"]
_ptrns = [r"(?:\..+)$", r"([ \t]*)\$\{FRAME::BODY\}", 
         r"[ \t]*\$\{FRAME::BODY\}", r"\$\{FRAME::TITLE\}", 
         r"\$\{FRAME::BODY\}", r"\$\{FRAME::LASTMOD\}", 
         r"\$\{FRAME::METAS::%s\}"]


feedout = nullstr


def recurseAddress(o, x, i=0):
    try:
        return o[x[i]] if i == (len(x) - 1) else recurseAddress(o[x[i]], x, i+1)
    except KeyError:
        console.error("invalid address {}".format(x))

def specifics(frameup, pane):
    allFormat = re.findall(r"([ \t]*)\x24\x7B(.+?)\x7D(?:\x5B([\d*]+)\x5D)?", frameup)
    for tab, each, index in allFormat:
        each_ = each.lstrip().split("::")
        if each_[1] != "METAS":
            each_ = each_[1:]
        else:
            each_ = each_[2:]
        paneValue = recurseAddress(pane, each_, 0)
        if paneValue is None:
            console.error("could not resolve the address \"{}\"".format(each_))
            sys.exit(1)
        if type(paneValue) is list:
            index = str(index)
            index = int(index) if index.isdigit() else index
            ptrn = u"%s\x24\x7B%s\x7D\x5B%s\x5D"%(tab, each, index)
            if index == "*" or index == "":
                paneValue = ", ".join(paneValue)
                paneValue = _doTabs(paneValue, tab)
                frameup = frameup.replace(ptrn, paneValue)
            else:
                paneValue = paneValue[index]
                paneValue = _doTabs(paneValue, tab)
                frameup = frameup.replace(ptrn, paneValue)
        else:
            paneValue = _doTabs(paneValue, tab)
            ptrn = u"%s\x24\x7B%s\x7D"%(tab,each)
            frameup = frameup.replace(ptrn, paneValue)
    return frameup

def render(src, mode=0):
    fr = compiler.Frame()
    fr.inform(basespace, workshop)
    return fr.compile(src, mode)

def get_all_files(basedir, ignore=(), _filter=(), ret=False):
    global workshop, feedout
    allfiles = os.listdir(basedir)
    dirsOnly = os.listdir(basedir)
    temp = []
    workshop = basedir
    for eachfile in allfiles:
        if os.path.isfile(os.path.join(basedir, eachfile)) and not eachfile in ignore:
            temp.append(eachfile)
            dirsOnly.remove(eachfile)
    for i in range(len(_filter)):
        for each in temp:
            if each.endswith(_filter[i]):
                feedout = _build(each, render(os.path.join(basedir, each)), ret)
    for eachdir in dirsOnly:
        if os.path.isdir(os.path.join(basedir, eachdir)) and not eachdir in ignore:
            get_all_files(os.path.join(basedir, eachdir), ignore, filter, ret)
    del allfiles, temp

def _build(filename, response, ret=False):
    cLayoutFrame = render(response[0], 1)
    cMainFrame = response[1]
    dest = response[2]
    specific = response[3]

    fname = re.sub(_ptrns[0], ext, filename)
    genHTMLFile = os.path.join(workshop, dest, fname)

    tab = re.search(_ptrns[1], cLayoutFrame).group(1) #search the current tab order
    fileo = nfc = None

    cMainFrame = _doTabs(cMainFrame, tab) #pad tabs according to tab order
    if cLayoutFrame:
        nfc = re.sub(_ptrns[2], cMainFrame, cLayoutFrame) #layout body
        nfc = re.sub(_ptrns[3], specific["title"], nfc) #page title
        nfc = specifics(nfc, specific["meta"]) #page meta tags
    else:
        nfc = cMainFrame

    if ret:
        # if yo ain't meant to
        # write out just feed out
        return nfc

    try:
        fileo = open(genHTMLFile, 'w')
        fileo.write(nfc)
    except IOError as ex:
        console.error(ex.message)
    except TypeError as ex:
        console.error(ex.message)
    finally:
        fileo.close()
        check = re.search(_ptrns[4], nfc)
        if check == None:
            console.success(status[1])
            sys.stdout.flush()
        else:
            console.error(status[0])
    return 0

def _doTabs(context=nullstr, tab=nullstr):
    codeframe = False
    lctx = context.split(n)
    nctx = r''
    for each in lctx:
        check = each.lstrip().rstrip()
        codecheck = check.startswith("<pre")
        ncodecheck = check.startswith("</pre") or check.endswith("</pre")
        if not codeframe:
            nctx += "%s%s\n"%(tab,each)
        else:
            nctx += "%s\n"%(each)
        if codecheck:
            codeframe = True
        if ncodecheck:
            codeframe = False
        
    return nctx.rstrip()

def _metas(x, c):
    if type(x) is str:
        yield re.sub(_ptrns[6]%(r".+?"), x, c)
        return
    for key, value in x.items():
        # del x[key] #commented out for Py 3 RuntimeError: dictionary changed size during iteration
        if not value:
            yield nullstr
            return
        c = re.sub(_ptrns[6]%key, value, c)
        yield c


from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
class Vigilante(PatternMatchingEventHandler):
    patterns = list(_filter).append("*.yml")

    def vigil(self, event):
        feedout = _build(None, os.path.basename(event.src_path), render(event.src_path))
    
    def on_modified(self, event):
        self.vigil(event)

    def on_created(self, event):
        self.vigil(event)



def hammer(workspace=os.path.dirname(__file__), watch=False, ret=False):
    global basespace
    if os.path.isfile(workspace):
        feedout = _build(os.path.basename(workspace), render(workspace), ret)
        
    basespace = workspace
    import json
    framerc = os.path.join(workspace,conf)
    framerc = open(igpath).read() if os.path.exists(igpath) else '{}'
    framerc = json.loads(framerc)
    ignore = (framerc['ignore'])
    _filter = (framerc['filter'])
    get_all_files(workspace, ignore, _filter, ret)

    if watch:
        ob = Observer()
        ob.schedule(Vigilante(), path=workspace)
        ob.start()
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            ob.stop()
            sys.exit(1)
        ob.join()

def get_build_output():
    """ returns the output of the build as text instead of writing out to file"""
    return feedout

