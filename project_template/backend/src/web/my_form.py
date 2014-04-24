# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def index(_write_tmpl, name):
    _write_tmpl('form.html', {'name': name})
