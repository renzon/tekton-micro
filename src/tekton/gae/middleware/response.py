# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class ResponseBase(object):
    def __init__(self, context):
        self.context = context
