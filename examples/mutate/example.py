import bitey
import mutate
import ctypes

x = ctypes.c_int(2)
mutate.mutate_int(x)
print x.value
