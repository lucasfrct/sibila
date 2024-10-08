# flake8: noqa: E501


from src.routines import migrate
from src.server import app

def run():
    app.run(debug=True)


if __name__ == "__main__":
    migrate.tables()
    run()
