# -*- coding]= utf-8 -*-
from __future__ import absolute_import, unicode_literals


def execute(next_process, handler, dependencies, **kwargs):
    dependencies["_req"] = handler.request
    dependencies["_resp"] = handler.response
    dependencies["_handler"] = handler
    dependencies["_dependencies"] = dependencies
    next_process(dependencies, **kwargs)
