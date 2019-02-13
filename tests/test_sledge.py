#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
test for sledge
using './lab_rat'
"""
import sys, os
import unittest
import yaml
import sledge

exp = yaml.load(open('tests/expected.yml').read())

test_var = os.path.abspath('tests/lab_rat/pages/test_var.frame')
test_explode = os.path.abspath('tests/lab_rat/pages/test_func_explode.frame')
test_encuri = os.path.abspath('tests/lab_rat/pages/test_func_encuri.frame')
test_b64 = os.path.abspath('tests/lab_rat/pages/test_func_b64.frame')
test_read = os.path.abspath('tests/lab_rat/pages/test_func_read.frame')
test_code = os.path.abspath('tests/lab_rat/pages/test_func_code.frame')
test_nullstr = os.path.abspath('tests/lab_rat/pages/test_nullstring.frame')
test_id_class = os.path.abspath('tests/lab_rat/pages/test_id_class.frame')

class TestOnLabRats(unittest.TestCase):
    def test_vars(self):
        sledge.hammer(test_var, ret=True)
        result = sledge.get_build_output()
        self.assertEqual(result, exp['var'])
    def test_func_explode(self):
        sledge.hammer(test_explode, ret=True)
        result = sledge.get_build_output()
        self.assertEqual(result, exp['explode'])
    def test_func_encuri(self):
        sledge.hammer(test_encuri, ret=True)
        result = sledge.get_build_output()
        self.assertEqual(str(result), exp['encuri'])
    def test_func_b64(self):
        sledge.hammer(test_b64,ret=True)
        result =  sledge.get_build_output()
        self.assertEqual(result, exp['b64'])
    def test_func_read(self):
        sledge.hammer(test_read, ret=True)
        result = sledge.get_build_output()
        self.assertEqual(result, exp['read'])
    def test_func_code(self):
        sledge.hammer(test_code, ret=True)
        result = sledge.get_build_output()
        self.assertEqual(result, exp['code'])
    def test_nullstring(self):
        sledge.hammer(test_nullstr, ret=True)
        result = sledge.get_build_output()
        self.assertEqual(result, '')
    def test_id_and_class(self):
        sledge.hammer(test_id_class, ret=True)
        result = sledge.get_build_output()
        self.assertEqual(result, exp['id_class'])

if __name__ == '__main__':
	unittest.main()