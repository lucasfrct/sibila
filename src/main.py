# flake8: noqa: E501

from src.modules.librarian import librarian as Librarian


def run():
    Librarian.register_in_bath("./library")

if __name__ == "__main__":
    run()
