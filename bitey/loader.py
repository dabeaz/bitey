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
        elif magic[:2] == b'\x42\x43':
            return True
        else:
            return False
    else:
	return False

def build_module(fullname, bitcode, preload=None, postload=None):
    '''
    Creates a new module from bitcode supplied as a simple byte-string.
    '''
    name = fullname.split(".")[-1]
    mod = imp.new_module(name)
    if preload:
        exec(preload, mod.__dict__, mod.__dict__)
    bind.wrap_llvm_bitcode(bitcode, mod)
    if postload:
        exec(postload, mod.__dict__, mod.__dict__)
    return mod
    
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

        preload = None
        postload = None

        # Get the preload file (if any)
        if os.path.exists(self.preload):
            with open(self.preload) as f:
                preload = f.read()

        # Get the bit-code
        with open(self.source, 'rb') as f:
            bitcode = f.read()

        # Get the postload file (if any)
        if os.path.exists(self.postload):
            with open(self.postload) as f:
                postload = f.read()
                
        mod = build_module(fullname, bitcode, preload, postload)
        sys.modules[fullname] = mod
        mod.__loader__ = self
        mod.__file__ = self.source
        return mod

def install():
    if LLVMLoader not in sys.meta_path:
        sys.meta_path.append(LLVMLoader)

def remove():
    sys.meta_path.remove(LLVMLoader)
