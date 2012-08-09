all: sharedlib llvm

sharedlib::
	# Make a traditional shared library using the C compiler
	# OS-X
	gcc -bundle -undefined dynamic_lookup fib.c -o libfib.so
	# Linux
	# gcc -shared fib.c -o libfib.so

llvm::
	clang -emit-llvm -c sample.c

