# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from tekton.gae.middleware import Middleware
from tekton.gae.middleware.response import ResponseBase


class JsonResponse(ResponseBase):
    def __init__(self, context, secure_prefix=")]}',\n"):
        super(JsonResponse, self).__init__(context)
        self.secure_prefix = secure_prefix

    def to_json(self):
        return self.secure_prefix + json.dumps(self.context)


class JsonUnsecureResponse(JsonResponse):
    def __init__(self, context, secure_prefix=''):
        super(JsonUnsecureResponse, self).__init__(context, secure_prefix)


class JsonResponseMiddleware(Middleware):
    def set_up(self):
        fcn_response = self.dependencies['_fcn_response']
        if isinstance(fcn_response, JsonResponse):
            resp = self.handler.response
            resp.headers[str('Content-Type')] = str('application/json')
            resp.write(fcn_response.to_json())
            return True  # after response, there is no need to look for more middlewares



