# Copyright (c) 2019 Caleb Adepitan. All rights reserved.
# Remarkup for HTML, python implementation.
# Sledge v1.0.0.
# Author(s): Caleb Pitan.
# The Remarkup guides that govern this implementation can be found at:
# https://framestd.github.io/sledge/remarkup/
# Developers Indulgent Program (DIP)
# Use of this source code is licensed under the MIT LICENSE
# which can be found in the LICENSE file.

from __future__ import print_function
import os
import time
import sys
msg = "{} is missing -- sledge {} continue without {}"
verbose = False

try:
    from termcolor import cprint
except ImportError:
    print(msg.format("termcolor", "will", "all those fancy colors"))
if os.name == 'nt':
    try:
        import colorama
        colorama.init()
    except ImportError:
        print(msg.format("colorama", "will", "all those fancy colors"))
        cprint = lambda m, *c: print(m)

def log(*msgs):
    print(*msgs)
def error(msg):
    cprint("[error]: {}".format(msg), "red")
    time.sleep(2.0)
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
def warn(msg):
    cprint("[warning]: {}".format(msg), "yellow")
    #time.sleep(0.75)
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
def info(msg):
    cprint(msg, "blue", attrs=["bold"])
    #time.sleep(0.5)
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
def success(msg):
    cprint("success: {}".format(msg), "green")
def aware(msg):
    cprint(msg, "cyan")
def sledge(msg, *args):
    cprint(msg, *args)