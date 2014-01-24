# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton import router


def execute(next_process, handler, dependencies, **kwargs):
    fcn, params = router.to_handler(handler.request.path, dependencies, **kwargs)
    fcn(*params, **kwargs)
    next_process(dependencies, **kwargs)
