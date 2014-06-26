# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest

from mock import Mock
from tekton.gae.middleware.json_middleware import JsonResponse, JsonResponseMiddlweare


class MiddlewareTests(unittest.TestCase):
    def test_json_secure(self):
        handler = Mock()
        handler.response.headers = {}
        dependencies = {'_fcn_response': JsonResponse({'param': 1})}

        JsonResponseMiddlweare(handler, dependencies,None).set_up()
        self.assertDictEqual({'Content-Type': 'application/json'}, handler.response.headers)
        handler.response.write.assert_called_with(''')]}\',\n{"param": 1}''')