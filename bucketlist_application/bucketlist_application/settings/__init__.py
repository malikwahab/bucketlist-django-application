import os

if not os.getenv('TRAVIS') and not os.getenv('HEROKU'):
    from .development import *

if os.getenv('HEROKU') is not None:
    from .production import *
