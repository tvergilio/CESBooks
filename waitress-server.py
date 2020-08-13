from waitress import serve
import application
serve(application.app, host='0.0.0.0', port=80)
