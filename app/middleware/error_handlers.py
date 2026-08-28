import logging
from flask import render_template, request, jsonify

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Bad Request', 'message': str(error.description if hasattr(error, 'description') else error)}), 400
        return render_template('errors/400.html', error=error), 400

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Unauthorized', 'message': 'Authentication is required.'}), 401
        return render_template('errors/401.html', error=error), 401

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to perform this action.'}), 403
        return render_template('errors/403.html', error=error), 403

    @app.errorhandler(404)
    def not_found(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found.'}), 404
        return render_template('errors/404.html', error=error), 404

    @app.errorhandler(429)
    def ratelimit_exceeded(error):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Rate Limit Exceeded', 'message': 'Too many requests. Please slow down.'}), 429
        return render_template('errors/429.html', error=error), 429

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}", exc_info=True)
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected server error occurred.'}), 500
        return render_template('errors/500.html', error=error), 500
