'''
Created on 31/01/2011

@author: Renzo Nuccitelli
'''

import unittest
import br
from br.handler.oneTest import ARequestHandlerStub
from br.handler import oneTest
from br import handler
from ex import handler as ex_handler
import home
from zen.ce import cengine


class PathToHandlerTestCase(unittest.TestCase):
    def test_handler_not_found_path_to_handler(self):
        self.assertRaises(cengine.HandlerNotFound,cengine.to_handler,"br/oneTest/ARequestHandlerStub/aRequestMetho")
        self.assertRaises(cengine.HandlerNotFound,cengine.to_handler,"br/oneTest/ARequestHandlerStub")
        self.assertRaises(cengine.HandlerNotFound,cengine.to_handler,"br/oneTest/ARequestHandlerStu")
        self.assertRaises(cengine.HandlerNotFound,cengine.to_handler,"br/oneTest")
        self.assertRaises(cengine.HandlerNotFound,cengine.to_handler,"br/oneT")
        self.assertRaises(cengine.HandlerNotFound,cengine.to_handler,"br/co")
        self.assertRaises(cengine.HandlerNotFound,cengine.to_handler,"br")
        
    def test_sucess_path_to_handler(self):
        result=cengine.to_handler("/br/oneTest/ARequestHandlerStub/aRequestMethod")
        self.assertEquals(result[0],ARequestHandlerStub)
        self.assertEquals(result[1],"aRequestMethod")
        self.assertEquals(len(result[2]),0)
        result=cengine.to_handler("/br/oneTest/ARequestHandlerStub/aRequestMethod/param1")
        self.assertEquals(result[0],ARequestHandlerStub)
        self.assertEquals(result[1],"aRequestMethod")
        self.assertEquals(result[2],["param1"])
        result=cengine.to_handler("/br/oneTest/ARequestHandlerStub/aRequestMethod/param1/param2")
        self.assertEquals(result[0],ARequestHandlerStub)
        self.assertEquals(result[1],"aRequestMethod")
        self.assertEquals(result[2],["param1","param2"])
        
        result=cengine.to_handler("/")
        self.assertEquals(result[0], home)
        self.assertEquals(result[1],"index")
        
        result=cengine.to_handler("/1")
        self.assertEquals(result[0], home)
        self.assertEquals(result[1],"index")
        self.assertEquals(result[2],["1"])
        
        result=cengine.to_handler("/ex")
        self.assertEquals(result[0],ex_handler.home)
        self.assertEquals(result[1],"index")
        
        result=cengine.to_handler("/ex/not_home")
        self.assertEquals(result[0],ex_handler.not_home)
        self.assertEquals(result[1],"index")
        
        result=cengine.to_handler("/ex/1")
        self.assertEquals(result[0],ex_handler.home)
        self.assertEquals(result[1],"index")
        self.assertEquals(result[2],["1"])
        
        
        
        result=cengine.to_handler("/ex/not_home/1")
        self.assertEquals(result[0],ex_handler.not_home)
        self.assertEquals(result[2],["1"])
        
        

class HandlerToPathTestCase(unittest.TestCase):
    def test_sucess_handler_to_path(self):
        result=cengine.to_path(ARequestHandlerStub.aRequestMethod)
        self.assertEquals(result,"/br/oneTest/ARequestHandlerStub/aRequestMethod")
        result=cengine.to_path(ARequestHandlerStub.aRequestMethod,"param1")
        self.assertEquals(result,"/br/oneTest/ARequestHandlerStub/aRequestMethod/param1")
        result=cengine.to_path(ARequestHandlerStub.aRequestMethod,"param1","param2")
        self.assertEquals(result,"/br/oneTest/ARequestHandlerStub/aRequestMethod/param1/param2")
        reqHandler=ARequestHandlerStub()
        result=cengine.to_path(reqHandler.aRequestMethod)
        self.assertEquals(result,"/br/oneTest/ARequestHandlerStub/aRequestMethod")
        result=cengine.to_path(reqHandler.aRequestMethod,"param1")
        self.assertEquals(result,"/br/oneTest/ARequestHandlerStub/aRequestMethod/param1")
        result=cengine.to_path(ARequestHandlerStub.anotherRequestMethod)
        self.assertEquals(result,"/br/oneTest/ARequestHandlerStub/anotherRequestMethod")
        reqHandler=ARequestHandlerStub()
        result=cengine.to_path(reqHandler.anotherRequestMethod)
        self.assertEquals(result,"/br/oneTest/ARequestHandlerStub/anotherRequestMethod")
        result=cengine.to_path(ARequestHandlerStub)
        self.assertEquals(result,"/br/oneTest/ARequestHandlerStub")
        result=cengine.to_path(ARequestHandlerStub())
        self.assertEquals(result,"/br/oneTest/ARequestHandlerStub")
        result=cengine.to_path(ARequestHandlerStub,"param1")
        self.assertEquals(result,"/br/oneTest/ARequestHandlerStub/param1")
        result=cengine.to_path(oneTest)
        self.assertEquals(result,"/br/oneTest")
        result=cengine.to_path(oneTest,"param1")
        self.assertEquals(result,"/br/oneTest/param1")
        result=cengine.to_path(handler)
        self.assertEquals(result,"/br")
        result=cengine.to_path(br)
        self.assertEquals(result,"/br")
        
        result=cengine.to_path(home)
        self.assertEquals(result,"/")
        
        result=cengine.to_path(home.index)
        self.assertEquals(result,"/")
        
        result=cengine.to_path(ex_handler)
        self.assertEquals(result,"/ex")
        
        result=cengine.to_path(ex_handler.home)
        self.assertEquals(result,"/ex")
        
        result=cengine.to_path(ex_handler.home.index)
        self.assertEquals(result,"/ex")
        
        result=cengine.to_path(ex_handler.not_home)
        self.assertEquals(result,"/ex/not_home")
        
        result=cengine.to_path(ex_handler.not_home.index)
        self.assertEquals(result,"/ex/not_home")
        
        
        
if __name__=="__main__":
    unittest.main()
    
    
    
    
    
    
    