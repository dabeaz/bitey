# point.post.py
#
# Code that executes in the point module *after* LLVM binding

print "Decorating"

def decorate(func):
    def wrapper(*args, **kwargs):
        print "Calling", func.__name__
        return func(*args, **kwargs)
    return wrapper

distance = decorate(distance)
