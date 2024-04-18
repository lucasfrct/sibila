import logging
import PyPDF2
import os

from typing import List, Dict, Tuple

class Paragraph:

	def __init__(self, doc, page, number: int = 1, content: str = ""):

		self.page = page.number
		self.name = doc.name
		self.number = number
		self.chunk = []
		self.line = {}

		self.line_start = doc.offset_line
		self.line_end = doc.offset_line
		self.size = len(content)
		self.chunks = 0
		self.lines = 0

		lines_raw = content.split("\n")

		self.lines = len(lines_raw)
		self.line_end = self.line_start + self.lines

		for i  in range(self.lines):
			line_number = (i + 1)
			self.line[line_number] = lines_raw[i]

		self.chunks_size = 1000
		self.offset = 200

		self.chunk = self.split_to_chunks(content)
		self.chunks = len(self.chunk)

	@property
	def content(self): 
		content = ""
		for i in range(self.chunks):
			content += self.chunk[i]
		return content

	@property
	def chunks_and_metadatas(self):
		metadatas = []
		for i in range(self.chunks):
			metadatas.append({
				"source": f"{self.name}, pg. {self.page}, ln ({self.line_start} a {self.line_end})",
				"line_start": self.line_start,
				"line_end": self.line_end,
				"paragraph": self.number,
				"name": self.name,
				"page": self.page,
				"patition": i
			})
		return self.chunk, metadatas

	def split_to_chunks(self, content: str) -> List[str]:
		chunks_data = []
		for i in range(0, len(content), self.chunks_size):
			start = i
			end = i + 1000
			if start != 0:
				start = start - self.offset
				end =  end - self.offset
			chunks_data.append(content[start:end])
		return chunks_data

class Page: 
	def __init__(self, doc, number, content):

		self.number = number
		self.name = doc.name
		self.paragraph = {}

		self.line_start = doc.offset_line
		self.line_end = doc.offset_line
		self.paragraphs = 0
		self.chunks = 0
		self.lines = 0
		self.size = 0

		paragraph_raw = content.split("\n\n")
		self.paragraphs = len(paragraph_raw)

		for i in range(self.paragraphs):

			paragraph_number = (i + 1)
			content = paragraph_raw[i]

			paragraph = Paragraph(doc, self, paragraph_number, content)
			self.chunks += paragraph.chunks
			self.lines += paragraph.lines
			self.size += paragraph.size
			self.paragraph[paragraph_number] = paragraph

		self.line_end = self.line_start + self.lines - 1

	@property
	def content(self): 
		content = ""
		for i in range(self.paragraphs):
			content += self.paragraph[i+1].content
		return content

	@property
	def chunk(self):
		ck = []
		for i in range(self.paragraphs):
			ck.extend(self.paragraph[i+1].chunk)
		return ck

	@property
	def chunks_and_metadatas(self):
		metadatas = []
		chunks = []
		for i in range(self.paragraphs):
			ck, mt = self.paragraph[i+1].chunks_and_metadatas
			metadatas.extend(mt)
			chunks.extend(ck)

		return chunks, metadatas
	
class Doc:

	def __init__(self, name: str = "", path: str = "", mimetype: str = "pdf", id: int = 0):
	
		self.page = {}
		self.id = id
		self.name = name
		self.path = path
		self.mimetype = mimetype
		
		self.data_embeddinds = []
		self.offset_line = 1
		self.line_start = 1
		self.paragraphs = 0
		self.embeddings = 0
		self.line_end = 0
		self.chunks = 0
		self.pages = 0
		self.lines = 0
		self.size  = 0

		reader = self.read(self.path)
		if reader != None:
			self.pages = len(reader.pages)

			for i in range(self.pages):
				
				page_raw = reader.pages[i]
				page_number = (i + 1)
				content = page_raw.extract_text()

				page = Page(self, page_number, content)
				self.paragraphs += page.paragraphs
				self.offset_line += page.lines
				self.chunks += page.chunks
				self.lines += page.lines
				self.size += page.size

				self.page[page_number] = page

			self.line_end = self.line_start + self.lines - 1

	def read(self, path: str = ""):
		try:
			file = open(os.path.normpath(path), 'rb')
			return PyPDF2.PdfReader(file)
		except Exception as e:
			logging.error(e)
			return None

	def set_embeddings(self, embedings):
		self.data_embeddinds = embedings
		self.embeddings = len(embedings)

	def get_embedings(self):
		return self.data_embeddinds

	@property
	def content(self):
		content = ""
		for i in range(self.pages):
			content += self.page[i+1].content
		return content

	@property
	def chunk(self):
		ck = []
		for i in range(self.pages):
			ck.extend(self.page[i+1].chunk)
		return ck

	@property
	def chunks_and_metadatas(self)-> Tuple[[], []]:
		metadatas = []
		chunks = []
		for i in range(self.pages):
			ck, mt = self.page[i+1].chunks_and_metadatas
			metadatas.extend(mt)
			chunks.extend(ck)

		return chunks, metadatas

	@property
	def chunks_embedings_and_metadatas(self)-> Tuple[[], [], []]:
		chunks, metadatas = self.chunks_and_metadatas
		return chunks, self.data_embeddinds, metadatas

	@property
	def info(self):
		return f"{self.name} | páginas: {self.pages} | paragrafos: {self.paragraphs} | chunks: {self.chunks} | linhas: {self.lines}"
