# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import tmpl


def execute(next_process, handler, dependencies, **kwargs):
    def write_tmpl(template_name, values=None):
        values = values or {}
        return handler.response.write(tmpl.render(template_name, values))

    dependencies["_write_tmpl"] = write_tmpl
    dependencies["_render"] = tmpl.render
    next_process(dependencies, **kwargs)
