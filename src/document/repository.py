
import logging
import traceback
from typing import List

from src.database import sqlitedb

def table()-> bool:
	try:
		conn = sqlitedb.client()
		conn.execute("""
			create table if not exists documents (
				id text primary key,
				name text,
				path text,
				mimetype text
			)
		""")
		return True
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

def table_metadata()-> bool:
	try:
		conn = sqlitedb.client()
		conn.execute("""
			create table if not exists lines (
				uuid text primary key,
				letters interger,
				page interger,
				content text,
				source text,
				name text,
				path text
			)
		""")
		return True
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

def save(document)-> bool :
	try: 
		path = document["path"]
		doc_data = show_by_path(path)

		if doc_data != None:
			return False

		doc_body = (document["name"], path, document["mimetype"]) 
		conn = sqlitedb.client()
		conn.execute("insert into documents (name, path, mimetype) values (?, ?, ?)", doc_body)
		conn.commit()
		return True

	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

def show_by_path(path: str = ""):
	try:
		_list = list_raw(path)
		docs = []
		for doc in _list:
			_id, name, path, mimetype = doc
			docs.append({ 'name': name, 'path': path, 'mimetype': mimetype, 'id': _id })

		if(len(docs) == 0):
			return None

		return docs[0]
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return None

def show_list()-> List[object] :
	try:
		conn = sqlitedb.client()
		cursor = conn.execute("select * from documents")
		docs = []
		for doc in cursor:
			_id, name, path, mimetype = doc
			docs.append({ 'name': name, 'path': path, 'mimetype': mimetype, 'id': _id })

		if len(docs) == 0:
			return []

		return docs
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []

def list_raw(path: str = ""):
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

def has_document(path: str = "")-> bool:
	try:
		if len(list_raw(path)) == 0:
			return False
		return True
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

def save_metadata(metadata = {})-> bool :
	try: 
		meta_body = (
      		metadata['uuid'], 
          	metadata['letters'], 
        	metadata['page'], 
           	metadata['content'], 
           	metadata['source'], 
            metadata['name'], 
            metadata['path'],
        ) 
  
		conn = sqlitedb.client()
		conn.execute("insert into lines (uuid, letters, page, content, source, name, path) values (?, ?, ?, ?, ?, ?, ?)", meta_body)
		conn.commit()
		return True

	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return False

def list_lines():
	try:
		conn = sqlitedb.client()
		cursor = conn.execute("select * from lines")
		lines = []
		for line in cursor:
			lines.append(extract_line(line))

		if len(lines) == 0:
			raise ValueError("Não foi encontrado nenhum documento")

		return lines
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []

def query_metadata_include(term: str = "", results: int = 10) :
	try:
		conn = sqlitedb.client()
		cursor = conn.execute(f"select * from lines where content like '%{term}%' limit {results}")
		lines = []
		for line in cursor:
			lines.append(extract_line(line))

		if len(lines) == 0:
			raise ValueError("Não foi encontrado nenhum documento")

		return lines
	except Exception as e:
		logging.error(f"{e}\n%s", traceback.format_exc())
		return []

def extract_line(line):
    uuid, letters, page, content, source, name, path = line
    return {
		'letters': letters,
		'content': content,
		'source': source,
		'uuid': uuid,
		'page': page,
		'name': name,
		'path': path,
	}