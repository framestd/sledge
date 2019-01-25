[![Build Status](https://travis-ci.org/framestd/pyframe.svg?branch=master)](https://travis-ci.org/framestd/pyframe)
<p align="center">
    <img src="https://raw.githubusercontent.com/framestd/pyframe/master/images/frame-text300.png" alt="Frame Logo"/>
</p>

# pyframe  
pyframe is the python implementation of the Frame Markup and Templating specificatons as defined by [Frame Studios](https://framestd.github.io/).  
If you are here, you must have been looking for ways to develop websites easily using HTML. Writing static HTML can be stressfull, but after you take your time to write like 10 web pages, you decide you have to change something. This is where the problem comes in, and you have to change that for each of the 10 pages. Think about when your pages grow more than just 10.  
Yes, you may be thinking this problem is already solved by most templating engines, but **_pyframe_**, using the **Frame Markup and Templating Spec** offers more.  
> **Note:** *As from now we shall refer to **Frame Markup and Templating Spec** as **FMTS***  
> **_Frame Markup_** _as_ **_frameup_**  
## What we offer in a nutshell  
FMTS offers:  
1. Time travel  
2. Frame  
3. Panes  
With pyframe and the FMTS in use:  
1. You can add preprocessors to your frameup -- here goes whatever you need to tell the compiler. Preprocessor are denoted with the &commat; operator. Here is an example for a page called `getstarted.frame`  
```html
@load: rel-"panes" src-"path/to/pane.json"
@load: rel-"dest" href-"this/folder/for/compiled/frameup/"
@load: rel-"layout" src-"this/page/layout.frame"
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
```json
{
    "author": "Caleb Pitan",
    "program": {
        "name": "pyframe",
        "license": "GPL-2.0" 
    },
    "nav": {
        "links": [{
            "HREF": "https://github.com/framestd/pyframe/",
            "TITLE": "pyframe"
        },{
            "HREF": "https://github.com/framestd/",
            "TITLE": "Frame Studios"
        }]
    }
}
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
                <a href="https://github.com/framestd/pyframe/">pyframe</a>
            </li>
            <li>
                <a href="https://github.com/framestd/">Frame Studios</a>
            </li>
        </ul>
    </div>
</div>
```  
## Using pyframe  
Using pyframe, you need to write your python script that uses the engine `engine.py`, the engine simplifies the usage. In this script you call the `buildall` method of `engine` and give it a workspace where you want it to build files from e.g `user/my/workspace/` **_check it out_** [MyBuild script](https://github.com/framestd/pyframe/tree/master/blob/scripts/MyBuild.py). You are meant to override the `TITLE` and `METAS` function of the class `engine.MyFrame` to set specific frames as `${FRAME::TITLE}` or `${FRAME::METAS}` -- `${FRAME::METAS::desc}, ${FRAME::METAS::author}` etc.  
We also provide a `.cmd` script which we called our **API Entry Point**  
### Using the `.cmd` script  
```cmd
cd where\frame\cmd\is
frame script --update path/to/MyBuild.py
frame start whatever argument MyBuild takes
```
# License  
pyframe is Licensed under GPL-2.0