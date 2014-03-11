# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
from mock import Mock
from tekton import json_middleware


class MiddlewareTests(unittest.TestCase):
    def test_json(self):
        handler = Mock()
        handler.response.headers = {}
        next_process = Mock()
        dependencies = {}
        json_middleware.execute(next_process, handler, dependencies)
        next_process.assert_called_with(dependencies)
        self.assertTrue('_json' in dependencies)
        json_dependencie = dependencies['_json']
        json_dependencie({'param': 1})
        self.assertDictEqual({'Content-Type': 'application/json'}, handler.response.headers)
        handler.response.write.assert_called_with(''')]}\',\n{"param": 1}''')
        json_dependencie({'param': 1}, prefix='')
        handler.response.write.assert_called_with('''{"param": 1}''')