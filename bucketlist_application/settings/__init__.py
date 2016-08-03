import os

if os.getenv('HEROKU') is not None:
    from .produnction import *
elif os.getenv('TRAVIS') is not None:
    from test import *
else:
    from development import *
