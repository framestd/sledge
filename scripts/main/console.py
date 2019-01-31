from __future__ import print_function
msg = "{} is missing -- sledge {} continue without {}"
cprint = lambda m, c: print(m)
try:
    import colorama
    colorama.init()
except ImportError:
    print(msg.format("colorama", "will", "all those fancy colors"))
try:
    if colorama:
        from termcolor import cprint
except ImportError:
    print(msg.format("termcolor", "will", "all those fancy colors"))

def log(msg):
    cprint(msg, "white")
def error(msg):
    cprint(msg, "red")
def warn(msg):
    cprint(msg, "yellow")
def info(msg):
    cprint(msg, "blue", attrs=["bold"])
def success(msg):
    cprint(msg, "green")
def aware(msg):
    cprint(msg, "cyan")
def sledge(msg, *args):
    cprint(msg, *args)