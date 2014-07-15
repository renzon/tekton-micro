# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton import router
from tekton.gae.middleware import Middleware


class RouterMiddleware(Middleware):
    def set_up(self):
        fcn, path_args = router.to_handler(self.handler.request.path, self.dependencies, **self.request_args)
        self.dependencies['_fcn'] = fcn
        self.dependencies['_path_args'] = path_args


class ExecutionMiddleware(Middleware):
    def set_up(self):
        fcn = self.dependencies['_fcn']
        path_args = self.dependencies['_path_args']
        self.dependencies['_fcn_response'] = fcn(*path_args, **self.request_args)