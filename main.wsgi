import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/dev/')
from main import app as application
application.secret_key = 'cs205Project'
