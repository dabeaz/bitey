# loader.py
"""
Import hook loader for LLVM bitcode files.

Use the install() method to install the loader into sys.meta_path.  Use
the remove() method to uninstall it.
"""

import sys
import os.path
import imp
from . import bind

def _check_magic(filename):
    if os.path.exists(filename):
	magic = open(filename,"rb").read(4)
        if magic == b'\xde\xc0\x17\x0b':
            return True
        elif magic == b'\x42\x43':
            return True
        else:
            return False
    else:
	return False
    
class LLVMLoader(object):
    """
    Load LLVM compiled bitcode and autogenerate a ctypes binding
    """
    def __init__(self, pkg, name, source, preload, postload):
	self.package = pkg
	self.name = name
	self.fullname = '.'.join((pkg,name))
	self.source = source
        self.preload = preload
        self.postload = postload

    @classmethod
    def find_module(cls, fullname, paths = None):
	if paths is None:
	    paths = sys.path
                        
        names = fullname.split('.')
        modname = names[-1]
        for f in paths:
            path = os.path.join(os.path.realpath(f), modname)
            source = path + '.o'
	    if _check_magic(source):
                preload = path + ".pre.py"
                postload = path + ".post.py"
                return cls('.'.join(names[:-1]), modname, source, preload, postload)

    def get_code(self, module):
        pass

    def get_data(self, module):
        pass

    def get_filename(self, name):
        return self.source

    def get_source(self, name):
        with open(self.source, 'rb') as f:
             return f.read()

    def is_package(self, *args, **kw):
        return False

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        mod = sys.modules[fullname] = imp.new_module(self.name)
        # Look for preload
        if os.path.exists(self.preload):
            with open(self.preload) as f:
                preload = f.read()
            exec(preload, mod.__dict__, mod.__dict__)
        # Build the bitcode
        with open(self.source, 'rb') as f:
            bitcode = f.read()
        bind.build_wrappers(bitcode, mod)
        mod.__loader__ = self
        mod.__file__ = self.source

        if os.path.exists(self.postload):
            with open(self.postload) as f:
                postload = f.read()
            exec(postload, mod.__dict__, mod.__dict__)
        return mod

def install():
    if LLVMLoader not in sys.meta_path:
        sys.meta_path.append(LLVMLoader)

def remove():
    sys.meta_path.remove(LLVMLoader)
