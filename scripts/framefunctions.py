import re
import sys
from . import console



def recurseAddress(o, x, i=0):
    try:
        return o[x[i]] if i == (len(x) - 1) else recurseAddress(o[x[i]], x, i+1)
    except KeyError:
        pass

def sub(pattern, item, where, key):
    return re.sub(pattern, 
    "{}".format(item[key]), 
    where) if key in item else re.sub(pattern, 
    '', where)


#########               METHOD EXCEPTION                   ##########

class FrameMethodError(Exception):
    def __init__(self, msg):
        Exception.__init__(msg)


#########               BEGIN FRAME FUNCTIONS                   ##########
from ._compiler import frame
from .frame import Frame

class FrameFunctions(Frame):
    def __init__(self, **kwargs):
        self.CURDIR = kwargs['cd']
        self.BASESPACE = kwargs['bs']
        self.pane = kwargs['pn']

    functions = dict()
    def explode(self):
        return 0
    def explode(self, group="", ctx="", address=""):
        """The Frame function -- explode:
        This is used to propagate a given string arg, mostly a markup and formatting it with unique Panes.
        It is used for links. For example, navbar links, other navigation links 
        and footer links for an HTML page"""
        
        Frame._RESTRUCTURE = 1
        options = self.pane

        cond = address == ""
        if cond:
            address, ctx, group = ctx, group, None
        temparg = address
        templateAddress = str(temparg).lstrip().rstrip().split("::")
        #pane = options["nav"]["nav-links"]
        pane = recurseAddress(options, templateAddress, 0)

        data = ctx
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
        
        cond = not group is None
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

    def getf(self, filepath):
        Frame._RESTRUCTURE = 0 # do not restructure tabs, pad them
        
        options = self.pane
        
        filepath = self.setformating(filepath.lstrip().rstrip())
        from .preprocessors import PreProcessor
        try:
            f = open(PreProcessor.realpath(self.CURDIR, filepath))
            return Frame.escape(
                str(
                    f.read()
                )
            )
        except IOError as ex:
            console.error(ex.message)
            sys.exit(1)
        return ""

    def encodeURI(self, uri, safe='/'):
        Frame._RESTRUCTURE = 0

        options = self.pane
        encoded = ""
        # unescape, you won't want to encode an \x5C:
        # reverse-solidus along with string 
        uri = Frame.unescape(uri)
        try:
            from urllib import parse # for Python 3
        except ImportError:
            try:
                import urllib as parse # for Python 2
            except ImportError:
                console.error("could not load required library 'urllib'")
                console.error("cannot encode URI")
                sys.exit(1)
        encoded = parse.quote_plus(uri, safe=safe)
        return encoded

    def encodeBase64(self, string, urlsafe=False):
        import base64 as b64
        # unescape, you won't want to encode an \x5C:
        # reverse-solidus along with string 
        string = Frame.unescape(self.setformating(string))
        try:
            string = string.encode("utf-8")
        except TypeError:
            console.error('Internal error') # this is not meant to happen
            sys.exit(1)
        encoded = ""

        if urlsafe:
            encoded = b64.urlsafe_b64encode(string).decode("ascii")
        else:
            encoded = b64.b64encode(string).decode("ascii")
        return encoded

    def decodeBase64(self, string, urlsafe=False):
        import base64 as b64
        # unescape not really necessary here
        # but to be on a safer side
        # unescape or not, I don't think anything is affected
        # Base64 don't contain "(" or "," or ")" or "\"
        string = Frame.unescape(self.setformating(string))
        try:
            string = string.encode("utf-8")
        except TypeError:
            console.error('Internal error') # this is not meant to happen
            sys.exit(1)
        decoded = ""

        if urlsafe:
            decoded = b64.urlsafe_b64decode(string).decode("ascii")
        else:
            decoded = b64.b64decode(string).decode("ascii")
        return decoded


    def htmlchars(self, code, inline_or_block=1):
        #useful for writing in <pre> and <code> tags without stress.
        # inline_or_block: 1 for block, 0 for inline
        if str(inline_or_block).isdigit():
            Frame._RESTRUCTURE = int(inline_or_block)
        else:
            console.warn("expected a number as the second argument")
            Frame._RESTRUCTURE = 0 # make inline if anything other than number
        
        specialchars = [
            ("&", "&amp;"),
            ("<", "&lt;"),
            (">", "&gt;"),
            ("\"", "&quot;"),
            ("'", "&#39;")
        ]
        inv = self.setformating(code.rstrip())
        for char, ent in specialchars:
            inv = inv.replace(char, ent)
        return str(inv).lstrip()
    
    @staticmethod
    def mount_method(method, access_name):
        """if method is None or access_name is None:
            raise FrameMethodError("access_name or method cannot be of type 'None'")
        if not True:
            raise AttributeError()
        FrameFunctions.functions[access_name] = method"""
        return NotImplemented#yet
    
    # export functions
    def mount(self):
        FrameFunctions.functions["explode"] = self.explode
        FrameFunctions.functions["read"] = self.getf
        FrameFunctions.functions["code"] = self.htmlchars
        FrameFunctions.functions["encodeURI"] = self.encodeURI
        FrameFunctions.functions["encodeB64"] = self.encodeBase64
        FrameFunctions.functions["decodeB64"] = self.decodeBase64
