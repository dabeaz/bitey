# Auto-install the loader on import
from . import loader, bind
loader.install()

# Utility function to load shared libraries (if needed by the module)
_library_cache = {}
def load_library(name):
    import ctypes
    if name in _library_cache:
        return _library_cache[name]
    _library_cache[name] = ctypes.CDLL(name, ctypes.RTLD_GLOBAL)
    return _library_cache[name]

# Bring some common binding functions up one lever
from bind import wrap_llvm_bitcode, wrap_llvm_module, wrap_llvm_function


