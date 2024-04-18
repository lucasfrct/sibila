
import sqlite3
import os

# path = ./data/sqlite
def client_db(path: str = "./data/sqlite"):
	if not os.path.exists(path):
		os.makedirs(path)
	return sqlite3.connect(f"{path}/sqlite.db")

def table_documents():
	conn = client_db()
	conn.execute("""
		create table if not exists documents (
		id integer primary key autoincrement,
		name text,
		path text,
		mimetype text
		)
	""")

def add_document(document) :
	
	_, path, _ = document
	doc_data = get_documents_by_path(path)
    
	if(len(doc_data) == 0):
		conn = client_db()
		conn.execute("insert into documents (name, path, mimetype) values (?, ?, ?)", document)
		conn.commit()
		return True
	return False


def get_documents_by_path(path: str = "") :
	conn = client_db()
	cursor = conn.execute("select * from documents where path=?", (path,))
	docs = []
	for doc in cursor:
		docs.append(doc)

	return docs

def get_documents()-> sqlite3.Cursor :
	conn = client_db()
	cursor = conn.execute("select * from documents")
	docs = []
	for doc in cursor:
		docs.append(doc)

	return docs
