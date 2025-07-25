# Sibila - Sistema RAG para Análise de Documentos Jurídicos

Sistema avançado de **RAG (Retrieval Augmented Generation)** especializado em análise de documentos jurídicos, utilizando IA para responder perguntas baseadas em documentos fornecidos pelo usuário.

## 🎯 Visão Geral

Sibila combina processamento de linguagem natural, bancos de dados vetoriais e modelos de linguagem para criar um assistente inteligente de análise documental. Processa documentos PDF (especialmente legislação), extrai conhecimento estruturado e fornece respostas precisas via API REST.

## 🚀 Instalação e Uso

### 1. Preparação do Ambiente
```bash
git clone https://github.com/lucasfrct/sibila.git
cd sibila
cp .env.example .env
pip install -r requirements.txt
```

### 2. Configuração do Ollama
```bash
# Instalar e iniciar Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve

# Em outro terminal, baixar modelo
ollama pull llama3
```

### 3. Executar Aplicação
```bash
python main.py              # Com hot reload
python main.py --no-reload  # Sem hot reload
```

**Acesso:** `http://localhost:3000`

**Documentação completa:** [SETUP_LOCAL.md](./SETUP_LOCAL.md)

### 4. Gestão do Banco de Dados
```bash
# Verificar status das migrações
python migrate_cli.py status

# Aplicar migrações pendentes
python migrate_cli.py migrate

# Criar nova migração
python migrate_cli.py create "Adicionar nova tabela"
```

**Documentação do sistema de migração:** [DATABASE_MIGRATION_GUIDE.md](./DATABASE_MIGRATION_GUIDE.md)

## 🏗️ Arquitetura do Sistema

### Pipeline de Processamento
1. **Leitura de PDFs** (`src/modules/document/reader.py`) - Extração precisa com pdfplumber
2. **Análise Jurídica** (`src/modules/analysis/legislation.py`) - Classificação automática de artigos
3. **Processamento NLP** (`src/modules/nlp/`) - Classificação de texto e análise de sentimento
4. **Banco Vetorial** (`src/modules/database/chromadbvector.py`) - ChromaDB para busca semântica
5. **Modelos LLM** (`src/models/`) - Integração Ollama/OpenAI para geração de respostas

### Fluxo RAG
```
PDF → Extração → Análise → Vetorização → ChromaDB → Query → LLM → Resposta
```

## 📊 Stack Tecnológico

**Core:** Python 3.9+, Flask 3.1.1  
**Processamento:** pdfplumber, PyPDF2, scikit-learn, NLTK  
**IA/ML:** Ollama, OpenAI, ChromaDB, transformers  
**Banco:** SQLite (metadados), ChromaDB (vetorial)

## 🗂️ Estrutura de Diretórios

```
sibila/
├── src/                      # Código fonte principal
│   ├── config/              # Configurações (Ollama, OpenAI)
│   ├── models/              # Integrações com LLMs
│   ├── modules/             # Módulos funcionais
│   │   ├── analysis/        # Análise jurídica
│   │   ├── catalog/         # Sistema de catalogação
│   │   ├── corpus/          # Geração de corpus
│   │   ├── database/        # Bancos de dados (ChromaDB, SQLite)
│   │   ├── document/        # Processamento de documentos
│   │   ├── nlp/             # Processamento de linguagem
│   │   ├── prompts/         # Sistema de prompts
│   │   ├── response/        # Formatação de respostas
│   │   └── viz/             # Visualizações
│   ├── routes/              # Endpoints da API
│   ├── routines/            # Rotinas de migração
│   ├── utils/               # Utilitários diversos
│   └── server.py            # Configuração Flask
├── dataset/                 # Dados de treinamento
│   ├── sources/            # Documentos fonte (PDFs)
│   ├── corpus/             # Corpus processado (CSV)
│   └── _library/           # Biblioteca de referência
├── data/                   # Persistência de dados
│   └── .chromadb/         # Banco vetorial ChromaDB
├── tests/                  # Testes automatizados
└── main.py                # Ponto de entrada da aplicação
```

## 🔄 Principais Funcionalidades

- **Processamento de Documentos**: Leitura de PDFs, geração de metadados e conversão para texto
- **Análise Jurídica**: Classificação automática de categorias, tipos normativos e eficácia
- **Sistema de Corpus**: Extração de artigos e anotações automáticas via LLM
- **Banco Vetorial**: Armazenamento e busca semântica via ChromaDB
- **API REST**: Endpoints para corpus, datasets e health check
- **Modelos LLM**: Integração dual com Ollama e OpenAI

## ⚙️ Configuração

### Variáveis de Ambiente (.env)
```bash
OPENAI_API_KEY=        # Chave API OpenAI (opcional)
OLLAMA_PROXY_URL=      # URL proxy Ollama (opcional)
```

### Parâmetros do Modelo
- `temperature`: Controle de aleatoriedade (0.0-1.0)
- `max_tokens`: Limite de tokens de saída (4096)
- `context`: Janela de contexto (2048)
- `diffusion_of_hallucination`: Anti-alucinação (0.8)
