# -*- coding: utf-8 -*-
from unittest.case import TestCase
from web import home,first_handler
from web.pack import home as pack_home,pack_handler


from zen import router
from zen.router import PathNotFound

#class ToPathTests(TestCase):
#    def test_package(self):
#        self.assertEqual("/",router.to_path(web))
#        self.assertEqual("/pack",router.to_path(pack))
#        self.assertEqual("/pack/deep",router.to_path(deep))
#        self.assertEqual("/pack/deep/deeper",router.to_path(deeper))
#
#    def test_module(self):
#        self.assertEqual("/somehandler",router.to_path(somehandler))
#        self.assertEqual("/pack/anotherhandler",router.to_path(anotherhandler))
#        self.assertEqual("/pack/deep/deephandler",router.to_path(deephandler))
#        self.assertEqual("/pack/deep/deeper/deeperhandler",router.to_path(deeperhandler))
#
#    def test_clazz(self):
#        self.assertEqual("/somehandler/clazz",router.to_path(somehandler.clazz))
#        self.assertEqual("/pack/anotherhandler/clazz",router.to_path(anotherhandler.clazz))
#        self.assertEqual("/pack/deep/deephandler/clazz",router.to_path(deephandler.clazz))
#        self.assertEqual("/pack/deep/deeper/deeperhandler/clazz",router.to_path(deeperhandler.clazz))
#
#    def test_instance(self):
#        self.assertEqual("/somehandler/clazz",router.to_path(somehandler.clazz()))
#        self.assertEqual("/pack/anotherhandler/clazz",router.to_path(anotherhandler.clazz()))
#        self.assertEqual("/pack/deep/deephandler/clazz",router.to_path(deephandler.clazz()))
#        self.assertEqual("/pack/deep/deeper/deeperhandler/clazz",router.to_path(deeperhandler.clazz()))
#
#    def test_class_method(self):
#        self.assertEqual("/somehandler/clazz/method",router.to_path(somehandler.clazz.method))
#        self.assertEqual("/pack/anotherhandler/clazz/method",router.to_path(anotherhandler.clazz.method))
#        self.assertEqual("/pack/deep/deephandler/clazz/method",router.to_path(deephandler.clazz.method))
#        self.assertEqual("/pack/deep/deeper/deeperhandler/clazz/method",router.to_path(deeperhandler.clazz.method))
#
#    def test_instance_method(self):
#        self.assertEqual("/somehandler/clazz/method",router.to_path(somehandler.clazz().method))
#        self.assertEqual("/pack/anotherhandler/clazz/method",router.to_path(anotherhandler.clazz().method))
#        self.assertEqual("/pack/deep/deephandler/clazz/method",router.to_path(deephandler.clazz().method))
#        self.assertEqual("/pack/deep/deeper/deeperhandler/clazz/method",router.to_path(deeperhandler.clazz().method))
#
#    def test_params(self):
#        self.assertEqual("/somehandler/clazz/method/1",router.to_path(somehandler.clazz().method,1))
#        self.assertEqual("/somehandler/clazz/method/1/2",router.to_path(somehandler.clazz().method,1,2))
#        self.assertEqual("/somehandler/clazz/method/1/2/blah/%C3%A7ao%40%26%20/2",router.to_path(somehandler.clazz().method,1,2,"blah","çao@& /2"))
#        self.assertEqual("/somehandler/clazz/method/1/2/blah",router.to_path(somehandler.clazz().method,1,2,"blah"))

convention_params={"request":"request","response":"response","handler":"handler"}

class ToHandlerTests(TestCase):
    def test_root(self):

        fcn,params=router.to_handler("/",convention_params)
        self.assertEqual(home.index,fcn)

        fcn,params=router.to_handler("/pack",convention_params)
        self.assertEqual(pack_home.index,fcn)



    def test_url_not_found(self):
        self.assertRaises(PathNotFound,router.to_handler,"/somehandler/function")


    def test_complete_path(self):
        fcn,params=router.to_handler("/pack/pack_handler/complete_path")
        self.assertEqual(pack_handler.complete_path,fcn)


    def test_complete_path_with_params(self):
        fcn,params=router.to_handler("/pack/pack_handler/with_params/1/%C3%A7ao%40%26%20")
        self.assertEqual(pack_handler.with_params,fcn)
        self.assertListEqual(["1","çao@& "],params)

        fcn,params=router.to_handler("/pack/pack_handler/with_params/1",param2=2)
        self.assertEqual(pack_handler.with_params,fcn)
        self.assertListEqual(["1"],params)

    def test_complete_path_with_defaults(self):
        fcn,params=router.to_handler("/pack/pack_handler/with_defaults")
        self.assertEqual(pack_handler.with_defaults,fcn)
        self.assertListEqual([],params)

        fcn,params=router.to_handler("/pack/pack_handler/with_defaults/1")
        self.assertEqual(pack_handler.with_defaults,fcn)
        self.assertListEqual(["1"],params)

        fcn,params=router.to_handler("/pack/pack_handler/with_defaults/1/2")
        self.assertEqual(pack_handler.with_defaults,fcn)
        self.assertListEqual(["1","2"],params)

        fcn,params=router.to_handler("/pack/pack_handler/with_defaults",param1="1",param2="2")
        self.assertEqual(pack_handler.with_defaults,fcn)
        self.assertListEqual([],params)

        fcn,params=router.to_handler("/pack/pack_handler/with_defaults/1",param2="2")
        self.assertEqual(pack_handler.with_defaults,fcn)
        self.assertListEqual(["1"],params)
#
#
#
#    def test_complete_path_with_vargs(self):
#        fcn,params=router.to_handler("/pack/deep/deephandler/clazz/method/1")
#        self.assertEqual(deephandler.clazz,handler.__class__)
#        self.assertEqual("method",method.__name__)
#        self.assertListEqual(["1"],params)
#
#        fcn,params=router.to_handler("/pack/deep/deephandler/clazz/method/1/2")
#        self.assertEqual(deephandler.clazz,handler.__class__)
#        self.assertEqual("method",method.__name__)
#        self.assertListEqual(["1","2"],params)
#
#        fcn,params=router.to_handler("/pack/deep/deephandler/clazz/method/1/2/3")
#        self.assertEqual(deephandler.clazz,handler.__class__)
#        self.assertEqual("method",method.__name__)
#        self.assertListEqual(["1","2","3"],params)
#
#    def test_complete_path_with_varargs_and_kwargs(self):
#        fcn,params=router.to_handler("/pack/deep/deeper/deeperhandler/clazz/method/1",blah=2)
#        self.assertEqual(deeperhandler.clazz,handler.__class__)
#        self.assertEqual("method",method.__name__)
#        self.assertListEqual(["1"],params)
#
#        fcn,params=router.to_handler("/pack/deep/deeper/deeperhandler/clazz/method/1/2")
#        self.assertEqual(deeperhandler.clazz,handler.__class__)
#        self.assertEqual("method",method.__name__)
#        self.assertListEqual(["1","2"],params)
#
#        fcn,params=router.to_handler("/pack/deep/deeper/deeperhandler/clazz/method/1/2/3")
#        self.assertEqual(deeperhandler.clazz,handler.__class__)
#        self.assertEqual("method",method.__name__)
#        self.assertListEqual(["1","2","3"],params)
#
#
#
#
