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
ENTITY_MAP = [
    ("&num;", "#"),
    ("&period;", "."),
    ("&dollar;", "$"),
    ("&colon;", ":"),
    ("&dblcln;", "::"),
    ("&excl;", "!"),
    ("&percnt;", "%"),
    ("&commat;", "@"),
    ("&amp;", "&")
]

def escape(text):
    if not text: return
    for entity, char in ENTITY_MAP:
        text = text.replace(entity, char)
    return text
