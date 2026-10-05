"""
AlgoLens Flask Application Factory
==================================
Creates and configures the Flask REST API application instance.
"""

from flask import Flask, jsonify
from .routes import api_bp


def create_app() -> Flask:
    """Create and configure the AlgoLens Flask application."""
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Configure CORS headers on all responses
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    import os
    from flask import send_from_directory

    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

    @app.route('/')
    @app.route('/visualize')
    @app.route('/algorithms')
    @app.route('/compare')
    @app.route('/datasets')
    @app.route('/history')
    @app.route('/about')
    def serve_frontend():
        return send_from_directory(static_dir, 'index.html')

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory(static_dir, filename)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
