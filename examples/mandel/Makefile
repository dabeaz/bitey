all::
	clang -O3 -emit-llvm -c _mandel.c

# Make a shared library for the ctypes version
shared::
	gcc -O3 -bundle -undefined dynamic_lookup _mandel.c -o _mandel.so
	# Linux
	# gcc -shared fib.c -o libfib.so
