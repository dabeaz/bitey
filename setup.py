from distutils.core import setup
setup(name = "bitey",
            description="Bitcode Import Tool",
            long_description = """
Bitey allows LLVM bitcode to be directly imported into Python as
an high performance extension module without the need for writing wrappers.
""",
            license="""BSD""",
            version = "0.0",
            author = "David Beazley",
            author_email = "dave@dabeaz.com",
            maintainer = "David Beazley",
            maintainer_email = "dave@dabeaz.com",
            url = "https://github.com/dabeaz/bitey/",
            packages = ['bitey'],
            classifiers = [
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 3',
              ]
            )
