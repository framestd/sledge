import re
import sys
from . import console
from .preprocessors import realpath

functions = dict()
framepane = dict()
Framecls = object()
workspace = ''

def recurseAddress(o, x, i=0):
    try:
        return o[x[i]] if i == (len(x) - 1) else recurseAddress(o[x[i]], x, i+1)
    except KeyError:
        pass

def Export(cls):
    global Framecls, workspace
    Framecls = cls
    return

def sub(pattern, item, where, key):
    return re.sub(pattern, 
    "{}".format(item[key]), 
    where) if key in item else re.sub(pattern, 
    '', where)

#########               BEGIN FRAME FUNCTIONS                   ##########

def explode(options, arg):
    """The Frame function -- explode:
    This is used to propagate a given string and formatting it with unique Panes.
    It is used for links. For example, navbar links, other navigation links 
    and footer links for an HTML page
    Learn more:
    https://framestd.github.io/remarkup/spec/v1/frame-functions.html#explode"""
    Framecls._Frame__RESTRUCTURE = 1
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

def getf(options, filepath):
    Framecls._Frame__RESTRUCTURE = 0 # do not restructure tabs, pad them


    if type(filepath) is list and len(filepath) != 1:
        console.error("read function expected 1 argument {} given".format(len(filepath)))
        return
    filepath = filepath[0]
    filepath = filepath.lstrip().rstrip()
    with open(realpath(workspace, filepath)) as res:
        return Framecls.escape(
            str(
                res.read()
            )
        )
    return ""

def encodeURI(options, s):
    Framecls._Frame__RESTRUCTURE = 0
    safe = "/"
    try:
        safe = s[1]
    except IndexError:
        safe = safe
    encoded = ""
    s = s[0]
    s = Framecls.unescape(s)
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

def encodeBase64(options, s):
    import base64 as b64
    try:
        urlsafe = int(s[1]) if type(s) is list else False
    except IndexError:
        urlsafe = False
    try:
        s = s[0] if type(s) is list else s
    except IndexError:
        console.error("expected a string as first argument got null string")
        sys.exit(1)

    s = Framecls.unescape(s)
    try:
        s = s.encode("utf-8")
    except TypeError:
        console.error('Internal error')
        sys.exit(1)
    encoded = ""

    if urlsafe:
        encoded = b64.urlsafe_b64encode(s).decode("ascii")
    else:
        encoded = b64.b64encode(s)
    return encoded

def decodeBase64(options, s):
    import base64 as b64
    try:
        urlsafe = int(s[1]) if type(s) is list else False
    except IndexError:
        urlsafe = False
    try:
        s = s[0] if type(s) is list else s
    except IndexError:
        console.error("expected a string as first argument got null string")
        sys.exit(1)

    s = Framecls.unescape(s)
    try:
        s = s.encode("utf-8")
    except TypeError:
        console.error('Internal error')
        sys.exit(1)
    decoded = ""

    if urlsafe:
        decoded = b64.urlsafe_b64decode(s).decode("ascii")
    else:
        decoded = b64.b64decode(s).decode("ascii")
    return decoded


def htmlchars(options, arg):
    #useful for writing in <pre> and <code> tags without stress.
    try:
        arg[1] = arg[1].lstrip().rstrip()
        if str(arg[1]).isdigit():
            Framecls._Frame__RESTRUCTURE = int(arg[1])
        else:
            console.warn("expected a number as the second argument")
            Framecls._Frame__RESTRUCTURE = 0
    except IndexError:
        Framecls._Frame__RESTRUCTURE = 1
    if len(arg) < 1:
        return
    specialchars = [
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ("\"", "&quot;")
    ]
    inv = arg[0].rstrip()
    for char, code in specialchars:
        inv = inv.replace(char, code)
    return str(inv).lstrip()

# export functions
functions["explode"] = explode
functions["read"] = getf
functions["code"] = htmlchars
functions["encodeURI"] = encodeURI
functions["encodeB64"] = encodeBase64
functions["decodeB64"] = decodeBase64
