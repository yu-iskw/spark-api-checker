import sys
import pkgutil
import inspect
import json
import re
import types

def get_method_info(klass, method_name):
    dict = {}
    dict["name"] = method_name
    r = re.compile("<type '(.*)'>")
    if r.match(str(type(klass.__dict__[method_name]))):
        m = r.search(str(type(method)))
        dict["type"] = m.group(1)
    dict["argspec"] = []
    return dict
    #argspec, _, _, _ = inspect.getargspec(method)
    #dict["name"] = method_name
    #dict["argspec"] = argspec
    #return dict

def is_instance_method(klass, method_name):
    if str(type(klass.__dict__[method_name])) == "<type 'instancemethod'>" or \
            str(type(klass.__dict__[method_name])) == "<type 'function'>" or \
            str(type(klass.__dict__[method_name])) == "<type 'property'>":
        return True
    else:
        return False

def is_class_method(klass, method_name):
    if str(type(klass.__dict__[method_name])) == "<type 'staticmethod'>" or \
            str(type(klass.__dict__[method_name])) == "<type 'classmethod'>" or \
            str(type(klass.__dict__[method_name])) == "<type 'function'>":
        return True
    else:
        return False

module_name = sys.argv[1]
__import__(module_name)

## Gets the reference of the target module
module = sys.modules[module_name]

## for-loop of the classes under the target module
definitions = {}
for c, _ in inspect.getmembers(module, predicate=inspect.isclass):
    definitions[c] = {}
    klass = getattr(module, c)
    ## name
    definitions[c]["name"] = c
    ## class methods
    definitions[c]["class_methods"] = {}
    definitions[c]["instance_methods"] = {}
    methods = inspect.getmembers(klass, predicate=inspect.ismethod)
    functions = inspect.getmembers(klass, predicate=inspect.isfunction)
    methods = filter(lambda x: not re.match("^__.*__$", str(x)), klass.__dict__.keys())
    for method_name in methods:
        method = getattr(klass, method_name)
        if is_instance_method(klass, method_name):
            method_info = get_method_info(klass, method_name)
            definitions[c]["instance_methods"][method_name] = method_info
        elif is_class_method(klass, method_name):
            method_info = get_method_info(klass, method_name)
            definitions[c]["class_methods"][method_name] = method_info


print(json.dumps(definitions))
