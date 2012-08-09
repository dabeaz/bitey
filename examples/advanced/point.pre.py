# point.pre.py
#
# Code that executes in the fib module prior to LLVM binding

# Declare the structure field names for the Point structure
class Point:
    _fields_ = ['x','y']

