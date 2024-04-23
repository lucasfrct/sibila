# ## python para desenvolvimento

# ! ## STAGE 1 - Maquina para armazenar as ferramentas
FROM python:3 AS environment-python-tools

WORKDIR /app

# ## install tools
RUN pip install numpy
RUN pip install pyvis
RUN pip install PyPDF2
RUN pip install openai
RUN pip install ollama
RUN pip install fastapi
RUN pip install unicorn
RUN pip install chromadb
RUN pip install pysqlite3
RUN pip install tokenizers
RUN pip install onnxruntime
RUN pip install scikit-learn

# ! ## STAGE 1 - Maquina para armazenar as dependencias
FROM environment-python-tools AS environment-python-dependences

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ! ## STAGE 3 - Maquina para excutar o ambiente de desenvolvimento
FROM environment-python-dependences AS environment-python-dev

WORKDIR /app

COPY . ./

CMD [ "python", "./agent.py" ]