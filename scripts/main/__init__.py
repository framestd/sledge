from __future__ import print_function
from . import _compiler as compiler
from . import console
import os, re

__version__ = 1.0
__all__ = ["render", "hammer", "get_all_files"]
__remarkup_version__ = 'Remarkup X.0'
console.aware("SLEDGE -- NAIL IT ALL!")

nullstr = ""
basespace = workshop = nullstr
ignore = ()
_filter = ()
ig = ".rmignore"
fl = ".filter"
ext = ".html"
n = "\n"
status = ["I'm sorry it failed. Check to see if you left \
some nails in your pocket", "you nailed it all!"]
_ptrns = [r"(?:\..+)$", r"([ \t]*)\$\{FRAME::BODY\}", 
         r"[ \t]*\$\{FRAME::BODY\}", r"\$\{FRAME::TITLE\}", 
         r"\$\{FRAME::BODY\}", r"\$\{FRAME::LASTMOD\}", 
         r"\$\{FRAME::METAS::%s\}"]



def render(src, mode=0):
    fr = compiler.Frame()
    fr.inform(basespace, workshop)
    return fr.compile(src, mode)

def get_all_files(basedir, ignore=(), _filter=()):
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
    for i in range(len(_filter)):
        for each in temp:
            if each.endswith(_filter[i]):
                _build(basedir, each, render(os.path.join(basedir, each)))
    for eachdir in dirsOnly:
        if os.path.isdir(os.path.join(basedir, eachdir)) and not eachdir in ignore:
            get_all_files(os.path.join(basedir, eachdir), ignore, filter)
    del allfiles, temp

def _build(basedir, filename, response):
    cLayoutFrame = render(response[0], 1)
    cMainFrame = response[1]
    dest = response[2]
    specific = response[3]
    fname = re.sub(_ptrns[0], ext, filename)
    genHTMLFile = os.path.join(workshop, dest, fname)
    tab = re.search(_ptrns[1], cLayoutFrame).group(1)
    fileo = nfc = None
    try:
        fileo = open(genHTMLFile, 'w')
        cMainFrame = _doTabs(cMainFrame, tab)
        nfc = re.sub(_ptrns[2], cMainFrame, cLayoutFrame) #layout body
        nfc = re.sub(_ptrns[3], specific["title"], nfc) #page title
        for c in _metas(specific["meta"], nfc): #page meta tags
            nfc = c
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
        else:
            console.error(status[0])
    return 0

def _doTabs(context=nullstr, tab=nullstr):
    lctx = context.split(n)
    nctx = r''
    for each in lctx:
        nctx += "%s%s\n"%(tab,each)
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
        _build(None, os.path.basename(event.src_path), render(event.src_path))
    
    def on_modified(self, event):
        self.vigil(event)

    def on_created(self, event):
        self.vigil(event)



def hammer(workspace=os.path.dirname(__file__), watch=False):
    global basespace
    if os.path.isfile(workspace):
        _build(None, os.path.basename(workspace), render(workspace))
        return
    basespace = workspace
    igpath, flpath = os.path.join(workspace,ig), os.path.join(workspace,fl)
    ignore = open(igpath).read().split(n) if os.path.exists(igpath) else ()
    _filter = open(flpath).read().split(n) if os.path.exists(flpath) else ()
    ignore = tuple(ignore)
    _filter = tuple(_filter)
    get_all_files(workspace, ignore, _filter)

    if watch:
        ob = Observer()
        ob.schedule(Vigilante(), path=workspace)
        ob.start()
        import time
        try:
            while True:
                time.sleep(1)
                """if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')"""
        except KeyboardInterrupt:
            ob.stop()
        ob.join()

