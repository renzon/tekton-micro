# -*- coding: utf-8 -*-
import importlib
import inspect
import urllib

__author__ = 'renzo'

class PathNotFound(Exception): pass

package_base="plugins.web"
home_base="home"
index_base="index"

def _to_abs_package(package_slices):
    if package_slices:
        return package_base+"."+".".join(package_slices)
    return package_base


def _in_range(param_num,spec,**kwargs):
    args=spec[0]
    max_args=len(args)-1 if args else 0
    defaults=spec[3]
    defaults_num=len(defaults) if defaults else 0
    min_args=max_args-defaults_num
    kwargs_num=len(kwargs)
    all_args_num=param_num+kwargs_num

    if min_args<=all_args_num<=max_args: return True

    varargs=spec[1]
    method_kwargs=spec[2]

    if varargs and method_kwargs: return True

    if varargs and not kwargs and param_num>=min_args:
        return True

    if method_kwargs and param_num>=(min_args-kwargs_num):
        return True






def _import_helper(package,module_name,class_name, method_name,params,**kwargs):
    try:
        full_module=package+"."+module_name
        module = importlib.import_module(full_module)
        if hasattr(module, class_name):
            clazz = getattr(module, class_name)
            if inspect.isclass(clazz) and hasattr(clazz, method_name):
                instance = clazz()
                method=getattr(instance, method_name)
                if _in_range(len(params),inspect.getargspec(method),**kwargs):
                    return instance,method,params
    except ImportError: pass


def _build_pack_and_slices(package, slices):
    slice_number=min(len(slices),3)
    package=".".join([package]+slices[:-slice_number])
    path_slices=slices[-slice_number:]
    return package,path_slices


def _search_full_path(package, path_slices,defaults=[],params=[],**kwargs):
    slices=path_slices+defaults
    if len(slices)<3: return
    pack,slices=_build_pack_and_slices(package,slices)
    result=_import_helper(pack,*slices,params=params,**kwargs)
    if result or not path_slices: return result

    params.insert(0,path_slices.pop())
    return _search_full_path(package,path_slices,defaults,params,**kwargs)


def _maybe_import(package, path_slices,**kwargs):
    result=_search_full_path(package,path_slices[:],[],[],**kwargs)
    if result: return result

    result=_search_full_path(package,path_slices[:],[index_base],[],**kwargs)
    if result: return result

    result=_search_full_path(package,path_slices[:],[home_base,index_base],[],**kwargs)
    if result: return result

    result=_search_full_path(package,path_slices[:],[home_base,home_base,index_base],[],**kwargs)
    if result: return result

    raise PathNotFound()






def to_handler(path,**kwargs):
    decoded_path = urllib.unquote(path)
    path_slices = filter(lambda d: d != "", decoded_path.split("/"))
#    Try importing package.handler.method
    return _maybe_import(package_base,path_slices,**kwargs)


def _build_params(*params):
    if params:
        def f(p):
            if isinstance(p, basestring):
                return urllib.quote(p)
            return urllib.quote(str(p))
        params=[f(p) for p in params]

        return "/"+"/".join(params)
    return ""


def to_path(handler,*params):
    params=_build_params(*params)

    if inspect.ismodule(handler):
        name=handler.__name__
    elif inspect.isclass(handler):
        name=_extract_full_module(handler)
    elif inspect.ismethod(handler):
        name=_extract_full_module(handler.im_class)+"/"+handler.__name__
    else:
        name=_extract_full_module(handler.__class__)
    name=name.replace(package_base,"",1)
    if not name: return params or "/"
    return name.replace(".","/")+params

def _extract_full_module(klass):
    return klass.__module__ + "/" + klass.__name__
