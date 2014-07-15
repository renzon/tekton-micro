# -*- coding: utf-8 -*-
import importlib
import inspect
import traceback
import os
import urllib

__author__ = 'renzo'


class PathNotFound(Exception): pass


package_base = "routes"
home_base = "home"
index_base = "index"


def _to_abs_package(package_slices):
    if package_slices:
        return package_base + "." + ".".join(package_slices)
    return package_base


def _check_convention_params(args, convention_params):
    convention_list = []
    for a in args:
        if a in convention_params:
            convention_list.append(convention_params.get(a))
        else:
            break

    return convention_list


def _check_params(params, convention_params, spec, **kwargs):
    args = spec[0]
    all_params = _check_convention_params(args, convention_params) + params
    param_num = len(all_params)
    max_args = len(args) if args else 0
    defaults = spec[3]
    defaults_num = len(defaults) if defaults else 0
    min_args = max_args - defaults_num
    kwargs_num = len(kwargs)
    all_args_num = param_num + kwargs_num

    if min_args <= all_args_num <= max_args: return all_params

    varargs = spec[1]
    method_kwargs = spec[2]

    if varargs and method_kwargs: return all_params

    if varargs and not kwargs and param_num >= min_args:
        return all_params

    if method_kwargs and param_num >= (min_args - kwargs_num):
        return all_params


def _import_helper(base_dir, errors, package, module_name, fcn_name, params, convention_params, **kwargs):
    full_module = package + "." + module_name
    module_path = os.path.join(base_dir, *full_module.split('.'))
    is_file = os.path.isfile(module_path + '.py')
    if not is_file:
        return
    module = None
    try:
        module = importlib.import_module(full_module)
    except:
        tb = traceback.format_exc()
        errors.append(tb)
        return
    if hasattr(module, fcn_name):
        fcn = getattr(module, fcn_name)
        if fcn and inspect.isfunction(fcn):
            all_params = _check_params(params, convention_params, inspect.getargspec(fcn), **kwargs)
            if all_params is not None:
                return fcn, all_params


def _build_pack_and_slices(package, slices):
    slice_number = min(len(slices), 2)
    package = ".".join([package] + slices[:-slice_number])
    path_slices = slices[-slice_number:]
    return package, path_slices


def _search_full_path(base_dir, package, path_slices, defaults=[], params=[], convention_params={}, errors=[],
                      **kwargs):
    slices = path_slices + defaults
    if len(slices) < 2:
        return
    pack, slices = _build_pack_and_slices(package, slices)
    result = _import_helper(base_dir, errors, pack, *slices, params=params, convention_params=convention_params,
                            **kwargs)
    if result or not path_slices:
        return result

    params.insert(0, path_slices.pop())
    return _search_full_path(base_dir, package, path_slices, defaults, params, convention_params, errors, **kwargs)


def _maybe_import(path, base_dir, package, path_slices, convention_params, errors, **kwargs):
    result = _search_full_path(base_dir, package, path_slices[:], [], [], convention_params, errors, **kwargs)
    if result:
        return result

    result = _search_full_path(base_dir, package, path_slices[:], [index_base], [], convention_params, errors,
                               **kwargs)
    if result:
        return result

    result = _search_full_path(base_dir, package, path_slices[:], [home_base, index_base], [], convention_params,
                               errors,
                               **kwargs)
    if result:
        return result
    msg = 'No module found for path: %s' % path
    if errors:
        separator = '------- Module Search Traceback -------\n'
        msg = separator.join(errors) + '\n' + msg
    raise PathNotFound(msg)


def to_handler(path, convention_params={}, **kwargs):
    base_dir = os.path.dirname(importlib.import_module(package_base).__file__)
    base_dir = os.path.join(base_dir, '..')
    decoded_path = urllib.unquote(path)
    path_slices = [d for d in decoded_path.split("/") if d != ""]
    errors = []
    # Try importing package.handler.method
    return _maybe_import(path, base_dir, package_base, path_slices, convention_params, errors, **kwargs)


def _build_params(*params):
    if params:
        def f(p):
            if isinstance(p, basestring):
                return urllib.quote(p)
            return urllib.quote(str(p))

        params = [f(p) for p in params]

        return "/" + "/".join(params)
    return ""


def to_path(handler, *params, **query_params):
    '''
    given a handler (path as string, function, module or package) build its respective path
    all params are going to be quoted and joined to the path
    query_params dict will be used to build the query_string of the path

    Ex: handler = module.function, params =['a','b'], query_params={'arg'=1,'arg2'=2} will return
    /module/function/a/b?arg1=1&args2=2
    '''
    params = _build_params(*params)

    if query_params:
        query_string = urllib.urlencode(query_params)

    if isinstance(handler, basestring):
        path = handler + params
        if query_params:
            path += '?' + query_string
        return path
    elif inspect.ismodule(handler):
        name = handler.__name__
    else:
        name = handler.__module__ + "/" + handler.__name__

    name = name.replace(package_base, "", 1)

    def remove_from_end(path, suffix):
        return path[:-len(suffix) - 1] if path.endswith(suffix) else path

    home_index = '/'.join((home_base, index_base))
    name = remove_from_end(name, home_index)
    name = remove_from_end(name, index_base)

    if not name:
        return params or "/"
    path = name.replace(".", "/") + params
    if query_params:
        path += '?' + query_string
    return path


def _extract_full_module(klass):
    return klass.__module__ + "/" + klass.__name__
