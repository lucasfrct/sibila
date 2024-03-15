import PyPDF2
import os

class Paragraph:

	def __init__(self, name, page, number, content, offset_line = 0):

		self.number = number
		self.page = page
		self.name = name
		self.chunk = []
		self.line = {}

		self.line_start = offset_line
		self.line_end = offset_line
		self.size = len(content)
		self.chunks = 0
		self.lines = 0

		ln = content.split("\n")

		self.lines = len(ln)
		self.line_end = self.line_start + self.lines

		for i  in range(self.lines):
			self.line[i] = ln[i]

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
				"paragraph": self.number,
				"line_end": self.line_end,
				"name": self.name,
				"page": self.page,
				"patition": i
			})
		return self.chunk, metadatas

	def split_to_chunks(self, content):
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
	def __init__(self, name, number, content, offset_line = 0):

		self.number = number
		self.paragraph = {}
		self.name = name

		self.line_start = offset_line
		self.line_end = offset_line
		self.paragraphs = 0
		self.chunks = 0
		self.lines = 0
		self.size = 0

		pr = content.split("\n\n")
		self.paragraphs = len(pr)

		for i in range(self.paragraphs):
			self.paragraph[i] = Paragraph(self.name, self.number, i, pr[i], offset_line)
			self.chunks += self.paragraph[i].chunks
			self.lines += self.paragraph[i].lines
			self.size += self.paragraph[i].size

		self.line_end = self.line_start + self.lines - 1

	@property
	def content(self): 
		content = ""
		for i in range(self.paragraphs):
			content += self.paragraph[i].content
		return content

	@property
	def chunk(self):
		ck = []
		for i in range(self.paragraphs):
			ck.extend(self.paragraph[i].chunk)
		return ck

	@property
	def chunks_and_metadatas(self):
		metadatas = []
		chunks = []
		for i in range(self.paragraphs):
			ck, mt = self.paragraph[i].chunks_and_metadatas
			metadatas.extend(mt)
			chunks.extend(ck)

		return chunks, metadatas
	
class Doc:

	def __init__(self, path = "", name = ""):
	
		self.page = {}
		self.name = name
		
		self.offset_line = 1
		self.line_start = 1
		self.paragraphs = 0
		self.line_end = 0
		self.chunks = 0
		self.pages = 0
		self.lines = 0
		self.size  = 0

		file = open(path, 'rb')
		reader = PyPDF2.PdfReader(file)
		self.pages = len(reader.pages)

		for i in range(self.pages):
			page = reader.pages[i]
			page_number = (i + 1)
			content = page.extract_text()
			self.page[i] = Page(self.name, page_number, content, self.offset_line)
			self.paragraphs += self.page[i].paragraphs
			self.chunks += self.page[i].chunks
			self.lines += self.page[i].lines
			self.size += self.page[i].size

			self.offset_line += self.page[i].lines

		self.line_end = self.line_start + self.lines - 1

	@property
	def content(self):
		content = ""
		for i in range(self.pages):
			content += self.page[i].content
		return content

	@property
	def chunk(self):
		ck = []
		for i in range(self.pages):
			ck.extend(self.page[i].chunk)
		return ck

	@property
	def chunks_and_metadatas(self):
		metadatas = []
		chunks = []
		for i in range(self.pages):
			ck, mt = self.page[i].chunks_and_metadatas
			metadatas.extend(mt)
			chunks.extend(ck)

		return chunks, metadatas
