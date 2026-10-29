"""Flask app factory served by Apache httpd."""

from datetime import UTC, datetime
from importlib.metadata import version
from os import environ

from flask import Flask, Response, jsonify

SERVICE_NAME = "flask-apache"
STARTED_AT = datetime.now(UTC)


def _envelope(data: dict[str, object]) -> Response:
    """Wrap a payload with the timestamp every response carries."""
    return jsonify(timestamp=datetime.now(UTC).isoformat(), **data)


def create_app() -> Flask:
    app = Flask(__name__)
    # Secret comes from the environment, never from source.
    app.secret_key = environ.get("SECRET_KEY", "")

    @app.get("/")
    def index() -> Response:
        return _envelope({"message": "Flask is running behind Apache"})

    @app.get("/health")
    def health() -> Response:
        return _envelope({"status": "UP"})

    @app.get("/info")
    def info() -> Response:
        return _envelope(
            {
                "service": SERVICE_NAME,
                "version": version(SERVICE_NAME),
                "started_at": STARTED_AT.isoformat(),
                "server": environ.get("SERVER_SOFTWARE", "unknown"),
            }
        )

    return app
