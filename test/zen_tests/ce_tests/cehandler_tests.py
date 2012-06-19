'''
Created on 02/02/2011

@author: Renzo Nuccitelli
'''
import unittest
from zen.ce.cehandler import BaseHandler


class Request(): 
    def get(self):
        pass
    
class Out():
    def write(self):
        pass


class Response(): 
    out=Out()


class TestRequestHandler(unittest.TestCase):
    def test_get(self):
        handler=BaseHandler()
        request=Request()
        request.path="br/oneTest/ARequestHandlerStub/aRequestMethod"
        response=Response()
        handler.request=request
        handler.response=response
        handler.make_convetion()
        self.assertEquals(request.param1,"1")
        self.assertEquals(request.methodExecutedName,"aRequestMethod")
        self.assertEquals(response.param2,"2")
        
        request.path="br/oneTest/ARequestHandlerStub/anotherRequestMethod"
        handler.make_convetion()
        self.assertEquals(request.param1,"8")
        self.assertEquals(request.methodExecutedName,"anotherRequestMethod")
        self.assertEquals(response.param2,"9")
        
        request.path="br/oneTest/ARequestHandlerStub/aRequestMethod/3"
        handler.make_convetion()
        self.assertEquals(request.param1,"3")
        self.assertEquals(request.methodExecutedName,"aRequestMethod")
        self.assertEquals(response.param2,"2")
        
        request.path="br/oneTest/ARequestHandlerStub/anotherRequestMethod/10"
        handler.make_convetion()
        self.assertEquals(request.param1,"10")
        self.assertEquals(request.methodExecutedName,"anotherRequestMethod")
        self.assertEquals(response.param2,"9")
        
        request.path="br/oneTest/ARequestHandlerStub/aRequestMethod/3/4"
        handler.make_convetion()
        self.assertEquals(request.param1,"3")
        self.assertEquals(request.methodExecutedName,"aRequestMethod")
        self.assertEquals(response.param2,"4")
        
        request.path="br/oneTest/ARequestHandlerStub/anotherRequestMethod/11/12"
        handler.make_convetion()
        self.assertEquals(request.param1,"11")
        self.assertEquals(request.methodExecutedName,"anotherRequestMethod")
        self.assertEquals(response.param2,"12")
        
        
