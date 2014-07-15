# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from tekton import router
from tekton.gae.middleware import Middleware
from tekton.gae.middleware.response import ResponseBase


class RedirectResponse(ResponseBase):
    def __init__(self, handler_fcn, *params, **query_string):
        super(RedirectResponse, self).__init__(router.to_path(handler_fcn, *params, **query_string))


class RedirectMiddleware(Middleware):
    def set_up(self):
        fcn_response = self.dependencies['_fcn_response']
        if isinstance(fcn_response, RedirectResponse):
            self.handler.redirect(fcn_response.context)
            return True  # after response, there is no need to look for more middlewares

