# -*- coding: utf-8 -*-
from unittest.case import TestCase
import web_test
from web_test import home, first_handler, pack
from web_test.pack import home as pack_home, pack_handler
from tekton import router
from tekton.router import PathNotFound

router.package_base = 'web_test'


class ToPathTests(TestCase):
    def test_querystring(self):
        query_string = {'foo': 'bar'}
        self.assertEqual("/pack?foo=bar", router.to_path(pack, **query_string))
        self.assertEqual("/pack?foo=bar", router.to_path('/pack', **query_string))
        query_string = {'foo': 'bar', 'param': 1}
        self.assertEqual("/pack?foo=bar&param=1", router.to_path(pack, **query_string))
        self.assertEqual("/pack?foo=bar&param=1", router.to_path('/pack', **query_string))
        query_string = {'foo': 'çáê', 'param': 1}
        self.assertEqual("/pack?foo=%C3%A7%C3%A1%C3%AA&param=1", router.to_path('/pack', **query_string))

    def test_package(self):
        self.assertEqual("/", router.to_path(web_test))
        self.assertEqual("/pack", router.to_path(pack))


    def test_module(self):
        self.assertEqual("/first_handler", router.to_path(first_handler))
        self.assertEqual("/pack/pack_handler", router.to_path(pack_handler))


    def test_function(self):
        self.assertEqual("/first_handler/fcn_resp_handler", router.to_path(first_handler.fcn_resp_handler))
        self.assertEqual("/pack/pack_handler/with_kwargs", router.to_path(pack_handler.with_kwargs))

    def test_function_with_params(self):
        self.assertEqual("/first_handler/fcn_resp_handler/1", router.to_path(first_handler.fcn_resp_handler, "1"))
        self.assertEqual("/pack/pack_handler/with_kwargs/1/2/3", router.to_path(pack_handler.with_kwargs, 1, 2, 3))

    def test_home_index(self):
        self.assertEqual("/first_handler/1", router.to_path(first_handler.index, "1"))
        self.assertEqual("/pack/1/2/3", router.to_path(pack_home.index, 1, 2, 3))
        self.assertEqual("/1/2/3", router.to_path(home.index, 1, 2, 3))
        self.assertEqual("/", router.to_path(home.index))


REQUEST = "request"
RESPONSE = "response"
HANDLER = "handler"
CONVENTION_PARAMS = {"request": REQUEST, "response": RESPONSE, "handler": HANDLER}


