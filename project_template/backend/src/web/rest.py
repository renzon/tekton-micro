# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton.gae.middleware.json_middleware import JsonResponse


def items():
    JsonResponse({'data': [1, 2, 3]})