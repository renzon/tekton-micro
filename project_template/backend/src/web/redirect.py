# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton.gae.middleware.redirect import RedirectResponse
from web import home


def index():
    return RedirectResponse(home)

