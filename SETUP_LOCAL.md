# Guia de Configuração Local - Sibila Sínica

## Visão Geral
O Sibila é uma aplicação de chatbot baseada em Flask que responde perguntas baseadas em documentos fornecidos pelo usuário, utilizando LLM (Llama 3) via Ollama.

## Pré-requisitos

### Software Necessário
- Python 3.8+ (recomendado Python 3.12+)
- pip (gerenciador de pacotes Python)
- Ollama (para execução do modelo LLM)
- Git

### Sistema Operacional
- Linux (Ubuntu/Debian recomendado)
- macOS
- Windows (com WSL recomendado)

## Configuração do Ambiente Local

### 1. Clonar o Repositório
```bash
git clone https://github.com/lucasfrct/sibila.git
cd sibila
```

### 2. Configurar Variáveis de Ambiente
```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure as variáveis:
```
OPENAI_API_KEY=sua_chave_openai_aqui  # Opcional, se quiser usar OpenAI
OLLAMA_PROXY_URL=http://localhost:11434  # URL do Ollama local
```

### 3. Instalar Dependências Python

#### Opção A: Pip (Recomendado)
```bash
# Instalar todas as dependências
pip install -r requirements.txt

# OU instalar dependências mínimas essenciais
pip install flask python-dotenv pdfplumber ollama openai sqlite3 requests
```

#### Opção B: Sistema Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3-flask python3-dotenv python3-requests python3-pip
pip install pdfplumber ollama openai
```

### 4. Configurar e Instalar Ollama

#### Instalar Ollama
```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# OU baixar diretamente de https://ollama.ai/download
```

#### Iniciar Ollama
```bash
# Iniciar o servidor Ollama
ollama serve
```

#### Baixar Modelo Llama (em outro terminal)
```bash
# Baixar o modelo Llama 3 (8B recomendado)
ollama pull llama3

# OU modelo menor para testes
ollama pull llama3:8b
```

### 5. Executar a Aplicação

#### Modo Desenvolvimento (com hot reload)
```bash
python main.py
```

#### Modo Produção (sem hot reload)
```bash
python main.py --no-reload
```

A aplicação estará disponível em `http://localhost:5000`

## Endpoints da API

### Saúde da Aplicação
```
GET /api/v1/health
```

### Completions (Perguntas para o LLM)
```
POST /api/v1/completions
Content-Type: application/json

{
  "question": "Sua pergunta aqui",
  "context": "Contexto opcional"
}
```

### Histórico de Completions
```
GET /api/v1/completions/history
```

### Pesquisa no Catálogo
```
GET /api/v1/catalog/search?q=termo_pesquisa
```

### Listar Catálogo
```
GET /api/v1/catalog
```

### Indexar Documentos
```
POST /api/v1/catalog/indexer
Content-Type: application/json

{
  "document_path": "/caminho/para/documento.pdf"
}
```

### Gerar Corpus
```
POST /api/v1/corpus/generate
```

### Detalhes de Páginas do Documento
```
GET /api/v1/document/pages?document_id=123
```

## Estrutura do Projeto

```
sibila/
├── main.py                    # Ponto de entrada da aplicação
├── requirements.txt           # Dependências Python
├── .env.example              # Exemplo de variáveis de ambiente
├── .env                      # Variáveis de ambiente (criar)
├── src/
│   ├── server.py             # Configuração do Flask
│   ├── routes/               # Rotas da API
│   ├── modules/              # Módulos de negócio
│   ├── models/               # Modelos de dados
│   ├── config/               # Configurações
│   └── utils/                # Utilitários
├── dataset/                  # Dados de treinamento e inicialização
├── data/                     # Persistência de dados (criado automaticamente)
└── .deploy/                  # Configurações Docker
```

## Execução com Docker (Alternativa)

### Usando Docker Compose
```bash
# Subir todos os serviços
docker-compose -f .deploy/docker-compose.yml up -d

# Ollama estará em http://localhost:11434
# Chatbot interface estará em http://localhost:3210
```

### Serviços Inclusos
- **ollama**: Servidor LLM em `localhost:11434`
- **chatbot**: Interface web em `localhost:3210`

## Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Instalar dependência específica
pip install nome_do_modulo

# OU instalar todas as dependências
pip install -r requirements.txt
```

### Erro: "Connection refused" (Ollama)
```bash
# Verificar se Ollama está rodando
ollama list

# Iniciar Ollama se não estiver rodando
ollama serve
```

### Erro: "No module named 'pdfplumber'"
```bash
pip install pdfplumber
```

### Problemas de Encoding
O arquivo `requirements.txt` pode ter problemas de encoding. Se necessário:
```bash
# Converter encoding
iconv -f UTF-16 -t UTF-8 requirements.txt > requirements_fixed.txt
mv requirements_fixed.txt requirements.txt
```

## Testes

### Verificar Funcionamento Básico
```bash
# Testar conexão com a API
curl http://localhost:5000/api/v1/health

# Testar completion simples
curl -X POST http://localhost:5000/api/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"question": "Olá, como você está?"}'
```

## Desenvolvimento

### Executar Testes
```bash
# Se houver testes configurados
python -m pytest tests/

# OU
python -m unittest discover tests/
```

### Linting
```bash
# Se flake8 estiver configurado
flake8 src/
```

## Notas Importantes

1. **Ollama é essencial**: A aplicação depende do Ollama para funcionar completamente
2. **Modelos LLM**: Certifique-se de ter pelo menos um modelo baixado (`ollama pull llama3`)
3. **Documentos PDF**: A aplicação processa documentos PDF para criar contexto para o chatbot
4. **Banco de Dados**: SQLite é usado por padrão, criado automaticamente na pasta `data/`
5. **Ambiente Virtual**: Recomendado usar `venv` ou `conda` para isolar as dependências

## Suporte

Para problemas específicos, consulte:
- Documentação do Ollama: https://ollama.ai/
- Logs da aplicação (saída do console)
- Issues do repositório no GitHub