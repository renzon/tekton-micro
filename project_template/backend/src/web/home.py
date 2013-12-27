# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from web_test import my_form
from zen import router


def index(_write_tmpl):
    url = router.to_path(my_form)
    _write_tmpl('templates/home.html', {'form_url': url})
