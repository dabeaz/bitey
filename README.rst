Bitey - Bitcode Import Tool
===========================
Import LLVM bitcode directly into Python and use it as an extension module.

Warning
=======
THIS IS PROOF-OF-CONCEPT SOFTWARE THAT DESPITE ITS CUTE NAME, MIGHT
ACTUALLY BITE YOUR ENTIRE LEG OFF.  USE AT YOUR OWN RISK!

Requirements
============
You'll need to have a pretty complete LLVM development environment
installed on your machine.  Bitey has been developed using
LLVM/Clang-3.1.  You might need to install it yourself.  

In addition, you need to install the ``llvm-py`` extension.  Get it at
at http://www.llvmpy.org. 

Bitey is unlikely to work with any older version of LLVM or the llvm-py
extension--especially preinstalled versions distributed with your
operating system.  You need to be using bleeding-edge modern versions
of these libraries.

Example and Basic Tutorial
==========================
First, you need some C code.  Something important like computing a
fibonacci number::

    /* fib.c */
    int fib(int n) {
        if (n < 3) {
           return 1;
        } else {
           return fib(n-1) + fib(n-2);
        }
    }

Now, compile it into LLVM bitcode using clang::

    bash % clang -emit-llvm -c fib.c

This makes an object file ``fib.o`` as usual--only the .o file contains
LLVM bitcode.  Now, just import it into Python::

    >>> import bitey
    >>> import fib
    >>> fib.fib(38)
    39088169
    >>>

Yes, that's it. Bitey does not use the C compiler, the linker, or the
dynamic loader. You don't write wrapper functions either.
Write normal C, compile it with clang, and import it.  Done.

Bitey understands most basic C datatypes including integers, floats,
void, pointers, arrays, and structures.  Because it builds a ctypes
based interface, you would access the code using the same
techniques. Here is an example that mutates a value through a
pointer::

    /* mutate.c */

    void mutate_int(int *x) {
         *x *= 2;
    }

Here's how you would use this::

    % clang -emit-llvm -c mutate.c
    % python 
    >>> import bitey
    >>> import mutate
    >>> import ctypes
    >>> x = ctypes.c_int(2)
    >>> mutate.mutate_int(x)
    >>> x.value
    4
    >>> 

Here is an example involving a structure::

    /* point.c */
    #include <math.h>
 
    struct Point {
        double x;
        double y;
    };

    double distance(struct Point *p1, struct Point *p2) {
        return sqrt((p1->x - p2->x)*(p1->x - p2->x) + 
                    (p1->y - p2->y)*(p1->y - p2->y));
    }

To run::
 
    % clang -emit-llvm -c point.c
    % python
    >>> import bitey
    >>> import point
    >>> p1 = point.Point(3,4)
    >>> p2 = point.Point(6,8)
    >>> point.distance(p1,p2)
    5.0
    >>> 

One subtle issue with structure wrapping is that LLVM bitcode doesn't
encode the names of structure fields. So, Bitey simply assigns them
to an indexed element variable like this::

    >>> p1.e0         # (Returns the .x component)
    3
    >>> p1.e1         # (Returns the .y component)
    4

This can be fixed using a pre-load module as described in the
"Advanced Topics" section later.

If you need to combine two LLVM object files together into a single
importable module, use ``llvm-ld`` like this::

    % llvm-ld point.o fib.o -b combined.o
    % python
    >>> import bitey
    >>> import combined
    >>> combined.fib(10)
    55
    >>> p1 = combined.Point(3,4)
    >>> p2 = combined.Point(6,8)
    >>> combined.distance(p1,p2)
    5.0
    >>> 

The C code you write can link with external libraries, but you might
need to take special steps to load the library prior to import.  For
example, suppose you compiled the Fibonacci code into a shared library
like this::

    # OS-X
    % gcc -bundle -export_dynamic fib.c -o libfib.so     

    # Linux
    % gcc -shared fib.c -o libfib.so

Now, suppose you had some C code that wanted to access this library::

     /* sample.c */
     #include <stdio.h>
     extern int fib(int n);

     void print_fib(int n) {
         while (n > 0) {
             printf("%d\n", fib(n));
             n--;
         }
     }

If you try to build it normally, you'll get an error::

     % clang -emit-llvm -c sample.c
     % python
     >>> import bitey
     >>> import sample
     LLVM ERROR: Program used external function 'fib' which could not be resolved!
     % 

However, you can load the library yourself doing this::
 
    % python
    >>> import bitey
    >>> bitey.load_library("./libfib.so")
   <CDLL './libfib.so', handle 1003cfc60 at 10049d090>
    >>> import sample
    >>> sample.print_fib(10)
    55
    34
    21
    13
    8
    5
    3
    2
    1
    1
    >>>

It is important to note that Bitey is NOT a wrapper generator meant to
access already-compiled C libraries.   It only exposes functionality
that has been explicitly compiled as LLVM bitcode.   To access the 
contents of a library, you would need to compile and link it using 
``clang`` and ``llvm-ld`` as shown in the examples.

