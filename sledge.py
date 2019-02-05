import sys
import os
sys.path.insert(0, "sledge")
import sledge
watch = False
workspace = os.path.abspath(sys.argv[1])
try:
    if sys.argv[1] == "-w" or sys.argv[1] == "--watch":
        watch = True
        workspace = os.path.abspath(sys.argv[2])
except IndexError:
    pass
sledge.hammer(workspace, watch)
