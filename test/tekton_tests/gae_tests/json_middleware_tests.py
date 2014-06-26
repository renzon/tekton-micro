# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest

from mock import Mock
from tekton.gae.middleware.json_middleware import JsonResponse, JsonResponseMiddleware, JsonUnsecureResponse


class MiddlewareTests(unittest.TestCase):
    def assert_json_return(self, json_response_class, param_):
        handler = Mock()
        handler.response.headers = {}
        dependencies = {'_fcn_response': json_response_class({'param': 1})}
        JsonResponseMiddleware(handler, dependencies, None).set_up()
        self.assertDictEqual({'Content-Type': 'application/json'}, handler.response.headers)
        handler.response.write.assert_called_with(param_)

    def test_json_secure(self):
        self.assert_json_return(JsonResponse, ''')]}\',\n{"param": 1}''')

    def test_json_unsecure(self):
        self.assert_json_return(JsonUnsecureResponse, '''{"param": 1}''')