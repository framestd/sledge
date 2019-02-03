import sys
import os
sys.path.insert(0, "main")
import main
watch = False
workspace = os.path.abspath(sys.argv[1])
try:
    if sys.argv[2] == "-w" or sys.argv[2] == "--watch":
        watch = True
except IndexError:
    pass
print(watch)
main.hammer(workspace, watch)
