# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class Middleware(object):
    def __init__(self, handler, dependencies, request_args):
        self.dependencies = dependencies
        self.handler = handler
        self.request_args = request_args

    def set_up(self):
        """
        Must return True to stop next middleware execution
        """
        pass

    def tear_down(self):
        pass

    def handle_error(self, e):
        pass


def execute(middleware_classes, handler):
    """
    This version of execute uses Object Orientation to keep stack trace clean
    Middlewares must be Middleware classes to be executed
    """
    dependecies = {}
    request_args = {}
    executed_middlewares = []
    exception = None
    for mid_class in middleware_classes:
        mid_obj = mid_class(handler, dependecies, request_args)
        executed_middlewares.append(mid_obj)
        try:
            should_stop_next_middleware = mid_obj.set_up()
            if should_stop_next_middleware:
                break
        except Exception, e:
            exception = e
            break

    for mid in reversed(executed_middlewares):
        if exception:
            mid.handle_error(exception)
        else:
            mid.tear_down()


