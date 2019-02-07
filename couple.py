from __future__ import print_function
import yaml
import os
import sys

banner = """Copyright {}. All rights reserved.
Remarkup v1.0 python implementation.
{} v{}.
Project Manager: {}.
The Remarkup specifications that govern this implementation can be found at:
https://framestd.github.io/remarkup/spec/v1/
Developers Indulgent Program (DIP)
Use of this source code is licensed under the {} LICENSE
which can be found in the LICENSE file."""
package = open("package.yml")
pkg = yaml.load(package)
pkg = pkg['package']
banner = banner.format(pkg["copyright"], pkg['name'], pkg['version'], pkg['authors'][1], pkg['license'])
banner = '# '.join(banner.splitlines(True))
dist = pkg['dist']

if not os.path.exists(dist):
    os.mkdir(dist)

def get_all_files(path, *ignore):
    allfiles = os.listdir(path)
    dirsOnly = os.listdir(path)
    temp = []
    for eachfile in allfiles:
        if eachfile.endswith('.pyc'): continue
        if os.path.isfile(os.path.join(path, eachfile)):
            temp.append(eachfile)
            dirsOnly.remove(eachfile)
    for each in temp:
        couple(path, each)
    for eachdir in dirsOnly:
        if os.path.isdir(os.path.join(path, eachdir)) and not eachdir in ignore:
            get_all_files(os.path.join(path, eachdir), *ignore)

def couple(p, f):
    print(p, f)
    src = os.path.join(p,f)
    dest = os.path.join(dist, f)
    fs = open(src)
    fc = fs.read()
    fc = '# ' + banner + '\n\n' + fc
    fd = open(dest, 'w')
    fd.write(fc)
    fs.close()
    fd.close()

absp = os.path.dirname(os.path.abspath(sys.argv[0]))
path = os.path.join(absp, 'scripts')
get_all_files(path, '.vs', '.vscode', '__pycache__')#py3 env
"""try:
    raw_input('press return to cancel')
except KeyboardInterrupt:
    sys.exit(0)"""
