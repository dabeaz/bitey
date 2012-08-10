# client.py
#
# An example of reading a LLVM bit-code file, sending it to a remote
# server, and then doing some RPC calls on it.   For this to work,
# you first need to run the server program like this:
#
#      % python remote.py 15000
#
# Note: multiprocessing.connection objects are used for communications.
# It would be easy to change this to use ZeroMQ or some other messaging.

import remote

# Grab the bitcode from a file
bitcode = open("fib.o","rb").read()

# Connect to remote server
mod = remote.RemoteModule('fib', bitcode, ('localhost',15000), b'peekaboo')

# Now, execute remote calls
for n in range(1,45):
    print(mod.fib(n))
