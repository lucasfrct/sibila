# flake8: noqa: E501

import asyncio

from src.routines import migrate
from src.server import app


if __name__ == "__main__":
    migrate.tables()
    app.run(debug=True)
