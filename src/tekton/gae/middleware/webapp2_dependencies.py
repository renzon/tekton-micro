# -*- coding]= utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton.gae.middleware import Middleware


class Webapp2Dependencies(Middleware):
    def set_up(self):
        self.dependencies["_req"] = self.handler.request
        self.dependencies["_resp"] = self.handler.response
        self.dependencies["_handler"] = self.handler
        self.dependencies["_dependencies"] = self.dependencies