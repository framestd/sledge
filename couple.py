from __future__ import print_function
import os
import sys

pkg = {
    'copyright': '2019 Caleb Adepitan',
    'name': 'Sledge',
    'version': '1.0.0',
    'authors': ['Caleb Pitan'],
    'license': 'MIT',
    'dist': 'sledge',
    'repo': 'https://github.com/framestd/sledge/',
    'site': 'https://framestd.github.io/sledge/'
}

banner = """Copyright (c) {}. All rights reserved.
Remarkup for HTML, python implementation.
{} v{}.
Author(s): {}.
The Remarkup guides that govern this implementation can be found at:
https://framestd.github.io/sledge/remarkup/
Developers Indulgent Program (DIP)
Use of this source code is licensed under the {} LICENSE
which can be found in the LICENSE file."""

banner = banner.format(pkg["copyright"], pkg['name'], pkg['version'], (''.join(pkg['authors'])), pkg['license'])
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
    global path
    src = os.path.join(p,f)
    from sledge import jobs
    pd = jobs.path_diff(path, p)['positive']
    pd = '' if pd is None else pd
    dest = os.path.join(dist, pd, f)
    print('copying "%s" to "%s"'%(src, dest))
    fs = open(src)
    fc = fs.read()
    fc = '# ' + banner + '\n\n' + fc
    fd = open(dest, 'w')
    fd.write(fc)
    fs.close()
    fd.close()

absp = os.path.dirname(os.path.abspath(sys.argv[0]))
#path = os.path.join(absp, 'scripts') # no need to use absolute path
path = 'scripts'
get_all_files(path, '.vs', '.vscode', '__pycache__')#py3 env

