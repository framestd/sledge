# Copyright 2019 Frame Studios. All rights reserved.
# Frame v1.0 python implementation by some Pane-in-the-Frame developers.
# pyFrame v1.0
# Project Manager: Caleb Adepitan
# The Frame specifications that govern this implementation can be found at:
# https://frame.github.io/spec/v1/
# Developers Indulgent Program (DIP)
# Use of this source code is licensed under the GPL 2.0 LICENSE
# which can be found in the LICENSE file.
# In attribution to Realongman, Inc.

import re

# escape entities
# # = &num;
# . = &period;
# $ = &dollar;
# : = &colon;
# :: = &dblcln; (non-standard entity)
# ! = &excl;
# % = &percnt;
# @ = &commat;
# & = &amp

"""These are the html entities for characters that may
have special meanings in the frame markup.
These characters cannot be written as they are in a frame markup;
as they may be parsed with respect to their meanings in a frame.
    How to escape: 
        (1) `&num;` will print `#`;
        (2) `&amp;num;` will print `&num;`
    So if you want a real `&num;` to appear in your compiled markup
    for the client or browser to parse, you'd write as (2).
    The escape is only needed for those characters that have special
    meanings in frame -- others don't need to be escaped
    As in:
        `&amp;num;` will print `&num;`
        `&num;` will print `#`
        but
        `&quot;` remains as `&quot;` 
        It is not frame's business."""
ENTITY_MAP = {
    "&num;": "#",
    "&period;": ".",
    "&dollar;": "$",
    "&colon;": ":",
    "&dblcln;": "::",
    "&excl;": "!",
    "&percnt;": "%",
    "&commat;": "@",
    "&amp;": "&"
}

def esc(text):
    for entity, char in ENTITY_MAP.items():
        text = re.sub(entity, char, text)
    return text
