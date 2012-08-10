all: llvm shared

llvm::
	clang -O3 -emit-llvm -c isprime.c

shared::
	gcc -O3 -bundle -undefined dynamic_lookup isprime.c -o isprime.so
	# Linux
	# gcc -O3 -shared isprime.c -o isprime.so
