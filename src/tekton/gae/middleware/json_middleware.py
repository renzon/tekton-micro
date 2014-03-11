# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json


def execute(next_process, handler, dependencies, **kwargs):
    def _json(dct, prefix=")]}',\n"):
        js = prefix + json.dumps(dct)
        resp = handler.response
        resp.headers[str('Content-Type')] = str('application/json')
        return resp.write(js)

    dependencies["_json"] = _json
    next_process(dependencies, **kwargs)
