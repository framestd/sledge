from __future__ import print_function
from collections import OrderedDict
import re
import sys
import yaml
import os
import io
from . import console
from .utils import indexer

lws = workspace = basespace = dest = ""

REL_TO_PAGES_ROOT = 'rel_to_pages_root'
DEST = 'dest'
BUILD = 'path'

from . import frame
from .frame import Frame
class PreProcessor(Frame):
    def __init__(self, **kwargs):
        self.CURDIR = kwargs['cd']
        self.WORKSPACE = kwargs['ws']
        self.CURFILE = kwargs['cf']
        self.CONF = kwargs['cnf']
        self.BASESPACE = kwargs['bs']
        self.PAGESFILE = kwargs['pf']
        self.path_diff = kwargs['pth_dif']
        self.mode = kwargs['mode']
        self.SOURCE = kwargs['src']
        self.Indexer = None
        if self.BASESPACE != "" and self.mode == Frame.DIR_MODE:
            self.Indexer = indexer.Indexer(
                os.path.join(self.BASESPACE, '.sledge', 'INDEX.db')
            )
            self.Indexer.load()
            self.IndexWriter = self.Indexer.index_on(self.SOURCE)
        self.deps = []
    
    @staticmethod
    def oload(stream, Loader=yaml.Loader, obj_pairs_hook=OrderedDict):
        """Preserve Dict Order
        -------------------------
        Load yaml mappings into `collections.OrderedDict`,
        so as to keep the ordering.
        Without this, methods like `FrameFunctions.explode(...)` may be affected,
        as ordering of links and groups would not be preserved in the compiled markup.  
        This implementation is based on a stackoverflow answer.  
        Question: [load yaml mappings as OrderedDict](https://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts)  
        Answer: [by @coldfix](https://stackoverflow.com/a/21912744/8124214)"""
        class OrderedLoader(Loader):
            pass
        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return obj_pairs_hook(loader.construct_pairs(node))
        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping
        )
        return yaml.load(stream, OrderedLoader)
    

    def loadpane(self, src):
        panefile = panecontent = None
        try:
            panefile = io.open(src, encoding="utf-8")
            panecontent = panefile.read()
            console.info("status: opening '{}'".format(src))
        except IOError:
            console.error("Could not open pane at '{}'".format(src))
        finally:
            panefile.close()
            console.info("status: parsing '{}'".format(src))
        return PreProcessor.oload(panecontent, yaml.SafeLoader) if not panecontent is None else None

    def parsepreprocessor(self, frameup, cb, mode):
        import sys
        exports = {
            "pane": {},
            "layout": None,
            "dest": None,
            "specific": {},
            "utils.Indexer": None
        }
        console.info("status: parsing preprocessors")
        splitframe = frameup.split('\n')
        for each in splitframe:
            pp = []
            pp = re.findall(r'^\s*(?:@)(\w+):\s*(.*)', each)
            check = re.match(r"^\s*<![\w-]+", each)
            if check is not None and len(pp) == 0:
                continue
            elif check is None and len(pp) == 0:
                break
            else:
                pass
            for tag, attrs in pp:
                cb(tag, attrs.lstrip(), mode, exports) # exports is passed by reference
        if len(self.deps) > 0 and mode == Frame.DIR_MODE:
            self.IndexWriter.write_index(*self.deps)
        return (
            exports["layout"]
            ,exports["pane"]
            ,exports["specific"]
            ,exports["dest"]
            ,self.Indexer)

    def getAttribute(self, attr, _collection):
        rel = ''
        try:
            rel = re.search(r'%s-(\"|\'){1}(.*?)\1'%attr, _collection, re.I).group(2)
        except AttributeError:
            console.warn("unassigned attribute \"{}\" around \"{}\"".format(attr, _collection))
            return None
        return rel


    def processor(self, tag, attr, mode, exports):
        # =================================
        # convert all preprocessor tags
        # to either uppercase or lowercase
        # it's meant to be case insensitive
        # =================================
        if tag.lower() == "load":
            rel = self.getAttribute('rel', attr).lstrip().lower()
            src = ""

            if rel == "panes":
                src = self.getAttribute('src', attr)
                src = PreProcessor.realpath(self.CURDIR, src)
                self.deps.append(src)

                pane = dict()
                if os.path.isfile(src):
                    pane.update(self.loadpane(src))
                else:
                    __panenotfound__ = True
                exports["pane"].update(pane)

            elif rel == "dest":
                PreProcessor.check_mode(mode, Frame.LAYOUT_MODE, "dest") # check mode

                dest = self.getAttribute('href', attr)
                dest = self.CONF[DEST][BUILD] if dest is None else dest
                # ===================================================
                # if the `.framerc` file specifies that destination
                # paths are relative to the pages root, not the 
                # directory where the file being compiled is,
                # then use `self.BASESPACE` which is the root of 
                # all pages i.e 'project/src/pages/' not 
                # 'project/src/pages/file/compile/'(example.frame)
                # in this sense, `dest-"../../build"` evaluates to
                # 'project/build/' otherwise, dest should be
                # `dest-"../../../../build"` 'projects/build'
                # ===================================================
                if dest.isspace() or dest == "":
                    console.error("'dest' cannot be '{}'".format(dest))
                    sys.exit(1)
                if self.CONF[DEST][REL_TO_PAGES_ROOT]:
                    dest = PreProcessor.realpath(self.BASESPACE, dest)  
                else:
                    dest = PreProcessor.realpath(self.CURDIR, dest)
                _path_diff = '' if self.path_diff is None else self.path_diff
                real_dest = PreProcessor.realpath(dest, _path_diff)
                print(dest, real_dest)
                if os.path.isdir(dest):
                    # ================================================
                    # wrap it in try/except in case there are no
                    # path differences and `real_dest` == `dest`
                    # so no exception is raised
                    # ================================================
                    try:
                        # ============================================
                        # `_path_diff` is meant for path reflections
                        # so a subfolder in the 'src/pages' root say
                        # 'project/src/pages/subfolder/'(example.frame)
                        # will also reflect in the build folder as 
                        # 'project/build/subfolder'/(example.html)
                        # =============================================
                        os.mkdir(real_dest)
                        # =============================================
                        # `real_dest` is the concatenation of the 
                        # `dest` and `_path_diff` to make path reflec-
                        # tions.
                        # =============================================
                    except:
                        pass
                else:
                    try:
                        # ==============================================
                        # do not use `os.makedirs` so do it twice
                        # if `dest` doesn't exist then create `dest`
                        # first `real_dest` relies on it because
                        # `real_dest` is a child directory to `dest`
                        # ==============================================
                        os.mkdir(dest)
                        os.mkdir(real_dest)
                    except OSError as ex:
                        console.error("unable to create destination folder: {}".format(ex.message))
                        sys.exit(1)
                exports["dest"] = real_dest

            elif rel == "layout":
                PreProcessor.check_mode(mode, Frame.LAYOUT_MODE, "layout") # check mode

                src = self.getAttribute('src', attr)
                src = PreProcessor.realpath(self.CURDIR, src)
                self.deps.append(src)

                exports["layout"] = src

            elif rel == "specific":
                PreProcessor.check_mode(mode, Frame.LAYOUT_MODE, "specific") # check mode

                src = self.getAttribute('src', attr)
                address = self.getAttribute('find', attr)
                src = PreProcessor.realpath(self.CURDIR, src)
                self.deps.append(src)

                pane = dict()
                if os.path.isfile(src):
                    pane.update(self.loadpane(src))
                else:
                    __panenotfound__ = True
                exports["specific"] = pane[address]
            else:
                pass

        elif tag.lower() == "import":
            src = self.getAttribute('src', attr)
            src = PreProcessor.realpath(self.CURDIR, src)
            assign = self.getAttribute('as', attr)
            self.deps.append(src)

            console.info("status: importing \"{}\" as \"{}\"".format(src, assign))
            from . import jobs
            lws = self.CURDIR
            basespace = self.BASESPACE
            jobs.add(src)
            exports["pane"][assign] = jobs.dojob()
            self.BASESPACE = basespace
        else:
            pass
        

    @staticmethod
    def realpath(workspace, path):
        if not os.path.isabs(path):
            path = os.path.join(workspace, path, '')
            return os.path.normpath(path)
        else: return path

    @staticmethod
    def check_mode(mode, against, msg):
        msgs = {
            "layout": "layout file cannot have a layout",
            "dest": "layout file is not qualified to have a 'dest' relationship",
            "specific": "layout file is not qualified to have a 'specific' relationship"
        }
        if mode == against:
            console.error(msgs[msg])
            sys.exit(1)
        return 0
