# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import bisect
from collections import defaultdict
import json
from tekton.gae.middleware import Middleware


class _ParamExtractor(object):
    def __init__(self):
        self.indexed_values = defaultdict(list)
        self.indexed_indexes = defaultdict(list)


    def _extract_values(self, handler, param, default_value=""):
        def handle_single_value(default_value, param, values):
            if not values:
                return param, default_value
            if len(values) == 1:
                return param, values[0]
            return param, values

        values = handler.request.get_all(param)
        if param.endswith('[]'):
            return param[:-2], values if values else []
        elif param.endswith(']') and '[' in param:
            try:
                param_name, param_idx = param[:-1].split('[')
                _, val = handle_single_value(default_value, param, values)
                param_idx = int(param_idx)
                sorted_list = self.indexed_values[param_name]
                sorted_indexes = self.indexed_indexes[param_name]
                idx = bisect.bisect_right(sorted_indexes, param_idx)
                sorted_list.insert(idx, val)
                sorted_indexes.insert(idx, param_idx)
                return param_name, sorted_list
            except:
                pass

        return handle_single_value(default_value, param, values)


class RequestParamsMiddleware(Middleware):
    def set_up(self):
        json_header = r'application/json, text/plain, */*'
        header_value = getattr(self.handler.request, 'accept', None)
        header_value = getattr(header_value, 'header_value', None)
        # AngularJS Call
        if header_value == json_header and self.handler.request.body:
            self.request_args.update(json.loads(self.handler.request.body))
        else:
            extractor = _ParamExtractor()
            self.request_args.update(
                dict(extractor._extract_values(self.handler, a) for a in self.handler.request.arguments()))