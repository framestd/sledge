# Copyright 2019 Frame Studios. All rights reserved.
# ReMarkup v1.0 python implementation.
# Sledge v1.0
# Project Manager: Caleb Adepitan
# The ReMarkup specifications that govern this implementation can be found at:
# https://framestd.github.io/remarkup/spec/v1/
# Developers Indulgent Program (DIP)
# Use of this source code is licensed under the MIT LICENSE
# which can be found in the LICENSE file.
# In attribution to Realongman, Inc.

import re
import io
import os
from . import framefunctions
from . import preprocessors  as prep
from .framefunctions import *
from . import escentity as esc
from . import console

__all__ = ["Frame"]
n = "\n"
class Frame():
    def __init__(self):
        self.pane = {}
        self.specific = {}
        self.dest = ""
        self.WORKSPACE = self.CURFILE = None
        self.BASESPACE = ""
        prep.setFrameInst(self)
        prep.ExportFrameCls(Frame)
        framefunctions.ExportFrameCls(Frame)

    linkedLayoutFrame = None
    funcs = framefunctions.functions
    #FrameFunctions option
    __RESTRUCTURE = 0

    # BEGIN DECLARATION: Frame global object and constant fields
    FRAME = "FRAME"    # GLOBAL INHERITABLE OBJECT
    BODY = "BODY"    # CONSTANT FIELD, PROPERTY OF `FRAME`
    DIRNAME = "DIRNAME"    # CONSTANT FIELD, PROPERTY OF `FRAME`
    FILENAME = "FILENAME"    # CONSTANT FIELD, PROPERTY OF `FRAME`
    TITLE = "TITLE"    # CONSTANT FIELD, PROPERTY OF `FRAME`
    METAS = "METAS"    # CONSTANT FIELD, PROPERTY OF `FRAME`
    GROUP = "GROUP"    # DEPENDENT CONSTANT FIELD, PROPERTY OF `FRAME`
    LAST_MODIFIED = "LASTMOD"    # CONSTANT FIELD, PROPERTY OF `FRAME`
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
    
    def __process(self, frameup, mode):
        return prep.parsepreprocessor(frameup, prep.processor, mode)

    def __doTabs(self, context="", tab=""):
        """Pad tabs to the beginning of each newline so replacement 
        can fit into the replaced's psoition"""
        if context is None: return ""
        if type(context) is int: return context
        lctx = str(context).split(n)
        nctx = r""
        for each in lctx:
            nctx += "%s%s\n"%(tab,each)
        return nctx.rstrip(n)

    def __parse_class(self, frameup):
        """Handles the parsing, to real HTML, of class-frame of a Frame markup"""
        classframe = re.sub(r"(<[\w#-]+)\.([\w.-]+)(#|>|/|\s+)", "\\1 class=\x22\\2\x22\\3", frameup)
        parsed = re.findall(r"class=\x22.+?\x22", classframe)
        for each in parsed:
            each_ = re.sub(r"\.", " ", each)
            classframe = re.sub(r"%s"%each, each_, classframe)
        return classframe

    def __parse_id(self, frameup):
        idframe = re.sub(r"(<.+?)(?<!(?:[\s\x3D]\x22))#([\w\d-]+)(?!\x22)", "\\1 id=\"\\2\"", frameup)
        return idframe

    def __autoclose(self, frameup):
        autoframe = re.sub(r"(<)([\w\d-]+)(.*?)//>", "\\1\\2\\3></\\2>", frameup)
        return autoframe

    def __setformating(self, frameup):
        pane = self.getpane()
        formatted = frameup
        frameup = re.sub(r"%\w+\(.*?\)", "", frameup, 0 ,re.DOTALL) # DO NOT DEAL WITH FUNCTIONS!
        allFormat = re.findall(r"([ \t]*)\x24\x7B(.+?)\x7D(?:\x5B([\d*]+)\x5D)?", frameup)

        for tab, each, index in allFormat:
            each_ = each.lstrip().split("::")

            # Begin Frame constant fields
            if each_[0] == Frame.FRAME:
                if each_[1] == Frame.BODY:
                    continue
                elif each_[1] == Frame.DIRNAME:
                    formatted = re.sub(r"\$\{FRAME::DIRNAME\}", self.WORKSPACE, formatted)
                elif each_[1] == Frame.FILENAME:
                    formatted = re.sub(r"\$\{FRAME::FILENAME\}", self.CURFILE, formatted)
                elif each_[1] == Frame.LAST_MODIFIED:
                    continue
                elif each_[1] == Frame.TITLE:
                    continue
                elif each_[1] == Frame.METAS:
                    continue
                else:
                    pass
            # End Frame constant fields
            
            paneValue = recurseAddress(pane, each_, 0)
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
                paneValue = self.__doTabs(paneValue, tab)
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
            If you so wish to have your own functions you MAY use Frame-lambdas.
            As and If the need arises functions WOULD be added to new releases 
            as UPDATED by the 'Frame Specifications' https://frame.github.io/spec/v1/frame-functions.html"""
        
        funclist = re.findall(r"%(\w+)\s*\((.*?)\)", frameup, re.DOTALL) 
        cache = re.findall(r"[ \t]*%\w+\s*\(.*?\)", frameup, re.DOTALL)
        functional = frameup
        funcReturnValue = None
        
        for i in range(len(funclist)):
            result = r""
            console.info("status: executing function \"{}\"".format(funclist[i][0]))
            funcReturnValue = Frame.funcs[funclist[i][0]](self.getpane(), (funclist[i][1].split(",")))

            if funcReturnValue is not None and type(funcReturnValue) is str:
                #BEGIN: search tabs before function and before parameter
                tab = re.search(r"\n?([ \t]*)\x25\w", cache[i]).group(1)
                atab = re.search(r"\n?([ \t]*)(?![\s\x00])", funclist[i][1].lstrip(n).split(n)[0]).group(1)
                _t = tab
                tab = tab.count(" ") if tab.count(" ") else tab.count("\t")
                atab = atab.count(" ") if atab.count(" ") else atab.count("\t")
                tab_diff = atab - tab
                #END

                #BEGIN: restructure tabs if parameter to function will be processed
                # and sent back as function return value. For example: in functions like 
                # `explode` and `htmlspecialchars`
                result = funcReturnValue
                if tab_diff and not tab_diff % 4 and Frame.__RESTRUCTURE:
                    result = re.sub(r"(?:[ \t]{%s})(?![\s\x00])"%tab_diff, "", result)
                else:
                    result = self.__doTabs(result, _t)
                del _t
                #END

                old = "{}".format(cache[i])
                functional = functional.replace(old, result.lstrip(n), 1)
            else:
                result = funcReturnValue
                old = "%s"%(cache[i])
                functional = functional.replace(old, result, 1)
        return functional


    def compile(self, framefile, mode=0):
        """compiles a frame to standard HTML
        framefile: path to file to compile
        mode: mode=0 means, normal pages; mode=1, means layout"""

        from . import console
        console.info("status: compiling \"{}\"".format(framefile))
        #BEGIN: get things ready
        frameup = None
        prep.workspace = os.path.dirname(framefile)
        self.WORKSPACE = prep.workspace
        FILE = framefile.split(os.sep)[-1]
        self.CURFILE = re.sub(r"(\..*?)$", "", FILE) if not mode else self.CURFILE
        #END
        with io.open(framefile, encoding="utf-8") as f:
            frameup = f.read()
        layoutFile, self.pane, specific, dest = self.__process(frameup, mode)
        framefunctions.framepane = self.pane# Do not do this and the ff until above __process call
        frameup = re.sub(r"@.+\n*", "", frameup)
        compiled = esc.escape(self.__parsefunctions(self.__autoclose(self.__parse_id(self.__parse_class(self.__setformating(frameup))))))
        if mode:
            return compiled
        return (layoutFile, compiled, dest, specific)
