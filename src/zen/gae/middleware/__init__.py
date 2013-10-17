# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def execute(midlewares, handler, dependencies=None, **kwargs):
    if midlewares:
        dependencies = dependencies or {}
        current_middleware = midlewares[0]

        def next_process(dependencies, **kwargs):
            next_middlewares = midlewares[1:]
            execute(next_middlewares, handler, dependencies, **kwargs)

        current_middleware(next_process, handler, dependencies, **kwargs)



