# flake8: noqa: E501

import sys

from src.routines import migrate
from src.server import app


if __name__ == "__main__":
    migrate.tables()
    no_reload = '--no-reload' in sys.argv
    app.run(debug=True, use_reloader=not no_reload)
