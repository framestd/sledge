@load: rel-"panes" src-"../panes/index.yml"
@load: rel-"dest" href-"../build"
@load: rel-"layout" src-"../layout.frame"
@load: rel-"specific" find-"index" src-"../panes/specific.yml"
<div.main-contents>
    ${name}
    ${FRAME::DIRNAME}
    ${FRAME::FILENAME}
</div>