
import logging
import traceback
from typing import  List, Tuple

from src.database import sqlitedb
from src.document.doc import Doc

def table()-> bool:
	try:
		conn = sqlitedb.client()
		conn.execute("""
			create table if not exists documents (
				id integer primary key autoincrement,
				name text,
				path text,
				mimetype text
			)
		""")
		return True
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

def save(document: Doc)-> bool :
	try: 
		path = document.path
		doc_data = show_by_path(path)
		if doc_data.name and doc_data.path:
			return False

		doc_body = (document.name, path, document.mimetype) 
		conn = sqlitedb.client()
		conn.execute("insert into documents (name, path, mimetype) values (?, ?, ?)", doc_body)
		conn.commit()
		return True

	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

def show_by_path(path: str = "") -> Doc:
	try:
		_list = list_only_path(path)
		docs = []
		for doc in _list:
			_id, name, path, mimetype = doc
			docs.append(Doc(name, path, mimetype, _id))

		if(len(docs) == 0):
			raise ValueError("documento não encontrado com path")

		return docs[0]
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return Doc()

def show_list()-> List[Doc] :
	try:
		conn = sqlitedb.client()
		cursor = conn.execute("select * from documents")
		docs = []
		for doc in cursor:
			name, path, mimetype = doc
			docs.append(Doc(name, path, mimetype))

		if len(docs) == 0:
			raise ValueError("Não foi encontrado nenhum documento")

		return docs
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []

def list_only_path(path: str = "")-> List[Tuple(int, str, str, str)]:
	try:
		conn = sqlitedb.client()
		cursor = conn.execute("select * from documents where path=?", (path,))
		docs = []
		for doc in cursor:
			docs.append(doc)

		return docs
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []

def has_path(path: str = "")-> bool:
	try:
		if len(list_only_path(path)) == 0:
			return False
		return True
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False
