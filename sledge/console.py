# Copyright 2019 Frame Studios. All rights reserved.
# Remarkup v1.0 python implementation.
# Sledge v1.0.
# Project Manager: Caleb Adepitan.
# The Remarkup specifications that govern this implementation can be found at:
# https://framestd.github.io/remarkup/spec/v1/
# Developers Indulgent Program (DIP)
# Use of this source code is licensed under the MIT LICENSE
# which can be found in the LICENSE file.

from __future__ import print_function
import os
msg = "{} is missing -- sledge {} continue without {}"
cprint = lambda m, c: print(m)
if os.name == 'nt':
    try:
        import colorama
        colorama.init()
    except ImportError:
        print(msg.format("colorama", "will", "all those fancy colors"))
try:
    from termcolor import cprint
except ImportError:
    print(msg.format("termcolor", "will", "all those fancy colors"))

def log(*msgs):
    print(*msgs)
def error(msg):
    cprint("error: {}".format(msg), "red")
def warn(msg):
    cprint("warning: {}".format(msg), "yellow")
def info(msg):
    cprint(msg, "blue", attrs=["bold"])
def success(msg):
    cprint("success: {}".format(msg), "green")
def aware(msg):
    cprint(msg, "cyan")
def sledge(msg, *args):
    cprint(msg, *args)