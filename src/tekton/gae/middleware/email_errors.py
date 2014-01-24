# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import logging
import traceback
import time

from google.appengine.api import app_identity, mail, capabilities
from google.appengine.runtime import DeadlineExceededError

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


def send_error_to_admins(exception, handler, write_tmpl):
    import settings  # workaround. See https://github.com/renzon/zenwarch/issues/3
    tb = traceback.format_exc()
    errmsg = exception.message

    logging.error(errmsg)
    logging.error(tb)
    write_tmpl("/templates/error.html")
    appid = app_identity.get_application_id()

    subject = 'ERROR in %s: [%s] %s' % (appid, handler.request.path, errmsg)
    body = """
------------- request ------------
%s
----------------------------------

------------- GET params ---------
%s
----------------------------------

----------- POST params ----------
%s
----------------------------------

----------- traceback ------------
%s
----------------------------------
""" % (handler.request, handler.request.GET, handler.request.POST, tb)
    body += 'API statuses = ' + json.dumps(get_apis_statuses(exception), indent=4)
    mail.send_mail_to_admins(sender=settings.SENDER_EMAIL,
                             subject=subject,
                             body=body)


def execute(next_process, handler, dependencies, **kwargs):
    try:
        next_process(dependencies, **kwargs)
    except PathNotFound, e:
        handler.response.set_status(404)
        send_error_to_admins(e, handler, dependencies['_write_tmpl'])
    except BaseException, e:
        handler.response.status_code = 400
        send_error_to_admins(e, handler, dependencies['_write_tmpl'])
