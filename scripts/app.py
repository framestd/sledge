import sys
import os
sys.path.insert(0, "main")
import main
watch = False
workspace = os.path.abspath(sys.argv[1])
try:
    if sys.argv[1] == "-w" or sys.argv[1] == "--watch":
        watch = True
        workspace = os.path.abspath(sys.argv[2])
except IndexError:
    pass
print(watch)
main.hammer(workspace, watch)
