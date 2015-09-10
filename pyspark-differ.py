import sys
import json
import re
import os
import copy


def load_json_as_dict(path):
    with open(path) as data_file:
        data = json.load(data_file)
    return data


def sort_version(versions, desc = False):
    not_master = filter(lambda x: x != "master", versions)
    if "master" in versions:
        list = sorted(not_master) + ["master"]
    else:
        list =  sorted(not_master)
    if desc == True:
        list = [x for x in reversed(list)]
    return list


class Package():
    def __init__(self, name):
        self._name = name
        self._classes = []

    def expand(self):
        dict = {}
        dict["name"] = self._name
        dict["classes"] = []
        for c in self._classes:
            dict["classes"].append(c.expand())
        return dict

    def diff_class(self, old_json, new_json, version):
        diff_classes = [x for x in new_json.keys() if x not in old_json.keys()]
        klasses = []
        for c in diff_classes:
            klass = Klass(c, version)
            klasses.append(klass)
            self._classes.append(klass)
        return klasses


class Klass():
    singletons = {}

    @classmethod
    def generate(cls, dict, version):
        singleton_key = dict["name"] + ":::" +  version
        if not version in Klass.singletons:
            klass = Klass(dict["name"], version)
            class_methods = dict["class_methods"]
            klass._class_methods = [Method.generate(class_methods[m], version) for m in class_methods]
            instance_methods = dict["instance_methods"]
            klass._instance_methods = [Method.generate(instance_methods[m], version) for m in instance_methods]
            Klass.singletons[singleton_key] = klass
        return Klass.singletons[singleton_key]

    def __init__(self, name, version):
        self._name = name
        self._version = version
        self._class_methods = []
        self._instance_methods = []

    def expand(self):
        dict = {}
        dict["name"] = self._name
        dict["version"] = self._version
        dict["class_methods"] = [m.expand() for m in self._class_methods]
        dict["instance_methods"] = [m.expand() for m in self._instance_methods]
        return dict

    def merge(self, other):
        if self._name != other._name:
            raise Exception(self_name + "is different from " + other._name)
        versions = sort_version([self._version, other._version])
        merged = Klass(self._name, versions[0])
        # class methods
        for m in self._class_methods:
            if other.has_class_method(m._name):
                x = m.merge(other.get_class_method(m._name))
            else:
                x = m
            merged._class_methods.append(x)
        # instance methods
        for m in self._instance_methods:
            if other.has_instance_method(m._name):
                x = m.merge(other.get_instance_method(m._name))
            else:
                x = m
            merged._instance_methods.append(x)
        return merged

    def has_class_method(self, name):
        return name in [m._name for m in self._class_methods]

    def has_instance_method(self, name):
        return name in [m._name for m in self._instance_methods]

    def get_class_method(self, name):
        for m in self._class_methods:
            if m._name == name:
                return m

    def get_instance_method(self, name):
        for m in self._instance_methods:
            if m._name == name:
                return m


class Method():
    singletons = {}

    @classmethod
    def generate(cls, dict, version):
        singleton_key = dict["name"] + version
        if not version in Method.singletons:
            Method.singletons[singleton_key] = Method(dict["name"], version, dict["type"])
        return Method.singletons[singleton_key]

    def __init__(self, name, version, object_type):
        self._name = name
        self._version = version
        self._type = object_type

    def expand(self):
        dict = {}
        dict["name"] = self._name
        dict["version"] = self._version
        dict["type"] = self._type
        return dict

    def merge(self, other):
        if self._name != other._name:
            raise Exception(self_name + "is different from " + other._name)
        versions = sort_version([self._version, other._version])
        merged = Method(self._name, versions[0], self._type)
        return merged


packages = []
klasses = {}
BASE_DIR = "pyspark-apis-checker-result"
package_names = os.listdir(BASE_DIR)
for p in package_names:
    package = Package(p)
    packages.append(package)

    subdir = os.path.join(BASE_DIR, p)
    files = os.listdir(subdir)
    files = [files[i] for i in range(1, len(files) - 1)] + [files[0]]
    versions = [f.replace(p + ".", "").replace(".json", "") for f in files]
    # Inspect diff
    for i in range(0, len(versions)):
        print(os.path.join(BASE_DIR, p, files[i]))
        defs = load_json_as_dict(os.path.join(BASE_DIR, p, files[i]))
        for k in defs.keys():
            klass = Klass.generate(defs[k], versions[i])

    for key in Klass.singletons.keys():
        klass_name, version = key.split(":::")
        if klass_name in klasses and not version in klasses[klass_name] :
            klasses[klass_name].append(version)
        else:
            klasses[klass_name] = [version]

for k in klasses.keys():
    versions = klasses[k]
    if "master" in versions:
        rev = sort_version(versions, desc = True)
        master_key = k + ":::" + rev[0]
        merged = Klass.singletons[master_key]
        for i in range(1, len(rev)):
            other_key = k + ":::" + rev[i]
            other = Klass.singletons[other_key]
            print(other_key)
            print(other.expand())
            merged = merged.merge(other)

        # Write JSON to a file
        path = os.path.join("pyspark-differ", k + ".json")
        with open(path, "w") as f:
            f.write(json.dumps(merged.expand()))
        print(json.dumps(merged.expand()))
