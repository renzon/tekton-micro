# -*- coding: utf-8 -*-
from unittest.case import TestCase
from plugins import web
from plugins.web import home,pack, somehandler
from plugins.web.pack import home as pack_home, anotherhandler, deep
from plugins.web.pack.deep import home as deep_home, deephandler, deeper
from plugins.web.pack.deep.deeper import home as deeper_home, deeperhandler

from zen import router
from zen.router import PathNotFound

class ToPathTests(TestCase):
    def test_package(self):
        self.assertEqual("/",router.to_path(web))
        self.assertEqual("/pack",router.to_path(pack))
        self.assertEqual("/pack/deep",router.to_path(deep))
        self.assertEqual("/pack/deep/deeper",router.to_path(deeper))

    def test_module(self):
        self.assertEqual("/somehandler",router.to_path(somehandler))
        self.assertEqual("/pack/anotherhandler",router.to_path(anotherhandler))
        self.assertEqual("/pack/deep/deephandler",router.to_path(deephandler))
        self.assertEqual("/pack/deep/deeper/deeperhandler",router.to_path(deeperhandler))

    def test_clazz(self):
        self.assertEqual("/somehandler/clazz",router.to_path(somehandler.clazz))
        self.assertEqual("/pack/anotherhandler/clazz",router.to_path(anotherhandler.clazz))
        self.assertEqual("/pack/deep/deephandler/clazz",router.to_path(deephandler.clazz))
        self.assertEqual("/pack/deep/deeper/deeperhandler/clazz",router.to_path(deeperhandler.clazz))

    def test_instance(self):
        self.assertEqual("/somehandler/clazz",router.to_path(somehandler.clazz()))
        self.assertEqual("/pack/anotherhandler/clazz",router.to_path(anotherhandler.clazz()))
        self.assertEqual("/pack/deep/deephandler/clazz",router.to_path(deephandler.clazz()))
        self.assertEqual("/pack/deep/deeper/deeperhandler/clazz",router.to_path(deeperhandler.clazz()))

    def test_class_method(self):
        self.assertEqual("/somehandler/clazz/method",router.to_path(somehandler.clazz.method))
        self.assertEqual("/pack/anotherhandler/clazz/method",router.to_path(anotherhandler.clazz.method))
        self.assertEqual("/pack/deep/deephandler/clazz/method",router.to_path(deephandler.clazz.method))
        self.assertEqual("/pack/deep/deeper/deeperhandler/clazz/method",router.to_path(deeperhandler.clazz.method))

    def test_instance_method(self):
        self.assertEqual("/somehandler/clazz/method",router.to_path(somehandler.clazz().method))
        self.assertEqual("/pack/anotherhandler/clazz/method",router.to_path(anotherhandler.clazz().method))
        self.assertEqual("/pack/deep/deephandler/clazz/method",router.to_path(deephandler.clazz().method))
        self.assertEqual("/pack/deep/deeper/deeperhandler/clazz/method",router.to_path(deeperhandler.clazz().method))

    def test_params(self):
        self.assertEqual("/somehandler/clazz/method/1",router.to_path(somehandler.clazz().method,1))
        self.assertEqual("/somehandler/clazz/method/1/2",router.to_path(somehandler.clazz().method,1,2))
        self.assertEqual("/somehandler/clazz/method/1/2/blah/%C3%A7ao%40%26%20/2",router.to_path(somehandler.clazz().method,1,2,"blah","çao@& /2"))
        self.assertEqual("/somehandler/clazz/method/1/2/blah",router.to_path(somehandler.clazz().method,1,2,"blah"))



class ToHandlerTests(TestCase):
    def test_root(self):
        handler,method,params=router.to_handler("/")
        self.assertEqual(home.home,handler.__class__)
        self.assertEqual("index",method.__name__)


