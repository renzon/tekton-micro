'''
Created on 31/01/2011

@author: Renzo Nuccitelli
'''
import inspect



class ARequestHandlerStub(object):
    def aRequestMethod(self,param1="1",param2="2"):
        self.request.param1=param1
        self.request.methodExecutedName="aRequestMethod"
        self.response.param2=param2
        
    def anotherRequestMethod(self,param1="8",param2="9"): 
        self.request.param1=param1
        self.request.methodExecutedName="anotherRequestMethod"
        self.response.param2=param2

print inspect.isclass(ARequestHandlerStub())
