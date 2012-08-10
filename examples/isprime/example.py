import bitey
from isprime import isprime as isprime1

import ctypes
ex = ctypes.cdll.LoadLibrary("./isprime.so")
isprime2 = ex.isprime
isprime2.argtypes = (ctypes.c_int,)
isprime2.restype = ctypes.c_int

from timeit import timeit

print("Bitey")
print(timeit("isprime1(1)", "from __main__ import isprime1"))
print("ctypes")
print(timeit("isprime2(1)", "from __main__ import isprime2"))

print("Bitey")
print(timeit("isprime1(10143937)", "from __main__ import isprime1"))
print("ctypes")
print(timeit("isprime2(10143937)", "from __main__ import isprime2"))

