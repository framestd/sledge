import re

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


def explode(options, arg):
    """The Frame function -- explode:
    This is used to propagate a given string and formatting it with unique Panes.
    It is used for links. For example, navbar links, other navigation links 
    and footer links for an HTML page
    Learn more:
    https://frame.github.io/spec/v1/frame-functions.html#explode"""
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

    if type(pane) == list:
        for item in pane:
            ndata = re.sub(r'\x24\x7BICON\x7D', "%s"%item['ICON'], data) if item.has_key("ICON") else re.sub(r'\x24\{ICON\}', '', data)
            ndata = re.sub(r'\x24\x7BTITLE\x7D', "%s"%item['TITLE'], ndata) if item.has_key("TITLE") else re.sub(r'\x24\{TITLE\}', '', ndata)
            ndata = re.sub(r'\x24\x7BHREF\x7D', "%s"%item['HREF'], ndata) if item.has_key("HREF") else re.sub(r'\x24\{HREF\}', '#', ndata)
            datalist.append(ndata)
        return str("".join(datalist))

    for item in pane.values():
        group_pane = pane.keys()[index] if cond else ''
        index += 1
        group_ = re.sub(r'\x24\x7BFRAME::GROUP\}', "%s"%group_pane, group) if cond else ''
        datalist.append(group_)

        for i in range(len(item)):
            ndata = re.sub(r'\x24\x7BICON\x7D', "%s"%item[i]['ICON'], data) if item[i].has_key("ICON") else re.sub(r'\x24\x7BICON\x7D', '', data)
            ndata = re.sub(r'\x24\x7BTITLE\x7D', "%s"%item[i]['TITLE'], ndata) if item[i].has_key("TITLE") else re.sub(r'\x24\x7BTITLE\x7D', '', ndata)
            ndata = re.sub(r'\x24\x7BHREF\x7D', "%s"%item[i]['HREF'], ndata) if item[i].has_key("HREF") else re.sub(r'\x24\x7BHREF\x7D', '#', ndata)
            datalist.append((datalist.pop() + ndata))
    return str("".join(datalist))

def getf(options, arg):
    Frame._Frame__RESTRUCTURE = 0
    if len(arg) < 1:
        return
    arg[0] = arg[0].lstrip().rstrip()
    with open(arg[0]) as res:
        return str(res.read())
    return ""

def invert(options, arg):
    #useful for writing in <pre> and <code> tags without stress.
    Frame._Frame__RESTRUCTURE = 1
    if len(arg) < 1:
        return
    specialchars = {
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "&": "&amp;amp;" # This is so because of the escape call, this has a meaning in frame. Check '/escentity/esc.py'[ln: 14-30]
    }
    inv = arg[0].rstrip()
    for char, code in specialchars.items():
        inv = inv.replace(char, code)
    return str(inv)

functions["explode"] = explode
functions["read"] = getf
functions["htmlspecialchars"] = invert