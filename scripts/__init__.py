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

console.aware("SLEDGE -- NAIL 'EM ALL!")

nullstr = ""

basespace = workshop = nullstr

ignore = ()
_filter = ()
conf = ".framerc"
ext = ".html"

n = "\n"

status = ["I'm sorry it failed. Check to see if you left \
some nails in your pocket", "you nailed 'em all!"]


_ptrns = [r"(?:\..+)$", r"([ \t]*)\$\{FRAME::BODY\}", 
         r"[ \t]*\$\{FRAME::BODY\}", r"\$\{FRAME::TITLE\}", 
         r"\$\{FRAME::BODY\}", r"\$\{FRAME::LASTMOD\}", 
         r"\$\{FRAME::METAS::%s\}"]


feedout = nullstr


class Mode:
    def __init__(self):
        pass
    DIR_MODE = compiler.Frame.DIR_MODE
    FILE_MODE = compiler.Frame.FILE_MODE
    LAYOUT_MODE = compiler.Frame.LAYOUT_MODE


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

def render(src, mode=Mode.DIR_MODE):

    if src is None or src == nullstr:
        console.warn("nothing to build")
        return None
    fr = compiler.Frame()
    fr.inform(basespace, workshop)
    return fr.compile(src, mode)

def get_all_files(basedir, ignore=(), _filter=(), ret=False):
    global workshop, feedout, basespace

    ignore = [os.path.join(basespace,d) for d in ignore]

    allfiles = os.listdir(basedir)
    dirsOnly = os.listdir(basedir)
    temp = []
    workshop = basedir

    for eachfile in allfiles:
        abs_eachfile = os.path.join(basedir, eachfile)
        if os.path.isfile(abs_eachfile) and not abs_eachfile in ignore:
            temp.append(eachfile)
            dirsOnly.remove(eachfile)
    for i in range(len(_filter)):
        for each in temp:
            if each.endswith(_filter[i]):
                feedout = _build(each, render(os.path.join(basedir, each)), ret)
    for eachdir in dirsOnly:
        abs_eachdir = os.path.join(basedir, eachdir)
        if os.path.isdir(abs_eachdir) and not abs_eachdir in ignore:
            get_all_files(os.path.join(basedir, eachdir), ignore, _filter, ret)
    del allfiles, temp

def _build(filename, response, ret=False):
    if response is None:
        return

    fileo = nfc = None
    dest = cLayoutFrame = genHTMLFile = None

    cMainFrame = response[1]

    if not response[0] is None:
        cLayoutFrame = render(response[0], Mode.LAYOUT_MODE)
    dest = response[2]
    specific = response[3]
    fname = re.sub(_ptrns[0], ext, filename)

    if not ret and not dest is None:
        genHTMLFile = os.path.join(workshop, dest, fname)
    if not cLayoutFrame is None:
        tab = re.search(_ptrns[1], cLayoutFrame).group(1) #search the current tab order
        cMainFrame = _doTabs(cMainFrame, tab) #pad tabs according to tab order
    
        nfc = re.sub(_ptrns[2], cMainFrame, cLayoutFrame) #layout body
        nfc = re.sub(_ptrns[3], specific["title"], nfc) #page title
        nfc = specifics(nfc, specific["meta"]) #page meta tags
    else:
        nfc = cMainFrame

    if ret or not genHTMLFile:
        # if yo ain't meant to
        # write out just feed out
        return nfc

    try:
        fileo = open(genHTMLFile, 'w')
        fileo.write(nfc)
    except IOError as ex:
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
        feedout = _build(os.path.basename(event.src_path), render(event.src_path, Mode.FILE_MODE))
    
    def on_modified(self, event):
        self.vigil(event)

    def on_created(self, event):
        self.vigil(event)



def hammer(workspace=os.path.dirname(__file__), watch=False, ret=False):
    global basespace, feedout

    if os.path.isfile(workspace):
        feedout = _build(os.path.basename(workspace), render(workspace, mode=Mode.FILE_MODE), ret)
        return

    basespace = workspace

    import json
    default_conf = '{"ignore":[],"filter":[".frame"]}'
    confile = os.path.join(workspace, conf)

    framerc = open(confile).read() if os.path.exists(confile) else default_conf
    framerc = json.loads(framerc)
    ignore = tuple(framerc['ignore'])
    _filter = tuple(framerc['filter'])

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
    """ returns the output of the build as text instead of writing out to file
    after calling `sledge.hammer(..., ret=True)`
    then `my_page = sledge.get_build_output()`"""
    return feedout

