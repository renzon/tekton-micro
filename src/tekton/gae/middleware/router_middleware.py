# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton import router
from tekton.gae.middleware import Middleware


def execute(next_process, handler, dependencies, **kwargs):
    fcn, params = router.to_handler(handler.request.path, dependencies, **kwargs)
    fcn(*params, **kwargs)
    next_process(dependencies, **kwargs)

class RouterMiddleware(Middleware):
    def set_up(self):
        fcn, params = router.to_handler(self.handler.request.path, self.dependencies, **self.request_args)
        fcn(*params, **self.request_args)