How it works
============
Bitey extends Python with an import hook that looks for ``.o`` files
containing LLVM bitcode. Type signatures and other information in the
bitcode are then used to build a ctypes-based binding to the natively
compiled functions contained within an LLVM execution engine.   It's
all a bit magical, but the LLVM JIT generates the executable code
whereas Bitey makes the ``ctypes`` binding to it---all behind the
scenes on import.

It's important to stress that Bitey does not use the C compiler, the
linker, the dynamic loader, or make calls to subprocesses.  It is
completely self-contained and only uses the functionality of
``llvm-py`` and ``ctypes``.

Performance
===========
The performance profile of Bitey is going to be virtually identical
that of using ``ctypes``.  LLVM bitcode is translated to native
machine code and Bitey builds a ``ctypes``-based interface to it
in exactly the same manner as a normal C library.

As a performance experiment, here is a simple C function that checks
if a number is prime or not::

   int isprime(int n) {
       int factor = 3;
       /* Special case for 2 */
       if (n == 2) {
           return 1;
       }
       /* Check for even numbers */
       if ((n % 2) == 0) {
          return 0;
       }
       /* Check for everything else */
       while (factor*factor < n) {
           if ((n % factor) == 0) {
               return 0;
           }
           factor += 2;
       } 
       return 1;
    }

Try compiling this code into LLVM and a C shared library::

    % clang -O3 -emit-llvm -c isprime.c

    # OS-X
    % gcc -O3 -bundle -undefined dynamic_lookup isprime.c -o isprime.so

    # Linux
    % gcc -O3 -shared isprime.c -o isprime.so

Now, let's put Bitey and ctypes in a head-to-head performance battle::

    >>> import bitey
    >>> from isprime import isprime as isprime1
    >>> import ctypes
    >>> ex = ctypes.cdll.LoadLibrary("./isprime.so")
    >>> isprime2 = ex.isprime
    >>> isprime2.argtypes=(ctypes.c_int,)
    >>> isprime2.restype=ctypes.c_int
    >>> 
    >>> from timeit import timeit
    >>> # Bitey
    >>> timeit("isprime1(3)","from __main__ import isprime1")
    1.1813910007476807
    >>> # ctypes
    >>> timeit("isprime2(3)", "from __main__ import isprime2")
    1.2408909797668457
    >>> 
    >>> # Bitey
    >>> timeit("isprime1(10143937)", "from __main__ import isprime1")
    9.839216947555542
    >>> # ctypes
    >>> timeit("isprime2(10143937)", "from __main__ import isprime2")
    9.663991212844849
    >>> 

As you can see, the performance is just about the same.  The main
difference would come down to the efficiency of LLVM vs. gcc code 
optimization.  

Advanced Usage
==============
If you're up for a bit of adventure, the module creation process can
be altered through the use of pre and post loading files.  

A pre-load file provides Python code that executes within the newly
created module prior to the LLVM-binding step.   One use of this
code is to specify the names of fields on data structures.  For
example, you can create the following pre-load file for the earlier
``Point`` example::

    # point.pre.py

    class Point:
        _fields_ = ['x','y']

If you do this, you'll find that the field-names get fixed::
 
   >>> import point
   >>> p = point.Point(3,4)
   >>> p.x
   3.0
   >>> p.y
   4.0
   >>>

You could also use a pre-load file to load library dependencies::

   # sample.pre.py
   import bitey
   bitey.load_library("./libfoo.so")

A post-load file allows you alter the contents of the module
after LLVM-binding.  You could use this to apply decorators
or add additional support code.  For example::

    # point.post.py
    #
    # Example of decorating a function already wrapped

    def decorate(func):
        def wrapper(*args, **kwargs):
            print "Calling", func.__name__
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper

    # Wrap the distance wrapper already created
    distance = decorate(distance)

The combination of the pre/post loading files gives you almost
unlimited opportunity for insane evil when loading the bitcode.
It must be stressed that that these files are executed in
the space of the module being created---they are not separate 
imports (i.e., the pre, post, and LLVM bindings all co-exist
in the same module namespace).

Automatic Binding
=================
In the examples, it is necessary to use ``import bitey`` for modules
to be recognized and loaded.  If you want to skip this step and make
everything automatic, create a ``bitey.pth`` file that contains the
following statement::

     # bitey.pth
     import bitey

Now, copy this file to the Python ``site-packages`` directory.

FAQ
===
Q: Will Bitey ever support C++?

A: No. C++ can bite me (*)

(*) I also wrote Swig and still have C++ scars. 

Q: Why is it called "Bitey?"

A: Well, "Bitey" is so much more catchy than simply calling it
something boring like "BIT (Bitcode Import Tool)".  Plus, just like
@johnderosa's pet Pomeranian of the same name, you're never quite sure
whether "Bitey" is adorably cute or a viscious beast that will
constantly nip your leg.   Actually, I just like the ring of
it--"Bitey" sort of rhymes with "Enterprisey".

Discussion Group
================
A discussion group for Bitey is available at http://groups.google.com/group/bitey

Authors
============
- David Beazley (@dabeaz),  http://www.dabeaz.com
