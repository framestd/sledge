[![Build Status](https://travis-ci.org/framestd/sledge.svg?branch=master)](https://travis-ci.org/framestd/sledge)  
[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Develop%20codes%20easily%20no%20lag.%20Allow%20Sledge%20to%20handle%20your%20build%20Get%20Sledge&url=https://github.com/framestd/sledge/&via=RealLongman&hashtags=python,sledge,templates,framestd,developers,remarkup,templatingengine,programming,web)
<p align="center">
  <img src="https://raw.githubusercontent.com/framestd/sledge/master/images/frame-text300.png" alt="Frame logo"/>
</p>

# Sledge  

## Warning
> Everything under this repository is still under development.  
> There are no official releases for the public yet.  
> To be informed when this repo leaves development and is released click the watch button in the top right corner relative to you, then choose your plan for the watch or you can star it to always remember to come back and check.  

Sledge is a powerful dev-tool for building, but not limited to, webpages. In fact, you can use sledge to build anything you deem suitable. Majorly you'd want to use it for HTML development. It makes the task of writing HTML easier. You may think of sledge as a **markup script**&mdash;a very easy and fast way to write what would be a complex markup in a simple way, and still get the same result.  
With this tool in your box, you should worry less about your markup and focus more on the functionality of your markup. Spend the time you need to write complex markup on scripting your markup's functionality, and your back-end's.

## What do I need?
Sledge is written in python, so you need python installed on your system. If you don't have python installed on your system and you run windows [download python](https://www.python.org/downloads/windows) for windows. If you are a linux user you should have python, you've just not unlocked it. Run this to unlock or consider this [python guide](https://docs.python-guide.org/starting/install3/linux/), but first check if it's installed, run:
```bash
python --version
# if this returns something like:
# Python 3.6.1
# or any other version like 2.7.14
# python is installed
# else run:
sudo apt-get update
sudo apt-get install python3.6
```  
Sledge is tested and runs fine with the following versions of python:  

1. Python 2.7  
2. Python 3.4  
3. Python 3.5  
4. Python 3.6  

So if your version is any of the above, sledge is yours.  

## What we offer in a nutshell  

1. Time travel: sledge gives you the ability to travel through time. With sledge you can deploy websites faster than ever before, and you can always easily go back in time to change the past.  
2. Frame: with the lock and key model, you can define markup that is not likely to change in what we call frame&mdash;the lock.  
3. Panes: still on the lock and key model, you can define variables, part of your markup that is likely to constantly change in your panes&mdash;the key.  
4. Scalability: scale large application to the size you can control. In the virtual view, make your application look simple, while it's really complex.  

## Keep your code on the cutting edge  
### Learn by examples  
You can add preprocessors to your markup -- here goes whatever you need to tell the compiler. Preprocessor are denoted with the `@` operator. Here is an example for a page called `getstarted.frame`  
```html
@load: rel-"panes" src-"path/to/pane.yml"
@load: rel-"dest" href-"this/folder/for/compiled/markup/"
@load: rel-"layout" src-"this/page/layout.frame"
@import: src-"another.frame" as-"anotherframe" 
<!--then you can use ${anotherframe} -->
```  
> **Note**: attributes and their values are case insensitive, save only values containig path which depends on your file system, and variable addresses.  
> We could rather say `rel` attributes and their values are case insensitive, but others are case sensitive.
> [Learn more from the docs](https://framestd.github.io/sledge/).  

**it could be**:
```html
@Load: rEl-"PANES" srC-"path/to/pane.yml"
@loAd: Rel-"Dest" HRef-"this/folder/for/compiled/markup/"
@load: REL-"layouT" src-"this/page/layout.frame"
@IMPORT: src-"another.frame" As-"anotherframe" 
<!--then you can use ${anotherframe} -->
```  
> But apply discretion so your code may be attractive and meaningful.

#### Explanation
> The first `load` command relates the page to a pane.  
> The second tells the engine the destination&mdash;the folder where you want your `.html` files compiled from your `.frame` files to go. If the left-most directory doesn't exist, it is created. 
> The third specifies the layout to build the page on. Layouts are shared resources between many pages. Many pages may link to one layout.  

### What are panes:  
As the name suggests, a `pane` is just like a panel that fits into your `frame`. So the `pane` is just a `YAML` source file containing variables that fits the ones your `frame` needs to access. This variables are locked into your `frame` at compile time.  

### How to access variables  
Variables are accessed using `$` followed by `{` `address` `}`  
Example `${author}`, `${program::license}`, and a pane that looks much like:  

```yaml
# say: example.yml
- author: Caleb Pitan
- program:
  - name: Sledge
  - license: MIT 
- nav: 
  - links:
    - HREF: https://github.com/framestd/sledge/
      TITLE: Sledge
    - HREF: https://github.com/framestd/
      TITLE: Frame Studios
```  
### More  
There are also functions that do tedious works, fetch things for you and lots more.  
Frame makes use of CSS `class` selector `.` and `id` selector `#` to specify class attributes and id attributes respectively. Classes can be chained together by another trailing dot then the classname. ID does not support chaining as one unique id per HTML element is the code, etc...  

```html
@load: rel-"panes" src-"example.yml"
<!--say: example.frame-->
<!--using the YAML source above as the pane-->
<div.container>
  <div.page#main>
    <p#help.hide.text>some help</p>
  </div>
  <span.nothing.goes.here//>
  <div.navlinks>
    <ul>
      %explode(
        <li>
          <a href="${HREF}">${TITLE}</a>
        </li>, nav::links
      )
    </ul>
  </div>
</div>
```  
**compiles to:**  
```html
<!--say: example.frame-->
<!--using the YAML source above as the pane-->
<div class="container">
  <div class="page" id="main">
    <p id="help" class="hide text">some help</p>
  </div>
  <span class="nothing goes here"></span>
  <div class="navlinks">
    <ul>
      <li>
        <a href="https://github.com/framestd/Sledge/">Sledge</a>
      </li>
      <li>
        <a href="https://github.com/framestd/">Frame Studios</a>
      </li>
    </ul>
  </div>
</div>
```  
> **Note**: preprocessors should be added at the begining of file, the parser terminates when it reads a token that is not a preprocessor, and never continue or come back to parse later.  

## Using Sledge  
Sledge has all you need -- we already have a python file `app.py` that does your work for you **_check it out_** [app.py script](https://github.com/framestd/sledge/blob/master/sledge.py). You can write your own script if you think you want to have more than the priviledges `app.py` offers. The sledge package exports three methods: 
* `render(src, mode)` this may return a tuple or a compiled markup. `mode` tells it whether it's a layout file or not `mode=1` for layout files then it returns a compiled markup; `mode=0` default it returns tuple containing compiled page and all other information from the preprocessors.   
* `hammer(src)` this does the whole build work and returns nothing (void).  
* a bonus `get_all_files` that can walk directorys recursively and call private `_build` method to do the build job.  

You can also automate your build. Using our `Vigilante` class you can watch files, limited to your pages only, i.e if your layout or panes&mdash;`.yml` sources are not in your pages directory then any change to layout or YAML source won't trigger a build. The directory passed from the command line as args to...as in:  

```bash
python sledge.py -w ../tests/pages 
# everything under this dir is watched
# [-w|--watch] will watch
python sledge.py ../tests/pages
# nothing is being watched
```  

### ..with bash
We do not provide any shell script yet, but we'll do soon  
```bash
python sledge.py --watch path/to/workspace 
# watching [-w|--watch]
```   
### ...with cmd  
We provide a `.cmd` script which we called our **API Entry Point** and idealy this should be used 

```batch
cd where\sledge\cmd\is
rem sledge script --update path/to/your-script.py
rem if you'll not use sledge.py but your own script
sledge nail -w path/to/workspace
rem watching path for changes
```  
# Installing Sledge  
As said [above](#warning) it is not yet production-ready, but when ready you can always install from [PyPI](https://www.pypi.org) using `pip`  
```bash
pip install <package-name>
```  
package name could be sledge we can't tell that now, depends on name availability.  
# Contributing  
Looking to be a contributor, no problem, you are welcome. Read our guidelines to contributing to sledge. We have a [CONTRIBUTING.md](https://github.com/framestd/sledge/blob/master/CONTRIBUTING.md) for that.  

# License  
Sledge is Licensed under [MIT](https://github.com/framestd/sledge/blob/master/LICENSE)
