# Copyright (c) 2019 Caleb Adepitan. All rights reserved.
# Remarkup for HTML, python implementation.
# Sledge v1.0.0.
# Author(s): Caleb Pitan.
# The Remarkup guides that govern this implementation can be found at:
# https://framestd.github.io/sledge/remarkup/
# Developers Indulgent Program (DIP)
# Use of this source code is licensed under the MIT LICENSE
# which can be found in the LICENSE file.

# -*- coding: utf-8 -*-

from __future__ import print_function
from . import _compiler as compiler
from . import console
import os, re, sys

__version__ = (1, 0)
__all__ = ["render", "hammer", "get_all_files", "get_build_output", "Mode", "Remarkup"]

class Remarkup:
    def __init__(self):
        pass
    __version__ = (1, 0)

console.aware("Frame Studios -- Sledge")

nullstr = ""

should_return = False
# root      # curdir
basespace = workshop = nullstr

framerc = {}
ignore = ()
_filter = ()

confile = ".framerc"
ext = ".html"
n = "\n"

status = ["sorry it failed. Check to see if you left \
some nails in your pocket", "completed"]

Indexer = None
_mode = None

_ptrns = [r"(?:\..+)$", r"([ \t]*)\$\{FRAME::BODY\}", 
         r"[ \t]*\$\{FRAME::BODY\}", r"\$\{FRAME::TITLE\}", 
         r"\$\{FRAME::BODY\}", r"\$\{FRAME::LASTMOD\}", 
         r"\$\{FRAME::METAS::%s\}"]


feedout = nullstr

# <enum>
class Mode:
    def __init__(self):
        raise TypeError('object of type enum cannot be instatiated')
    DIR_MODE = compiler.Compiler.DIR_MODE
    FILE_MODE = compiler.Compiler.FILE_MODE
    LAYOUT_MODE = compiler.Compiler.LAYOUT_MODE


def recurseAddress(o, x, i=0):
    try:
        return o[x[i]] if i == (len(x) - 1) else recurseAddress(o[x[i]], x, i+1)
    except KeyError:
        console.warn("value at address '{}' is null-string".format(x))
        return None

def specifics(frameup, pane):
    allFormat = re.findall(r"([ \t]*)\x24\x7B(.+?)\x7D(?:\x5B([\d*]+)\x5D)?", frameup)
    for tab, each, index in allFormat:
        each_ = each.lstrip().split("::")
        if each_[1] != "METAS":
            each_ = each_[1:]
        else:
            each_ = ['meta'] + each_[2:]
        paneValue = recurseAddress(pane, each_, 0)
        if paneValue is None:
            console.warn("could not resolve address \"{}\"".format(each))
            paneValue = nullstr
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

def render(src, mode=Mode.DIR_MODE):
    global _mode 
    _mode = mode
    fname = src if mode & 3 else None
    if src is None or src == nullstr:
        console.warn("nothing to build")
        return None
    fr = compiler.Compiler()
    fr.inform(mode, fname, basespace, workshop, framerc)
    return fr.compile(src, mode)

def get_all_files(basedir, ignore=None, _filter=None):
    global workshop, feedout, basespace
    import fnmatch
    if _filter is None or ignore is None:
        # it should never come to this
        raise TypeError("expected filter and ignore to be of type 'list' got 'NoneType'")
    ignore = [os.path.join(basespace, d) for d in ignore]
    ignore = [''] if len(ignore) < 1 else ignore

    allfiles = os.listdir(basedir)
    dirsOnly = os.listdir(basedir)
    temp = []
    workshop = basedir

    for n in range(len(ignore)):
        for eachfile in allfiles:
            abs_eachfile = os.path.join(basedir, eachfile)
            if os.path.isfile(abs_eachfile) and not fnmatch.fnmatch(abs_eachfile, ignore[n]):
                temp.append(eachfile)
                dirsOnly.remove(eachfile)
    for i in range(len(_filter)):
        for each in temp:
            if fnmatch.fnmatch(each, _filter[i]): # allow globs pattern matching
                feedout = _build(each, render(os.path.join(basedir, each)))
    for j in range(len(ignore)):
        for eachdir in dirsOnly:
            abs_eachdir = os.path.join(basedir, eachdir)
            if os.path.isdir(abs_eachdir) and not fnmatch.fnmatch(abs_eachdir, ignore[j]): # allow globs pattern matching
                get_all_files(os.path.join(basedir, eachdir), ignore, _filter) # recurse
    del allfiles, temp # insignificant though

