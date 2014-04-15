# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
from mock import Mock
from tekton.gae import middleware
from tekton.gae.middleware import router_middleware


def build_middleware(setup_return=False, execute_tear_down_on_error=False):
    mid = Mock()
    mid.set_up = Mock(return_value=setup_return)
    mid_class = Mock(return_value=mid)
    mid_class.execute_tear_down_on_error = execute_tear_down_on_error
    return mid_class, mid


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

    def test_successful_execute_2(self):
        mid_1_class, mid_1 = build_middleware()
        mid_2_class, mid_2 = build_middleware()

        middleware.execute_2([mid_1_class, mid_2_class], None)
        mid_1_class.assert_called_once_with(None, {}, {})
        mid_2_class.assert_called_once_with(None, {}, {})
        mid_1.set_up.assert_called_once_with()
        mid_2.set_up.assert_called_once_with()
        mid_1.tear_down.assert_called_once_with()
        mid_2.tear_down.assert_called_once_with()

    def test_stop_next_middleware_execute_2(self):
        mid_1_class, mid_1 = build_middleware(True)
        mid_2_class, mid_2 = build_middleware()

        middleware.execute_2([mid_1_class, mid_2_class], None)
        mid_1_class.assert_called_once_with(None, {}, {})
        self.assertFalse(mid_2_class.called)
        mid_1.set_up.assert_called_once_with()
        self.assertFalse(mid_2.set_up.called)
        mid_1.tear_down.assert_called_once_with()
        self.assertFalse(mid_2.tear_down.called)


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
