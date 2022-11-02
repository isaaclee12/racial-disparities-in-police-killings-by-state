import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/dev/')
from main import app as application
# SECRET KEY REMOVED FOR SECURITY - Set FLASK_SECRET_KEY environment variable
import os
application.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-only-insecure-key')
