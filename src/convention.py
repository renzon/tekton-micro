import logging
import traceback
import webapp2
from zen import router
from zen.router import PathNotFound

def _extract_values(handler,param,default_value=""):
    values=handler.request.get_all(param)
    if param.endswith("[]"):
        return param[:-2],values if values else []
    else:
        if not values: return param,default_value
        if len(values)==1: return param,values[0]
        return param,values


class BaseHandler(webapp2.RequestHandler):
    def get(self):
        self.make_convetion()

    def post(self):
        self.make_convetion()

    def make_convetion(self):
        kwargs=dict(_extract_values(self,a) for a in self.request.arguments())
        convention_params={"req": self.request,"resp": self.response,
                           "handler": self}
        try:
            fcn,params = router.to_handler(self.request.path,convention_params,**kwargs)
            fcn(*params,**kwargs)
        except PathNotFound:
            logging.error("Path not Found: "+self.request.path)
        except:
            logging.error((fcn,params,kwargs))
            logging.error(traceback.format_exc())


app = webapp2.WSGIApplication([("/.*", BaseHandler)], debug = False)

