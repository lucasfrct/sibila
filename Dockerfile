# ## python para desenvolvimento

# ! ## STAGE 1 - Maquina para armazenar as dependencias
FROM python:3 AS environment-python-dependences

WORKDIR /app

# ## install tools
RUN pip install chromadb
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ! ## STAGE 2 - Maquina para excutar o ambiente de desenvolvimento
FROM environment-python-dependences AS environment-python-dev

COPY . .

CMD [ "python", "./main.py" ]