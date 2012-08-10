# remote.py
'''
Remote module transfer, loading and procedure call using Bitey.
RemoteModuleServer opens up a connection and waits for an incoming
connection.  Upon connection, it receives a payload of LLVM bitcode
that is then turned into a proper Python module.  Afterwards, 
it implements RPC with the loaded module.

To create and run a server:

   serv = RemoteModuleServer(('',15000),authkey=b'123')
   serv.serve_client()

To connect as a client:

   bitcode = open("somebitcode.o","rb").read()
   client = RemoteModule('modname',bitcode,
                         ('localhost',15000), authkey=b'123')

Now, execute remote functions:

   client.foo(1,2,3)
   client.bar(4.5)
   ...
'''

from multiprocessing.connection import Listener, Client
import bitey.loader
import sys

class RemoteModuleServer(object):
    def __init__(self, address, authkey):
        self.conn = Listener(address, authkey=authkey)
        
    def serve_client(self):
        while True:
            print("Waiting for connection")
            client = self.conn.accept()
            # Receive module name and bitcode from the client
            name, bitcode = client.recv()
            print("Received module %s" % name)
            mod = bitey.loader.build_module(name, bitcode)
            sys.modules[name] = mod
            while True:
                # Now, receive requests
                name, args, kwargs = client.recv()
                try:
                    result = getattr(mod, name)(*args, **kwargs)
                    client.send(result)
                except Exception as e:
                    client.send(e)

class RemoteModule(object):
    def __init__(self, name, bitcode, address, authkey):
        self.conn = Client(address, authkey=authkey)
        self.conn.send((name, bitcode))

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self.conn.send((name, args, kwargs))
            return self.conn.recv()
        return do_rpc

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: %s port\n" % sys.argv[0])
        raise SystemExit(1)

    # Create the server and start serving clients
    serv = RemoteModuleServer(("",int(sys.argv[1])), authkey=b"peekaboo")
    while True:
        try:
            serv.serve_client()
        except EOFError:
            print("Goodbye!")






