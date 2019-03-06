import os
from .frame import Frame

class Compiler(Frame):
    def __init__(self):
        Frame.__init__(self)
    
    def inform(self, mode, src, root, curdir, framerc):
        """If mode==LAYOUT_MODE src is None"""
        from . import jobs
        p, n = "positive", "negative"
        self.BASESPACE = root
        self.WORKSPACE = curdir
        self.CONFIGURATION = framerc
        self.SRC = src
        Frame.CONFIGURATION = framerc
        Frame.BASESPACE = root
        path_diff = ''
        if not src == None and mode != Compiler.LAYOUT_MODE:
            path_diff = jobs.path_diff(root, 
                os.path.dirname(src))[p]
            path_diff = '' if path_diff is None else path_diff
        self.path_diff = path_diff
        if mode == Compiler.DIR_MODE:
            Frame.path_prefix = '../'*path_diff.count(os.sep)
        return

    def compile(self, framefile, mode=Frame.DIR_MODE):
        """compiles a frame to standard HTML
        framefile: path to file to compile
        mode: mode=0 means, normal pages; mode=1, means layout"""

        import io
        import re
        from . import console

        LAYOUT_FILE = 'LAYOUT_FILE'
        DEST = 'DEST'
        PAGE = 'PAGE'
        UNIQUE = 'UNIQUE'
        PATH_PREFIX = 'PATH_PREFIX'
        INDEXER = 'INDEXER'

        self.MODE = mode
        console.info("status: compiling '{}'".format(framefile))

        #BEGIN: get things ready
        frameup = None

        self.CURFILE = framefile
        self.CURDIR = os.path.dirname(framefile)

        if mode == Compiler.FILE_MODE or mode == Compiler.DIR_MODE:
            FILE = framefile.split(os.sep)[-1]
            self.PAGESFILE = re.sub(r"(\..*?)$", "", FILE)
        else:
            pass
        #END

        with io.open(framefile, encoding="utf-8") as f:
            frameup = f.read()
        if frameup is None: sys.exit(3)

        frameup = self._unescape(frameup)

        layoutFile, self.pane, specific, dest, Indexer = self._process(frameup, mode)
        #specific.update({PATH_PREFIX: Compiler.path_prefix})
        # Do not do the ff until above _process call
        frameup = re.sub(r"^(?:@[\w\d\s:\"\'./-]+)+", "", frameup, re.M) # remove preprocessors
        compiled = self.setformating(
            self.parsefunctions(
                self.autoclose(
                    self.parse_id(
                        self.parse_class(
                            self.setformating(
                                frameup
                            )
                        )
                    )
                )
            )
        )
        compiled = self._unescape(compiled, all=True)
        if mode == Compiler.LAYOUT_MODE:
            return compiled
        return {
            LAYOUT_FILE: layoutFile,
            PAGE: compiled,
            DEST: dest,
            UNIQUE: specific,
            PATH_PREFIX: Compiler.path_prefix,
            INDEXER: Indexer
        }
        