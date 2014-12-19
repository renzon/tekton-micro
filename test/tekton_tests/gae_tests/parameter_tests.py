# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from unittest import TestCase
from mock import Mock
from tekton.gae.middleware.parameter import _extract_values


class ExtractValueTests(TestCase):
    def handler_mock(self, return_value):
        handler = Mock()
        handler.request.get_all = Mock(return_value=return_value)
        return handler

    def test_list(self):
        handler_mock = self.handler_mock(['1', '2'])
        tpl = _extract_values(handler_mock, {}, 'some_list[]')
        self.assertTupleEqual(('some_list', ['1', '2']), tpl)

        handler_mock = self.handler_mock(['1'])
        tpl = _extract_values(handler_mock, {}, 'some_list[]')
        self.assertTupleEqual(('some_list', ['1']), tpl, 'Should return list because of "[]"')

        handler_mock = self.handler_mock(['1'])
        tpl = _extract_values(handler_mock, {}, 'single')
        self.assertTupleEqual(('single', '1'), tpl, 'Should return only "1" and not a list')

        handler_mock = self.handler_mock(['1', '2'])
        tpl = _extract_values(handler_mock, {}, 'single')
        self.assertTupleEqual(('single', ['1', '2']), tpl)

    def test_indexed_list(self):
        handler_mock = self.handler_mock('1')
        request_args = {}

        tpl = _extract_values(handler_mock, request_args, 'list_indexed[1]')
        self.assertTupleEqual(('list_indexed', ['1']), tpl)

        request_args['list_indexed'] = tpl[1]
        handler_mock = self.handler_mock('3')

        tpl = _extract_values(handler_mock, request_args, 'list_indexed[3]')
        # Must keep list ordered based on index
        self.assertTupleEqual(('list_indexed', ['1', '3']), tpl)

        request_args['list_indexed'] = tpl[1]

        handler_mock = self.handler_mock('2')

        tpl = _extract_values(handler_mock, request_args, 'list_indexed[2]')
        # Must keep list ordered based on index
        self.assertTupleEqual(('list_indexed', ['1', '2', '3']), tpl)

    def test_default(self):
        handler_mock = self.handler_mock(None)
        tpl = _extract_values(handler_mock, {}, 'empty_str')
        self.assertTupleEqual(('empty_str', ''), tpl)

        tpl = _extract_values(handler_mock, {}, 'none', None)
        self.assertTupleEqual(('none', None), tpl)

        tpl = _extract_values(handler_mock, {}, 'foo', 'bar')
        self.assertTupleEqual(('foo', 'bar'), tpl)



