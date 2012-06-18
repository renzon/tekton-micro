'''
Created on 02/02/2011

@author: Renzo Nuccitelli
'''

import webapp2
from zen.ce import cengine


class BaseHandler(webapp2.RequestHandler):
    def get(self):
        self.make_convetion()
        
    def post(self):
        self.make_convetion()
        
    def make_convetion(self):
        (handler_class, method_name, params) = cengine.to_handler(self.request.path)
        handler = handler_class()
        handler.request = self.request
        handler.get=self.request.get
        handler.write=self.response.out.write
        handler.response = self.response
        handler.handler = self
        handler.redirect=self.redirect
        method = getattr(handler, method_name)
        method(*params)


app = webapp2.WSGIApplication([("/.*", BaseHandler)], debug = False)

