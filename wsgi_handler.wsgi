import sys, os
sys.path.insert(0, os.path.dirname(__file__)) 
from application import app as application
application.debug = True