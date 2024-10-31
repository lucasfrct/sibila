import time

from src.utils.colors import colors


def delay(content, delay=0.01):
    print(f"{colors.OKCYAN}------------------------------------------------------------------------------------------------------------------------------------------", "\n", end='', flush=True)  # noqa: E501
    print(f"{colors.BOLD}R: {colors.ENDC}{colors.OKCYAN}", end='', flush=True)  # noqa: E501

    for letter in content:
        print(letter, end='', flush=True)
        time.sleep(delay)

    print()
    print(f"{colors.OKCYAN}------------------------------------------------------------------------------------------------------------------------------------------{colors.ENDC}")  # noqa: E501
    print("\n")