def _build(filename, response):
    global Indexer, _mode
    if _mode == Mode.DIR_MODE:
        Indexer = response['INDEXER']
    if response is None:
        return
    fileo = nfc = None
    dest = cLayoutFrame = genHTMLFile = None
    cMainFrame = response['PAGE']
    if not response['LAYOUT_FILE'] is None:
        cLayoutFrame = render(response['LAYOUT_FILE'], Mode.LAYOUT_MODE)
    dest = response['DEST']
    specific = response['UNIQUE']
    specific['PATH_PREFIX'] = response['PATH_PREFIX']
    fname = re.sub(_ptrns[0], ext, filename)
    if not should_return and not dest is None:
        genHTMLFile = os.path.join(workshop, dest, fname)
    if not cLayoutFrame is None:
        tab = re.search(_ptrns[1], cLayoutFrame).group(1) # query the current tab order
        cMainFrame = _doTabs(cMainFrame, tab) # pad tabs according to tab order
        nfc = re.sub(_ptrns[2], cMainFrame, cLayoutFrame) # layout body
        nfc = re.sub(_ptrns[3], specific["title"], nfc) # page title
        nfc = specifics(nfc, specific) # all defered variables
    else:
        nfc = cMainFrame
    if should_return or not genHTMLFile:
        return nfc
    try:
        fileo = open(genHTMLFile, 'w')
        fileo.write(nfc)
    except IOError as ex:
        console.error("could not open file '{}'".format(genHTMLFile))
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
        ncodecheck = check.startswith("</pre>") or check.endswith("</pre>")
        if ncodecheck:
            codeframe = False
        if not codeframe:
            nctx += "%s%s\n"%(tab,each)
        else:
            nctx += "%s\n"%(each)
        if codecheck:
            codeframe = True
    return nctx.rstrip()

def _metas(x, c):
    if type(x) is str:
        yield re.sub(_ptrns[6]%(r".+?"), x, c)
        return
    for key, value in x.items():
        if not value:
            yield nullstr
            return
        c = re.sub(_ptrns[6]%key, value, c)
        yield c

def hammer(workspace=os.path.dirname(
            os.path.abspath(__file__)), watch=False,
            verbose=False, ret=False):
    global basespace, feedout, should_return
    global framerc, confile, Indexer
    if ret and watch:
        console.error("you can't watch while expecting a return value")
        sys.exit(1)
    if not os.path.exists(workspace):
        console.error('the specified path could not be found')
        sys.exit(3)
    import json
    default_conf = """{
        "ignore":["*.sledge/"],
        "filter":["*.frame"],
        "dest": {
            "path": "../../build",
            "rel_to_pages_root": true
        }
    }"""
    framerc.update(json.loads(default_conf))

    should_return = ret
    if os.path.isfile(workspace):
        basespace = os.path.dirname(workspace)
        feedout = _build(os.path.basename(workspace), render(workspace, mode=Mode.FILE_MODE))
        return
    basespace = workspace

    
    confile = os.path.join(workspace, confile)
    confile = open(confile).read() if os.path.exists(confile) else default_conf
    framerc.update(json.loads(confile))

    ignore = framerc['ignore']
    _filter = framerc['filter']

    get_all_files(workspace, ignore, _filter)

    if watch:
        import watchdog.observers
        from .utils import vigilante

        class callbacks:
            def __init__(self):
                pass
            @staticmethod
            def build(filename, response):
                return _build(filename, response)
            @staticmethod
            def renderer(src, mode):
                return render(src, mode)

        handler = vigilante.Vigilante(_filter, ignore, Indexer, callbacks, Mode)
        path_to_watch = os.path.normpath(os.path.join(workspace, '..'))
        ob = watchdog.observers.Observer()
        ob.schedule(handler, path=path_to_watch, recursive=True)
        ob.start()
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            ob.stop()
            Indexer.close()
            #sys.exit(1)
        ob.join()

def get_build_output():
    """ returns the output of the build as text instead of writing out to file
    after calling `sledge.hammer(..., ret=True)`
    then `my_page = sledge.get_build_output()`"""
    return feedout
