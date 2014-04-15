# -*- coding]= utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton.gae.middleware import Middleware


def execute(next_process, handler, dependencies, **kwargs):
    dependencies["_req"] = handler.request
    dependencies["_resp"] = handler.response
    dependencies["_handler"] = handler
    dependencies["_dependencies"] = dependencies
    next_process(dependencies, **kwargs)


class Webapp2Dependencies(Middleware):
    def set_up(self):
        self.dependencies["_req"] = self.handler.request
        self.dependencies["_resp"] = self.handler.response
        self.dependencies["_handler"] = self.handler
        self.dependencies["_dependencies"] = self.dependencies