#        Testing pack root
        handler,method,params=router.to_handler("/pack")
        self.assertEqual(pack_home.home,handler.__class__)
        self.assertEqual("index",method.__name__)
        

        #Testing deep root
        handler,method,params=router.to_handler("/pack/deep")
        self.assertEqual(deep_home.home,handler.__class__)
        self.assertEqual("index",method.__name__)

        #Testing deep root
        handler,method,params=router.to_handler("/pack/deep/deeper")
        self.assertEqual(deeper_home.home,handler.__class__)
        self.assertEqual("index",method.__name__)

    def test_url_not_found(self):
        self.assertRaises(PathNotFound,router.to_handler,"/somehandler/clazz/method")


    def test_complete_path(self):
        handler,method,params=router.to_handler("/pack/anotherhandler/clazz/method")
        self.assertEqual(anotherhandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)


        handler,method,params=router.to_handler("/pack/deep/deephandler/clazz/method")
        self.assertEqual(deephandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)

        handler,method,params=router.to_handler("/pack/deep/deeper/deeperhandler/clazz/method")
        self.assertEqual(deeperhandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)

    def test_complete_path_with_params(self):
        handler,method,params=router.to_handler("/somehandler/clazz/method/1/%C3%A7ao%40%26%20")
        self.assertEqual(somehandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1","çao@& "],params)

        handler,method,params=router.to_handler("/somehandler/clazz/method/1",param2=2)
        self.assertEqual(somehandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1"],params)

    def test_complete_path_with_defaults(self):
        handler,method,params=router.to_handler("/pack/anotherhandler/clazz/method")
        self.assertEqual(anotherhandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual([],params)

        handler,method,params=router.to_handler("/pack/anotherhandler/clazz/method/1")
        self.assertEqual(anotherhandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1"],params)

        handler,method,params=router.to_handler("/pack/anotherhandler/clazz/method/1/2")
        self.assertEqual(anotherhandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1","2"],params)

        handler,method,params=router.to_handler("/pack/anotherhandler/clazz/method",param1="1",param2="2")
        self.assertEqual(anotherhandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual([],params)

        handler,method,params=router.to_handler("/pack/anotherhandler/clazz/method/1",param2="2")
        self.assertEqual(anotherhandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1"],params)



    def test_complete_path_with_vargs(self):
        handler,method,params=router.to_handler("/pack/deep/deephandler/clazz/method/1")
        self.assertEqual(deephandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1"],params)

        handler,method,params=router.to_handler("/pack/deep/deephandler/clazz/method/1/2")
        self.assertEqual(deephandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1","2"],params)

        handler,method,params=router.to_handler("/pack/deep/deephandler/clazz/method/1/2/3")
        self.assertEqual(deephandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1","2","3"],params)

    def test_complete_path_with_varargs_and_kwargs(self):
        handler,method,params=router.to_handler("/pack/deep/deeper/deeperhandler/clazz/method/1",blah=2)
        self.assertEqual(deeperhandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1"],params)

        handler,method,params=router.to_handler("/pack/deep/deeper/deeperhandler/clazz/method/1/2")
        self.assertEqual(deeperhandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1","2"],params)

        handler,method,params=router.to_handler("/pack/deep/deeper/deeperhandler/clazz/method/1/2/3")
        self.assertEqual(deeperhandler.clazz,handler.__class__)
        self.assertEqual("method",method.__name__)
        self.assertListEqual(["1","2","3"],params)




    def test_index(self):
        handler,method,params=router.to_handler("/somehandler/clazz")
        self.assertEqual(somehandler.clazz,handler.__class__)
        self.assertEqual("index",method.__name__)


        handler,method,params=router.to_handler("/pack/anotherhandler/clazz")
        self.assertEqual(anotherhandler.clazz,handler.__class__)
        self.assertEqual("index",method.__name__)


        handler,method,params=router.to_handler("/pack/deep/deephandler/clazz")
        self.assertEqual(deephandler.clazz,handler.__class__)
        self.assertEqual("index",method.__name__)

        handler,method,params=router.to_handler("/pack/deep/deeper/deeperhandler/clazz")
        self.assertEqual(deeperhandler.clazz,handler.__class__)
        self.assertEqual("index",method.__name__)

    def test_home(self):
        handler,method,params=router.to_handler("/somehandler")
        self.assertEqual(somehandler.home,handler.__class__)
        self.assertEqual("index",method.__name__)


        handler,method,params=router.to_handler("/pack/anotherhandler")
        self.assertEqual(anotherhandler.home,handler.__class__)
        self.assertEqual("index",method.__name__)


        handler,method,params=router.to_handler("/pack/deep/deephandler")
        self.assertEqual(deephandler.home,handler.__class__)
        self.assertEqual("index",method.__name__)

        handler,method,params=router.to_handler("/pack/deep/deeper/deeperhandler")
        self.assertEqual(deeperhandler.home,handler.__class__)
        self.assertEqual("index",method.__name__)


