all:
	clang -emit-llvm -c fib.c
	clang -emit-llvm -c fact.c
	llvm-ld fib.o fact.o -b sample.o
