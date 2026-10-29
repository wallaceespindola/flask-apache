"""mod_wsgi entry point. The venv and src path come from WSGIDaemonProcess."""

import logging
import sys

logging.basicConfig(stream=sys.stderr)

from flask_apache import create_app  # noqa: E402

application = create_app()
