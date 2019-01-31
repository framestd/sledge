import sys
import os
sys.path.insert(0, "main")
import main
workspace = os.path.abspath(sys.argv[1])
main.hammer(workspace)
