import application
import os
from waitress import serve
serve(application.app, host='0.0.0.0', port=os.environ.get('PORT', 17995))
