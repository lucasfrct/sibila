import traceback
import logging
import sqlite3
import os

# path = ./data/sqlite
def client(path: str = "./data/sqlite") -> object:
	try:
		if not os.path.exists(path):
			os.makedirs(path)
		return sqlite3.connect(f"{path}/sqlite.db")
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return None

def db() -> object:
	return sqlite3