class ToHandlerTests(TestCase):
    def assert_error_msg(self, path, msg):
        try:
            router.to_handler(path)
        except PathNotFound, e:
            self.assertTrue(e.message.find(msg) != -1, 'error msg should contain ' + msg)
            return

        self.fail('should raise PathNotFound')

    def test_import_error_msg(self):
        self.assert_error_msg('/import_error', 'ImportError: No module named not_existing_module')

    def test_syntax_error_msg(self):
        self.assert_error_msg('/syntax_error', "NameError: name 'foo' is not defined")

    def test_cycle_error_msg(self):
        self.assert_error_msg("/cycle_error", 'ImportError: cannot import name cycle_error')


    def test_security(self):
        #try to access listdir from os that is imported inside the first_handler script
        self.assertRaises(PathNotFound, router.to_handler, "/first_handler/listdir/a")

    def test_root(self):
        fcn, params = router.to_handler("/", CONVENTION_PARAMS)
        self.assertEqual(home.index, fcn)

        fcn, params = router.to_handler("/pack", CONVENTION_PARAMS)
        self.assertEqual(pack_home.index, fcn)


    def test_url_not_found(self):
        self.assertRaises(PathNotFound, router.to_handler, "/somehandler/function")


    def test_complete_path(self):
        fcn, params = router.to_handler("/pack/pack_handler/complete_path")
        self.assertEqual(pack_handler.complete_path, fcn)


    def test_complete_path_with_params(self):
        fcn, params = router.to_handler("/pack/pack_handler/with_params/1/%C3%A7ao%40%26%20")
        self.assertEqual(pack_handler.with_params, fcn)
        self.assertListEqual(["1", "çao@& "], params)

        fcn, params = router.to_handler("/pack/pack_handler/with_params/1", param2=2)
        self.assertEqual(pack_handler.with_params, fcn)
        self.assertListEqual(["1"], params)

    def test_complete_path_with_defaults(self):
        fcn, params = router.to_handler("/pack/pack_handler/with_defaults")
        self.assertEqual(pack_handler.with_defaults, fcn)
        self.assertListEqual([], params)

        fcn, params = router.to_handler("/pack/pack_handler/with_defaults/1")
        self.assertEqual(pack_handler.with_defaults, fcn)
        self.assertListEqual(["1"], params)

        fcn, params = router.to_handler("/pack/pack_handler/with_defaults/1/2")
        self.assertEqual(pack_handler.with_defaults, fcn)
        self.assertListEqual(["1", "2"], params)

        fcn, params = router.to_handler("/pack/pack_handler/with_defaults", param1="1", param2="2")
        self.assertEqual(pack_handler.with_defaults, fcn)
        self.assertListEqual([], params)

        fcn, params = router.to_handler("/pack/pack_handler/with_defaults/1", param2="2")
        self.assertEqual(pack_handler.with_defaults, fcn)
        self.assertListEqual(["1"], params)


    def test_complete_path_with_vargs(self):
        fcn, params = router.to_handler("/pack/pack_handler/with_vargs/1")
        self.assertEqual(pack_handler.with_vargs, fcn)
        self.assertListEqual(["1"], params)

        fcn, params = router.to_handler("/pack/pack_handler/with_vargs/1/2")
        self.assertEqual(pack_handler.with_vargs, fcn)
        self.assertListEqual(["1", "2"], params)

        fcn, params = router.to_handler("/pack/pack_handler/with_vargs/1/2/3")
        self.assertEqual(pack_handler.with_vargs, fcn)
        self.assertListEqual(["1", "2", "3"], params)

    def test_complete_path_with_varargs_and_kwargs(self):
        fcn, params = router.to_handler("/pack/pack_handler/with_kwargs/1", blah=2)
        self.assertEqual(pack_handler.with_kwargs, fcn)
        self.assertListEqual(["1"], params)

        fcn, params = router.to_handler("/pack/pack_handler/with_kwargs/1/2")
        self.assertEqual(pack_handler.with_kwargs, fcn)
        self.assertListEqual(["1", "2"], params)

        fcn, params = router.to_handler("/pack/pack_handler/with_kwargs/1/2/3")
        self.assertEqual(pack_handler.with_kwargs, fcn)
        self.assertListEqual(["1", "2", "3"], params)

    def test_req_resp_handler_convention(self):
        fcn, params = router.to_handler("/first_handler/fcn_req_resp_handler/1", CONVENTION_PARAMS)
        self.assertEqual(first_handler.fcn_req_resp_handler, fcn)
        self.assertListEqual([REQUEST, RESPONSE, HANDLER, "1"], params)

    def test_req_resp_convention(self):
        fcn, params = router.to_handler("/first_handler/fcn_req_resp/1", CONVENTION_PARAMS)
        self.assertEqual(first_handler.fcn_req_resp, fcn)
        self.assertListEqual([REQUEST, RESPONSE, "1"], params)

    def test_req_convention(self):
        fcn, params = router.to_handler("/first_handler/fcn_request/1", CONVENTION_PARAMS)
        self.assertEqual(first_handler.fcn_request, fcn)
        self.assertListEqual([REQUEST, "1"], params)

    def test_response_convention(self):
        fcn, params = router.to_handler("/first_handler/fcn_response/1", CONVENTION_PARAMS)
        self.assertEqual(first_handler.fcn_response, fcn)
        self.assertListEqual([RESPONSE, "1"], params)

    def test_handler_convention(self):
        fcn, params = router.to_handler("/first_handler/fcn_handler/1", CONVENTION_PARAMS)
        self.assertEqual(first_handler.fcn_handler, fcn)
        self.assertListEqual([HANDLER, "1"], params)


    def test_req_handler_convention(self):
        fcn, params = router.to_handler("/first_handler/fcn_req_handler/1", CONVENTION_PARAMS)
        self.assertEqual(first_handler.fcn_req_handler, fcn)
        self.assertListEqual([REQUEST, HANDLER, "1"], params)

    def test_resp_handler_convention(self):
        fcn, params = router.to_handler("/first_handler/fcn_resp_handler/1", CONVENTION_PARAMS)
        self.assertEqual(first_handler.fcn_resp_handler, fcn)
        self.assertListEqual([RESPONSE, HANDLER, "1"], params)

    def test_req_resp_handler_vargs_kwargs_convention(self):
        fcn, params = router.to_handler("/first_handler/fcn_req_resp_handler_default_vargs_kwargs/1", CONVENTION_PARAMS)
        self.assertEqual(first_handler.fcn_req_resp_handler_default_vargs_kwargs, fcn)
        self.assertListEqual([REQUEST, RESPONSE, HANDLER, "1"], params)

        fcn, params = router.to_handler("/first_handler/fcn_req_resp_handler_default_vargs_kwargs/1/2/3",
                                        CONVENTION_PARAMS)
        self.assertEqual(first_handler.fcn_req_resp_handler_default_vargs_kwargs, fcn)
        self.assertListEqual([REQUEST, RESPONSE, HANDLER, "1", "2", "3"], params)

        fcn, params = router.to_handler("/first_handler/fcn_req_resp_handler_default_vargs_kwargs/1/2/3",
                                        CONVENTION_PARAMS, param1="blah", param2="foo")
        self.assertEqual(first_handler.fcn_req_resp_handler_default_vargs_kwargs, fcn)
        self.assertListEqual([REQUEST, RESPONSE, HANDLER, "1", "2", "3"], params)



