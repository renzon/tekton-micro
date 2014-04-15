# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from tekton.gae.middleware import Middleware


def _extract_values(handler, param, default_value=""):
    values = handler.request.get_all(param)
    if param.endswith("[]"):
        return param[:-2], values if values else []
    else:
        if not values: return param, default_value
        if len(values) == 1: return param, values[0]
        return param, values


def execute(next_process, handler, dependencies, **kwargs):
    json_header = r'application/json, text/plain, */*'
    header_value = getattr(handler.request, 'accept', None)
    header_value = getattr(header_value, 'header_value', None)
    # AngularJS Call
    if header_value == json_header and handler.request.body:
        kwargs.update(json.loads(handler.request.body))
    else:
        kwargs.update(dict(_extract_values(handler, a) for a in handler.request.arguments()))
    next_process(dependencies, **kwargs)


class RequestParamsMiddleware(Middleware):
    def set_up(self):
        json_header = r'application/json, text/plain, */*'
        header_value = getattr(self.handler.request, 'accept', None)
        header_value = getattr(header_value, 'header_value', None)
        # AngularJS Call
        if header_value == json_header and self.handler.request.body:
            self.request_args.update(json.loads(self.handler.request.body))
        else:
            self.request_args.update(dict(_extract_values(self.handler, a) for a in self.handler.request.arguments()))