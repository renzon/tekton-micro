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


class Middleware(object):
    execute_tear_down_on_error = False

    def __init__(self, handler, dependecies, request_args):
        self.dependecies = dependecies
        self.handler = handler
        self.request_args = request_args

    def set_up(self):
        '''
        Must return True to stop next middleware execution
        '''
        pass

    def tear_down(self):
        pass


def execute_2(middleware_classes, handler):
    '''
    This version of execute uses Object Orientation to keep stack trace clean
    Middlewares must be Middleware classes to be executed
    '''
    dependecies = {}
    request_args = {}
    executed_middlewares = []
    for mid_class in middleware_classes:
        mid_obj = mid_class(handler, dependecies, request_args)
        executed_middlewares.append(mid_obj)
        should_stop_next_middleware = mid_obj.set_up()
        if should_stop_next_middleware:
            break

    for mid in reversed(executed_middlewares):
        mid.tear_down()


