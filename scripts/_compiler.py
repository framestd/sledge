import re
import io
import os
import sys
from . import framefunctions
from . import preprocessors  as prep
from .framefunctions import *
from . import console
from . import console

#\x5C->\ esc char

__all__ = ["Frame"]
n = "\n"

def _rep(s, o, n):
    return s.replace(o, n)

class Frame():
    def __init__(self):

        self.pane = {} # general pane
        self.specific = {} # contains unique props. for each file,
                           # title, meta variables are accessed from here
                           # The usage is defered until build time
        self.dest = ""
        self.WORKSPACE = "" # current working dir
        self.PAGESFILE = "" # current page file not layout or import
        self.CURFILE = "" # file currently working on + layout + import
        self.BASESPACE = "" # root src dir

        prep.Initialize(self, Frame)

        framefunctions.Export(Frame)

    funcs = framefunctions.functions

    #FrameFunctions option
    __RESTRUCTURE = 0

    # enum MODES
    
    DIR_MODE = 0 # all files in dir
    FILE_MODE = 1 # single file
    LAYOUT_MODE = 2 # dependent file layout file


    # BEGIN DECLARATION: Frame global object and constant fields
    FRAME = "FRAME"    # GLOBAL INHERITABLE NAMESPACE FIELD
    BODY = "BODY"    # CONSTANT FIELD, PROPERTY OF `FRAME`
    DIRNAME = "DIRNAME"    # CONSTANT FIELD, PROPERTY OF `FRAME`
    FILENAME = "FILENAME"    # CONSTANT FIELD, PROPERTY OF `FRAME`
    TITLE = "TITLE"    # UNIQUE FIELD, PROPERTY OF `FRAME`
    METAS = "METAS"    # NAMESPACE FIELD, UNIQUE, PROPERTY OF `FRAME`
    GROUP = "GROUP"    # DEPENDENT CONSTANT FIELD, PROPERTY OF `FRAME`
    LAST_MODIFIED = "LASTMOD"    # CONSTANT FIELD, PROPERTY OF `FRAME`
    TIME = "TIME"
    # END

    def storepane(self, pane):
        self.pane = pane

    def getpane(self):
        return self.pane

    def inform(self, a, b):
        from . import jobs
        p, n = "positive", "negative"
        self.BASESPACE = a
        self.WORKSPACE = b
        return

    @staticmethod
    def unescape(context, all=True):
        """This is used with framefunctions to compile escape for args"""
        return Frame().__unescape(context, all)
    @staticmethod
    def escape(context):
        """This is used with framefunctions to escape strings returned from functions like `read(...)`"""
        return Frame().__escape(context)

    def __escape(self, context):
        context = re.sub(r"\\", r"\\\\", context)
        context = re.sub(r"([\x23\x24\x25\x28\x29\x2C\x2E\x40])", u"\x5C\x5C\\1", context)
        return context
    
    def __unescape(self, context, all=False):
        """escape frame escapable chars when `all=True`
        else: only every '\\\\' when `all=false`.
        others will be used as tokens to identify part of strings
        differently from programs to prevent a clash, as strings ain't enclosed in any quotes.
        After compilation escapeable chars are escaped. """
        try:
            escapable = r"\x5C([\x23\x25\x28\x29\x2C\x2E\x40])" # escapable chars: [#$%(),.@] 
                                                                                  # sq. bracks. not included
            if not all:
                context = re.sub(r"\\\\", r"\\//~~\\//", context)
            if all:
                context = _rep(context, '\\$', '&dollar;') # variables could still be active, not only
                                                           # at compile time, but also at build time.
                context = re.sub(escapable, "\\1", context) 
                context = context.replace("\\//~~\\//", r"\\")
        except re.error as rex:
            console.error(rex.message)
            sys.exit(1)
        return context
    
    def __process(self, frameup, mode):
        return prep.parsepreprocessor(frameup, 
                                      prep.processor, mode)

    def __doTabs(self, context="", tab=""):
        """Pad tabs to the beginning of each newline so replacement 
        can fit into the replaced's psoition"""
        if context is None: return ""
        if type(context) is int: return context
        lctx = str(context).split(n)
        nctx = r""
        for each in lctx:
            nctx += "{}{}\n".format(tab,each)
        return nctx.rstrip(n)

    def __parse_class(self, frameup):
        """Handles the parsing to real HTML, of class-frame of a Frame markup"""
        classframe = re.sub(r"(<[\d\w#-]+)(?<!\x5C)\.([\d\w.\x5C-]+)(#|>|/|\s)", 
                            "\\1 class=\x22\\2\x22\\3", frameup)
        parsed = re.findall(r"class=\x22.+?\x22", classframe)
        for each in parsed:
            each_ = re.sub(r"(?<!\x5C)\.", " ", each)
            classframe = classframe.replace(r"%s"%each, each_)
        return classframe

    def __parse_id(self, frameup):
        idframe = re.sub(r"(<.+?)(?<!(?:[\x5C\x3D\x3E]\x22))#([\w\d:-]+)(?!\x22)", 
                         "\\1 id=\"\\2\"", frameup) # dots can be present in id attr. come back
        return idframe

    def __autoclose(self, frameup):
        autoframe = re.sub(r"(<)([\w\d-]+)(.*?)//>", "\\1\\2\\3></\\2>", frameup)
        return autoframe

    def __setformating(self, frameup):
        pane = self.getpane()
        formatted = frameup
        frameup = re.sub(r"(?<!\x5C)%\w+\(.*?(?<!\x5C)\)", "", frameup, 0 ,re.DOTALL) # DO NOT DEAL WITH FUNCTIONS!
        allFormat = re.findall(r"([ \t]*)(?<!\x5C)\x24\x7B(.+?)\x7D(?:\x5B([\d*]+)\x5D)?", frameup)

        if len(allFormat) < 1 or allFormat is None: return formatted

        for tab, each, index in allFormat:
            each_ = each.lstrip().split("::")

            # Begin Frame namespace and constant fields
            if each_[0] == Frame.FRAME:
                ptrn = [
                    "${FRAME::DIRNAME}", "${FRAME::FILENAME}",
                    "${FRAME::LASTMOD}", "${FRAME::TIME}"
                ]
                if each_[1] == Frame.BODY:
                    continue
                elif each_[1] == Frame.DIRNAME:
                    formatted = _rep(formatted, ptrn[0], self.WORKSPACE)
                elif each_[1] == Frame.FILENAME:
                    formatted = _rep(formattedr, ptrn[1], self.PAGESFILE)
                elif each_[1] == Frame.LAST_MODIFIED or each_[1] == Frame.TIME:
                    import datetime
                    date = datetime.datetime.now().strftime("%d %b, %Y %H:%M:%S")
                    formatted = _rep(formatted, ptrn[2], date)
                    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%Z")
                    formatted = _rep(formatted, ptrn[3], date)
                    del datetime
                elif each_[1] == Frame.TITLE:
                    continue
                elif each_[1] == Frame.METAS:
                    continue
                else:
                    pass
            # End Frame constant fields
            
            paneValue = recurseAddress(pane, each_, 0)
            try:
                if type(paneValue) is dict:
                    raise TypeError()
            except TypeError:
                console.error('TypeError: cannot handle type "Map" in this context')
                console.error('\tunsupported type "Map" instead of String or List')
                sys.exit(1)

            if type(paneValue) is list:
                index = str(index)
                index = int(index) if index.isdigit() else index
                ptrn = u"%s\x24\x7B%s\x7D\x5B%s\x5D"%(tab, each, index)
                if index == "*" or index == "":
                    paneValue = " ".join(paneValue)
                    paneValue = self.__doTabs(paneValue, tab)
                    formatted = formatted.replace(ptrn, paneValue)
                else:
                    paneValue = paneValue[index]
                    paneValue = self.__doTabs(paneValue, tab)
                    formatted = formatted.replace(ptrn, paneValue)
            else:
                paneValue = self.__doTabs(paneValue, tab) # if paneValue is `None` will return nullstring
                #BEGIN: one statement
                formatted = re.sub(r"%s\x24\x7B%s\x7D"%(tab,each), 
                    "%s"%paneValue, 
                    formatted)
                #END
        for key, value in pane.items():
            #frame-attribute formatting non-standard
            formatted = re.sub(r"%s=\"\{\}\""%key, "%s=\"%s\""%(key,value), formatted)
        return formatted


    def __parsefunctions(self, frameup):
        """Parses and executes frame functions.
        Note: Frame-functions are built-in functions, and it is NOT RECOMENDED 
            to personally add your own functions.
            As and If the need arises functions WOULD be added to new releases 
            as UPDATED by the 'Frame Specifications' 
            https://framestd.github.io/remarkup/spec/v1/frame-functions.html"""
        
        funclist = re.findall(r"""
            ([ \t]*)(?<!\x5C) #not preceeded by an escape char (\)
            %(\w+)\s*\x28 # open bracket
            (.*?)(?<!\x5c) # closing bracket not preceeded by escape char
            \x29""", frameup, re.S|re.X) 
        cache = re.findall(r"""
            [ \t]*(?<!\x5C) #not preceeded by an escape char (\)
            %\w+\s*\x28 # a bracket
            .*?(?<!\x5c) # closing bracket not preceeded by escape char
            \x29""", frameup, re.S|re.X)
        functional = frameup
        funcReturnValue = None
        i = 0
        
        if len(funclist) < 1 or funclist is None: return frameup 

        for tab, funcname, args in funclist:
            result = r""
            
            _args_ = re.split(r"(?<!\x5C)\x2C", args) # split at the point where there is no "\" before ","
                                                      # if "," follows "\" then it's an escaped string within function

            console.info("status: executing function \"{}\"".format(funcname))
            try:
                funcReturnValue = Frame.funcs[funcname](self.getpane(), _args_)
                funcReturnValue = self.__unescape(funcReturnValue, all=True)
                funcReturnValue = str(funcReturnValue)

            except KeyError:
                import sys
                msg = "cannot execute function\
                \nTrace-> encountered an unknown function \"{}\" in {}".format(funcname, self.CURFILE)
                console.error(msg+"\nif this is not intended to be a function you can escape the `%` using"
                +" a reverse solidus `\%`") # come back CURFILE recheck
                sys.exit(1)

            if funcReturnValue is not None and type(funcReturnValue) is str:
                #BEGIN: search tabs before function and before parameter
                #tab = re.search(r"\n?([ \t]*)\x25\w", cache[i]).group(1)
                atab = re.search(r"\n?([ \t]*)(?![\s\x00])", args.lstrip(n).split(n)[0]).group(1)
                _t = tab
                tab = tab.count(" ") if tab.count(" ") else tab.count("\t")
                atab = atab.count(" ") if atab.count(" ") else atab.count("\t")
                tab_diff = atab - tab
                #END

                #BEGIN: restructure tabs if parameter to function will be processed
                # and sent back as function return value. For example: in functions like 
                # `explode` and `code`
                result = funcReturnValue
                if tab_diff and not 4 % tab_diff and Frame.__RESTRUCTURE:
                    result = re.sub(r"(?:[ \t]{%s})(?![\s\x00])"%tab_diff, "", result)
                else:
                    result = self.__doTabs(result, _t)
                del _t
                #END
                
                old = "{}".format(cache[i])
                functional = functional.replace(old, result.lstrip(n), 1)
            else:
                result = funcReturnValue
                old = "{}".format(cache[i])
                functional = functional.replace(old, result, 1)
            i += 1
        return functional


    def compile(self, framefile, mode=DIR_MODE):
        """compiles a frame to standard HTML
        framefile: path to file to compile
        mode: mode=0 means, normal pages; mode=1, means layout"""
        
        from . import console
        console.info("status: compiling \"{}\"".format(framefile))

        #BEGIN: get things ready
        self.CURFILE = framefile
        frameup = None
        if mode == Frame.LAYOUT_MODE:
            prep.workspace = os.path.dirname(framefile)
            self.WORKSPACE = prep.workspace
        elif mode == Frame.FILE_MODE:
            FILE = framefile.split(os.sep)[-1]
            self.PAGESFILE = re.sub(r"(\..*?)$", "", FILE)
        elif mode == Frame.DIR_MODE:
            FILE = framefile.split(os.sep)[-1]
            self.PAGESFILE = re.sub(r"(\..*?)$", "", FILE)
        else:
            pass
        prep.workspace = os.path.dirname(framefile)
        self.WORKSPACE = prep.workspace
        framefunctions.workspace = self.WORKSPACE
        #END

        with io.open(framefile, encoding="utf-8") as f:
            frameup = f.read()
        if frameup is None: sys.exit(1)

        frameup = self.__unescape(frameup)
        
        layoutFile, self.pane, specific, dest = self.__process(frameup, mode)
        
        framefunctions.framepane = self.pane # Do not do this and the ff until above __process call
        
        frameup = re.sub(r"^(?:@[\w\d\s:\"\'./-]+)+", "", frameup, re.M) # remove preprocessors
        
        compiled = self.__parsefunctions(
            self.__autoclose(
                self.__parse_id(
                    self.__parse_class(
                        self.__setformating(
                            frameup
                        )
                    )
                )
            )
        )
        compiled = self.__unescape(compiled, all=True)
        if mode == Frame.LAYOUT_MODE:
            return compiled
        return (layoutFile, compiled, dest, specific)
        