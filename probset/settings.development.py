try:
    from .shared_settings import *
except ImportError:
    print("Shared settings not found")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+x=df)-#r(ub3jc=vlzv)41kli7-5lq_404n#)l%xnl#3&2vm9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True