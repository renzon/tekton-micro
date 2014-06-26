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
    return mid_class, mid


class MiddlewareTests(unittest.TestCase):
    def test_successful_execute(self):
        mid_1_class, mid_1 = build_middleware()
        mid_2_class, mid_2 = build_middleware()

        middleware.execute([mid_1_class, mid_2_class], None)
        mid_1_class.assert_called_once_with(None, {}, {})
        mid_2_class.assert_called_once_with(None, {}, {})
        mid_1.set_up.assert_called_once_with()
        mid_2.set_up.assert_called_once_with()
        mid_1.tear_down.assert_called_once_with()
        mid_2.tear_down.assert_called_once_with()

    def test_stop_next_middleware_execute(self):
        mid_1_class, mid_1 = build_middleware(True)
        mid_2_class, mid_2 = build_middleware()

        middleware.execute([mid_1_class, mid_2_class], None)
        mid_1_class.assert_called_once_with(None, {}, {})
        self.assertFalse(mid_2_class.called)
        mid_1.set_up.assert_called_once_with()
        self.assertFalse(mid_2.set_up.called)
        mid_1.tear_down.assert_called_once_with()
        self.assertFalse(mid_2.tear_down.called)

    def test_middleware_with_error(self):
        mid_1_class, mid_1 = build_middleware()
        mid_2_class, mid_2 = build_middleware()
        mid_3_class, mid_3 = build_middleware()

        def f():
            raise Exception()

        mid_2.set_up = f

        middleware.execute([mid_1_class, mid_2_class, mid_3_class], None)
        mid_1_class.assert_called_once_with(None, {}, {})
        mid_2_class.assert_called_once_with(None, {}, {})
        self.assertFalse(mid_3_class.called)
        mid_1.set_up.assert_called_once_with()
        self.assertFalse(mid_3.set_up.called)
        self.assertFalse(mid_1.tear_down.called)
        self.assertFalse(mid_2.tear_down.called)
        self.assertFalse(mid_3.tear_down.called)
        self.assertTrue(mid_1.handle_error.called)
        self.assertTrue(mid_2.handle_error.called)

