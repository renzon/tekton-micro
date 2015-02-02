# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import logging
import traceback
import time

from google.appengine.api import app_identity, mail, capabilities
from google.appengine.runtime import DeadlineExceededError
from tekton.gae.middleware import Middleware

from tekton.router import PathNotFound


def get_apis_statuses(e):
    if not isinstance(e, DeadlineExceededError):
        return {}
    t1 = time.time()
    statuses = {
        'blobstore': capabilities.CapabilitySet('blobstore').is_enabled(),
        'datastore_v3': capabilities.CapabilitySet('datastore_v3').is_enabled(),
        'datastore_v3_write': capabilities.CapabilitySet('datastore_v3', ['write']).is_enabled(),
        'images': capabilities.CapabilitySet('images').is_enabled(),
        'mail': capabilities.CapabilitySet('mail').is_enabled(),
        'memcache': capabilities.CapabilitySet('memcache').is_enabled(),
        'taskqueue': capabilities.CapabilitySet('taskqueue').is_enabled(),
        'urlfetch': capabilities.CapabilitySet('urlfetch').is_enabled(),
    }
    t2 = time.time()
    statuses['time'] = t2 - t1
    return statuses


def send_error_to_admins(settings, exception, handler, render, template, user):
    trace_back = traceback.format_exc()
    errmsg = exception.message

    logging.error(errmsg)
    logging.error(trace_back)
    handler.response.write(render(template))
    appid = app_identity.get_application_id()

    subject = 'ERROR in %s. Path: %s' % (appid, handler.request.path)
    body = """
------------- Logged User ------------
%(user)s
------------- request ------------
%(request)s
----------------------------------

------------- GET params ---------
%(get_params)s
----------------------------------

----------- POST params ----------
%(post_params)s
----------------------------------

----------- traceback ------------
%(trace_back)s
----------------------------------
""" % {'request': handler.request,
       'get_params': handler.request.GET,
       'post_params': handler.request.POST,
       'trace_back': trace_back,
       'user': user}
    body += 'API statuses = ' + json.dumps(get_apis_statuses(exception), indent=4)
    mail.send_mail_to_admins(sender=settings.SENDER_EMAIL,
                             subject=subject,
                             body=body)


class EmailMiddleware(Middleware):
    def handle_error(self, exception):
        import settings  # workaround. See https://github.com/renzon/zenwarch/issues/3

        if isinstance(exception, PathNotFound):
            self.handler.response.set_status(404)
            template = settings.TEMPLATE_404_ERROR
        else:
            self.handler.response.set_status(400)
            template = settings.TEMPLATE_400_ERROR
        _logged_user = self.dependencies['_logged_user']
        if _logged_user:
            _logged_user = _logged_user.to_dict(include=['id', 'email'])
        send_error_to_admins(settings, exception, self.handler, self.dependencies['_render'],
                             template, _logged_user)

