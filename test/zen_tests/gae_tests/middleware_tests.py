# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
from mock import Mock
from zen.gae import middleware
from zen.gae.middleware import router_middleware


class MiddlewareTests(unittest.TestCase):
    def test_execute(self):
        mid_flags = [False, False]

        def middleware_1(next_process, handler, dependencies, **kwargs):
            mid_flags[0] = True
            dependencies['_foo'] = 'foo'
            next_process(dependencies, kwarg_1='bar1')

        def middleware_2(next_process, handler, dependencies, **kwargs):
            mid_flags[1] = True
            self.assertEqual('foo', dependencies['_foo'])
            self.assertDictEqual({'kwarg_1': 'bar1'}, kwargs)
            next_process(dependencies, **kwargs)

        middleware.execute([middleware_1, middleware_2], None)
        self.assertListEqual([True, True], mid_flags)


    def test_router(self):
        f = Mock()

        router_middleware.router.to_handler = Mock(return_value=(f, []))
        handler = Mock()
        handler.request.path = '/first_handler/fnc'
        next_process = Mock()
        router_middleware.execute(next_process, handler, {})
        f.assert_called_with()
        next_process.assert_called_with({})
        router_middleware.router.to_handler.assert_called_with('/first_handler/fnc', {})
