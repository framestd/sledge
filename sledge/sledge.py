import sys
import os
from . import hammer
watch = False
workspace = os.path.abspath(sys.argv[1])
def main():
	try:
    	if sys.argv[1] == "-w" or sys.argv[1] == "--watch":
        	watch = True
        	workspace = os.path.abspath(sys.argv[2])
	except IndexError:
    	pass
	hammer(workspace, watch)
if __name__ == '__main__':
	main()
