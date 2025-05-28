import logging
import traceback
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logging.error("Unhandled Exception:\n%s", traceback.format_exc())
        return jsonify({
            "code": 500,
            "message": "Server error, please contact the administrator."
        }), 500
