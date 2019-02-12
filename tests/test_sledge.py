#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
test for sledge
using './lab_rat'
"""
import unittest
import sledge

var = "<div>\n  hello world\n</div>"
explode = """<ul>
  <li>
    Test
  </li>
  <li>
    <span>svg</span>
    <a href="explode">explode</a>
  </li>
  <li>
    <span>ico</span>
    <a href="links">links</a>
  </li>
</ul>"""

class TestOnLabRats(unittest.TestCase):
    def vars_test(self):
        sledge.hammer('lab_rat/pages/test_var.frame', ret=True)
        result = sledge.get_build_output()
        self.assertEqual(result, var)
    def func_test_explode(self):
        sledge.hammer('lab_rat/pages/test_func_explode.frame', ret=True)
        result = sledge.get_build_output()
        self.assertEqual(result, explode)