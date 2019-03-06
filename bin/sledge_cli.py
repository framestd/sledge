#!usr/bin/env python
import sys
import os
import argparse
import sledge

class Clapi:
    def __init__(self):
        pass
    INIT_HELP = '''creates a new project in the directory
    from where the program is invoked'''
    INIT_PATH_HELP = '''creates a new project in the directory
    specified by the --path'''
    BUILD_HELP = '''builds the project in the directory passed alongside
    the build command'''
    BUILD_PATH_HELP = '''the path to source dir from where to build files
        e.g-> sledge build project/src/pages.'''
    BUILD_WATCH_HELP = '''watches the directory specified by path for changes
        e.g-> sledge build [-w|--watch] project/src/pages.'''
    BUILD_VERB_HELP = '''enable verbose logging to console'''
    FRAMERC = """{
        "ignore":[""],
        "filter":["*.frame"],
        "dest": {
            "path": "../build",
            "rel_to_pages_root": true
        }
    }"""
    COPYRIGHT = "Copyright 2019 Frame Studios, Caleb Adepitan"
    LICENSE =  "{}.\nMIT Licensed".format(COPYRIGHT)

    @staticmethod
    def start():
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--version', action='version', version='Sledge 1.0.0')
        #parser.add_argument('--license', '-l', action='license', license=Clapi.LICENSE)

        sub_parser = parser.add_subparsers()
        init_parser = sub_parser.add_parser('init', help=Clapi.INIT_HELP)
        init_parser.add_argument('--path', default='.', help=Clapi.INIT_PATH_HELP)
        init_parser.set_defaults(func=Clapi.initialize)

        build_parser = sub_parser.add_parser('build', help=Clapi.BUILD_HELP)
        build_parser.add_argument('path', help=Clapi.BUILD_PATH_HELP)
        build_parser.add_argument('-w', '--watch', action='store_true', help=Clapi.BUILD_WATCH_HELP)
        build_parser.add_argument('-v', '--verbose', action='store_true', help=Clapi.BUILD_VERB_HELP)
        build_parser.set_defaults(func=Clapi.build)
        args = parser.parse_args()
        args.func(args)
    
    @staticmethod
    def make(_type, path, content=''):
        if _type == 'dir':
            try:
                os.mkdir(path)
            except os.error as ex:
                print('[failed]: could not initialize a new project\n    %s'%ex.message)
                sys.exit(1)
        elif _type == 'file':
            import io
            if not os.path.exists(path):
                with io.open(path, 'w', encoding='utf-8') as f:
                    f.write(content.decode('utf-8'))
            else:
                print("path '%s' already exists"%(_file))
        else:
            return
        
    @staticmethod
    def join_path(path, *paths):
        return os.path.normpath(
            os.path.join(path, *paths)
        )


    @staticmethod
    def build(args):
        workspace = os.path.abspath(args.path)
        if args.watch:
            sledge.hammer(workspace, watch=args.watch)
        else:
            sledge.hammer(workspace)
    
    @staticmethod
    def initialize(args):
        path = args.path
        root = Clapi.join_path(path, 'src')
        dirs = ('src/pages', 'src/layout'
                ,'src/imports', 'src/panes', 'src/pages/.sledge')
        files = ('pages/.framerc', 'pages/index.frame'
                ,'panes/index.yml', 'layout/layout.frame'
                ,'layout/layout.yml')
        content = {
            '.framerc': Clapi.FRAMERC,
            'index.frame': '@load: rel-"panes" src-"../%s"\n${message}'%(files[2]),
            'index.yml': 'message: Hello, buddy!',
            'layout.frame': '@load: rel-"panes" src-"../%s"'%(files[4]),
            'layout.yml': '# some variable used in layout.frame'
        }
        root = os.path.abspath(root)
        if not os.path.exists(root):
            Clapi.make('dir', root)
        else:
            print('[exists]: path "%s" already exists'%root)
            sys.exit(1)
        
        for each in dirs:
            each = os.path.abspath(Clapi.join_path(path, each))
            if not os.path.exists(each):
                Clapi.make('dir', each)
            else:
                print('this directory "%s" has an ongoing project'%each)
                sys.exit(1)
        
        base = lambda p: os.path.basename(p) 
        for each in files:
            each = os.path.abspath(
                Clapi.join_path(path, 'src', each)
            )
            if not os.path.exists(each):
                Clapi.make('file', each, content[base(each)])
            else:
                print('this directory has an ongoing project')
                sys.exit(1)
        print('[success]: new project in "%s"'%(root))
        return 0

if __name__ == '__main__':
    Clapi.start()
