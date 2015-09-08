import sys
import pkgutil
import inspect
import json
import re

module_name = sys.argv[1]
__import__(module_name)

## Gets the reference of the target module
module = sys.modules[module_name]

## for-loop of the classes under the target module
definitions = {}
for c, _ in inspect.getmembers(module, predicate=inspect.isclass):
    if c == "SparkContext":
        continue
    elif c == "Savable" or c == "Loader":
        continue
    elif c == "JavaModelWrapper" or c == "JavaSavable" or c == "JavaLoader":
        continue
    elif c == "Params":
        continue
    elif re.match("^Has.*", c):
        continue

    definitions[c] = {}
    klass = getattr(module, c)
    ## class methods
    definitions[c]["class_methods"] = {}
    methods = inspect.getmembers(klass, predicate=inspect.ismethod)
    for method_name, _ in methods:
        method = getattr(klass, method_name)
        argspec, _, _, _ = inspect.getargspec(method)
        definitions[c]["class_methods"][method_name] = argspec
    ## instance methods
    definitions[c]["instance_methods"] = {}
    methods = inspect.getmembers(klass, predicate=inspect.isfunction)
    for method_name, _ in methods:
        method = getattr(klass, method_name)
        argspec, _, _, _ = inspect.getargspec(method)
        definitions[c]["instance_methods"][method_name] = argspec

print(json.dumps(definitions))
