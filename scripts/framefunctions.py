import re
import sys
import base64 as b64
import urllib2
from . import console

functions = dict()
framepane = dict()
Frame = None
def recurseAddress(o, x, i=0):
    try:
        return o[x[i]] if i == (len(x) - 1) else recurseAddress(o[x[i]], x, i+1)
    except KeyError:
        pass

def ExportFrameCls(object):
    global Frame
    Frame = object
    return

def sub(pattern, item, where, key):
    return re.sub(pattern, 
    "{}".format(item[key]), 
    where) if key in item else re.sub(pattern, 
    '', where)


def explode(options, arg):
    """The Frame function -- explode:
    This is used to propagate a given string and formatting it with unique Panes.
    It is used for links. For example, navbar links, other navigation links 
    and footer links for an HTML page
    Learn more:
    https://framestd.github.io/remarkup/spec/v1/frame-functions.html#explode"""
    Frame._Frame__RESTRUCTURE = 1
    cond = len(arg) == 3
    temparg = arg[2] if cond else arg[1]
    templateAddress = str(temparg).lstrip().rstrip().split("::")
    #pane = options["WAB-NAV"]["NAV-LINKS"]
    pane = recurseAddress(options, templateAddress, 0)
    
    group = arg[0] if cond else None
    data = arg[1] if cond else arg[0]
    datalist = []
    ndata = None
    index = 0

    if type(pane) is list:
        for item in pane:
            ndata = sub(r'\x24\x7BICON\x7D', item, data, "ICON")
            ndata = sub(r'\x24\x7BTITLE\x7D', item, ndata, "TITLE")
            ndata = sub(r'\x24\x7BHREF\x7D', item, ndata, "HREF")
            datalist.append(ndata)
        return str("".join(datalist))

    for item in pane.values():
        group_pane = list(pane.keys())[index] if cond else ''
        index += 1
        group_ = re.sub(r'\x24\x7BFRAME::GROUP\x7D', group_pane, group) if cond else ''
        datalist.append(group_)

        for i in range(len(item)):
            ndata = sub(r'\x24\x7BICON\x7D', item[i], data, "ICON")
            ndata = sub(r'\x24\x7BTITLE\x7D', item[i], ndata, "TITLE")
            ndata = sub(r'\x24\x7BHREF\x7D', item[i], ndata, "HREF")
            datalist.append((datalist.pop() + ndata))
    return str("".join(datalist))

def getf(options, arg):
    Frame._Frame__RESTRUCTURE = 0
    if len(arg) != 1:
        console.error("read function expected 1 argument {} given".format(len(arg)))
        return
    arg[0] = arg[0].lstrip().rstrip()
    with open(arg[0]) as res:
        return str(res.read())
    return ""

def encodeURI(options, s):
    Frame._Frame__RESTRUCTURE = 0
    safe = "/"
    try:
        safe = s[1]
    except IndexError:
        safe = safe
    encoded = ""
    s = s[0]
    try:
        from urllib import parse # for Python 3
    except ImportError:
        try:
            import urllib as parse # for Python 2
        except ImportError:
            console.error("could not load library \"urllib\"")
            console.error("cannot encode URI")
            sys.exit(1)
    encoded = parse.quote_plus(s, safe=safe)
    return encoded



def invert(options, arg):
    #useful for writing in <pre> and <code> tags without stress.
    try:
        arg[1] = arg[1].lstrip().rstrip()
        if str(arg[1]).isdigit():
            Frame._Frame__RESTRUCTURE = int(arg[1])
        else:
            console.warn("expected a number as the second argument")
            Frame._Frame__RESTRUCTURE = 0
    except IndexError:
        Frame._Frame__RESTRUCTURE = 1
    if len(arg) < 1:
        return
    specialchars = {
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "&": "&amp;amp;" # This is so because of the escape call in _compiler.py, 
                         # this has a meaning in a frame. Check 'entity.py'[ln: 14-30]
    }
    inv = arg[0].rstrip()
    for char, code in specialchars.items():
        inv = inv.replace(char, code)
    return str(inv)

# export functions
functions["explode"] = explode
functions["read"] = getf
functions["code"] = invert
functions["encodeURI"] = encodeURI
