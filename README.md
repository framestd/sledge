[![Build Status](https://travis-ci.org/framestd/sledge.svg?branch=master)](https://travis-ci.org/framestd/sledge)  
[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Develop%20codes%20easily0%20no%20lag%Allow%20Sledge%20to%20handle %20your%20build.%20Get%20Sledge&url=https://github.com/framestd/sledge/&via=RealLongman&hashtags=python,sledge,templates,frame,developers,Remarkup,templatingengine,programming)
<p align="center">
    <img src="https://raw.githubusercontent.com/framestd/sledge/master/images/frame-text300.png" alt="Frame Logo"/>
</p>

# Sledge  
Sledge is the python implementation of the Frame Markup and Templating specificatons as defined by [Frame Studios](https://framestd.github.io/).  
If you are here, you must have been looking for ways to develop websites easily using HTML. Writing static HTML can be stressfull, but after you take your time to write like 10 web pages, you decide you have to change something. This is where the problem comes in, and you have to change that for each of the 10 pages. Think about when your pages grow more than just 10.  
Yes, you may be thinking this problem is already solved by most templating engines, but **_Sledge_**, using the **Frame Markup and Templating Spec** offers more.  
> **Note:** *As from now we shall refer to **Frame Markup and Templating Spec** as **FMTS***  
> **_Frame Markup_** _as_ **_frameup_**  
## What we offer in a nutshell  
FMTS offers:  
1. Time travel  
2. Frame  
3. Panes  

With Sledge and the FMTS in use:  
1. You can add preprocessors to your frameup -- here goes whatever you need to tell the compiler. Preprocessor are denoted with the &commat; operator. Here is an example for a page called `getstarted.frame`  
```html
@load: rel-"panes" src-"path/to/pane.json"
@load: rel-"dest" href-"this/folder/for/compiled/frameup/"
@load: rel-"layout" src-"this/page/layout.frame"
@import: src-"another.frame" as-"anotherframe" 
<!--then you can use ${anotherframe} -->
```  
The first `load` command relates the page to a pane.  
The second tells the engine the destination -- the folder where you want your `.html` files compiled from your `.frame` files to go  
The third specifies the layout to build the page on.  
### What are panes:  
> As the name suggests, a `pane` is just like a panel that fits into your `frame`. So the `pane` is just a `json` file containing variables that fits the ones your `frame` needs to access. This variables are formatted into your `frame` at compile time.  
### How to access variables  
> Variables are accessed using `$` followed by `{` `the path to the variable` and `}`  
> Example `${author}`, `${program::license}`  
> and a pane that looks much like:  
```yaml
- author: Caleb Pitan
- program:
    - name: Sledge
    - license: MIT 
- nav: 
    - links:
        - HREF: https://github.com/framestd/Sledge/
          TITLE: Sledge
        - HREF: https://github.com/framestd/
          TITLE: Frame Studios
```  
### More  
> There are also functions that does tedious works, fetch things for you and lots more.  
> Frame makes use of css class selector and id selector to specify class attributes and id attributes respectively.  
> etc...  
```html
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
```
**compiles to:**  
```html
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
## Using Sledge  
Sledge has all you need -- we already have a python file `app.py` that does your work for you **_check it out_** [app.py script](https://github.com/framestd/sledge/tree/master/scripts/app.py). You can write your own script if you think you want to have more than the priviledges `app.py` offers. The sledge package exports three methods: 
* `render(src, mode)` this may return a tuple or a compiled markup. `mode` tells it whether it's a layout file or not `mode=1` for layout files then it returns a compiled markup; `mode=0` default it returns tuple containing compiled page and all other information from the preprocessors.   
* `hammer(src)` this does the whole build work and returns nothing (void).  
* a bonus `get_all_files` that can walk directorys recursively and call private `__build` method to do the build job.  

### ..with bash
We do not provide any shell script yet, but we'll do soon  
```bash
cd scripts/bin #from Sledge install location
python app path/to/workspace #note the path is relative
                                 #so when resolved it will be "scripts/bin/path/to/workspace"
```   
### Using the `.cmd` script on Windows  
We provide a `.cmd` script which we called our **API Entry Point** 
```cmd
cd where\sledge\cmd\is
sledge script --update path/to/your-script.py
rem if you'd not use app.py but your own script
sledge nail path/to/workspace
```
# License  
Sledge is Licensed under MIT
