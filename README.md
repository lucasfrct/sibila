# Sibila - Sistema RAG para Análise de Documentos Jurídicos

As sibilas eram figuras da mitologia inspiradas pelos deuses para profetizar. Esse repositório implementa um sistema avançado de **RAG (Retrieval Augmented Generation)** especializado em análise de documentos jurídicos, capaz de responder perguntas baseadas em documentos fornecidos pelo usuário através de inteligência artificial.

## 🎯 Visão Geral do Sistema

Sibila é uma aplicação Python que combina processamento de linguagem natural, bancos de dados vetoriais e modelos de linguagem para criar um assistente inteligente para análise documental. O sistema processa documentos PDF (especialmente legislação), extrai conhecimento estruturado e fornece respostas precisas através de uma API REST.

## 🚀 Como Executar Localmente

### Configuração Rápida

1. **Clone o repositório**
```bash
git clone https://github.com/lucasfrct/sibila.git
cd sibila
```

2. **Configure o ambiente**
```bash
cp .env.example .env
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Instale e configure o Ollama**
```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Iniciar o servidor Ollama
ollama serve

# Em outro terminal, baixar o modelo
ollama pull llama3
```

5. **Execute a aplicação**
```bash
python main.py
```

A aplicação estará disponível em `http://localhost:3000`

### Execução sem Hot Reload
```bash
python main.py --no-reload
```

### 📖 Guia Completo
Para instruções detalhadas, consulte: **[SETUP_LOCAL.md](./SETUP_LOCAL.md)**

## 🏗️ Arquitetura do Sistema

### Pipeline de Processamento de Documentos

O sistema implementa um pipeline sofisticado para processamento de documentos PDF:

#### 1. **Módulo de Leitura (`src/modules/document/reader.py`)**
- **Biblioteca principal**: `pdfplumber` para extração precisa de texto
- **Funcionalidades**:
  - Leitura completa de documentos PDF
  - Extração de páginas específicas com controle de intervalo
  - Mecânica de limite de páginas com validação automática
  - Tratamento de erros e logging detalhado

#### 2. **Sistema de Metadados (`src/modules/document/`)**
- **Metadados de página** (`page_metadata.py`): Informações estruturais de cada página
- **Metadados de parágrafo** (`paragraph_metadata.py`): Segmentação em parágrafos com posicionamento
- **Metadados de frase** (`phrase_metadata.py`): Granularidade no nível de sentença
- **Repositórios de dados**: Persistência SQLite com padrão Repository

#### 3. **Análise de Legislação (`src/modules/analysis/legislation.py`)**
- **Divisão automática em artigos**: Regex avançado para identificar estrutura legal
- **Classificação de categorias jurídicas**:
  - Direito Constitucional, Trabalhista, Civil, Penal
  - Direito Administrativo, Tributário, Ambiental, etc.
- **Identificação de tipos normativos**: Lei, Decreto, Portaria, Resolução, etc.
- **Sistema de eficácia normativa**: Plena, Limitada, Contida

### Sistema de Processamento de Linguagem Natural

#### 1. **Módulo NLP (`src/modules/nlp/`)**

**Bag of Words (BoW)** (`bow.py`):
```python
# Geração de vocabulário com sklearn CountVectorizer
def generate_bow(content: str) -> dict:
    processed_content = Str.removal_stopwords(content)
    vectorizer = CountVectorizer()
    bow = vectorizer.fit_transform([processed_content])
    # Retorna dicionário palavra: frequência
```

**Classificação de Texto** (`classifier.py`):
- **Algoritmo**: Regressão Logística com TF-IDF
- **Pipeline**: Vetorização → Treinamento → Predição
- **Persistência**: Modelos salvos em formato joblib
- **Avaliação**: Classification report do scikit-learn

**Análise de Sentimento** (`sentiment.py`):
- Classificação emocional de textos jurídicos
- Integração com pipeline de análise de documentos

**Extração de Features** (`featureextractor.py`):
- Características linguísticas relevantes para classificação
- Otimização para domínio jurídico

#### 2. **Pré-processamento Avançado**
- **Remoção de stop words**: Lista customizada para português jurídico
- **Normalização de texto**: Tratamento de caracteres especiais
- **Tokenização inteligente**: Preservação de termos jurídicos específicos

### Banco de Dados Vetorial e Recuperação

#### ChromaDB Integration (`src/modules/database/chromadbvector.py`)

**Configuração do Cliente**:
```python
def client(path: str = "./data/.chromadb") -> chromadb.ClientAPI:
    return chromadb.PersistentClient(path=path)
```

**Funcionalidades principais**:
- **Armazenamento vetorial**: Embeddings de documentos e chunks
- **Busca por similaridade**: Recuperação baseada em distância cossenoidal
- **Gestão de coleções**: Organização hierárquica de documentos
- **Detecção de conflitos**: Prevenção de duplicação de IDs
- **Indexação HNSW**: Performance otimizada para buscas aproximadas

### Integração com Modelos de Linguagem

#### 1. **Suporte Dual para LLMs (`src/models/`)**

**Ollama Local** (`ollama.py`):
```python
class ModelOllama:
    def __init__(self, model: str = "sibila"):
        self.client = ollama
        self.temperature = 0.5           # Controle de aleatoriedade
        self.max_tokens = 4096          # Limite de tokens de saída
        self.context = 2048             # Janela de contexto
        self.diffusion_of_hallucination = 0.8  # Anti-alucinação
```

**OpenAI Cloud** (`open_ai.py`):
- Integração com API oficial da OpenAI
- Fallback para quando Ollama não está disponível
- Suporte a modelos GPT-3.5/GPT-4

#### 2. **Sistema de Prompts Avançado (`src/modules/prompts/prompts.py`)**

**Persona de Bibliotecário IA**:
```python
def resume(documents: str) -> str:
    prompt_template = """Você é um assistente de IA com experiência de um bibliotecário organizado.
    Você tem uma alta capacidade de organizar ideias, documentos, assuntos e sessões.
    Os documentos abaixo apresentam as fontes atualizadas e devem ser consideradas como verdade.
    Suas respostas são apenas baseadas no documento e não deve inventar, adicionar ou alucinar.
    Gere um resumo de no máximo 50 palavras...
    """
```

**Tipos de prompts implementados**:
- **Keywords**: Extração de palavras-chave relevantes
- **Resume**: Resumos concisos de documentos
- **Names**: Identificação de pessoas e autores citados
- **Publisher**: Identificação de editoras e fontes

### API REST e Endpoints

#### Estrutura da API (`src/routes/routes.py`)

**Endpoints principais**:
- `GET /api/v1/health` - Status do sistema
- `GET /api/v1/dataset` - Listagem de datasets disponíveis
- `GET /api/v1/corpus` - Listagem do corpus gerado
- `POST /api/v1/corpus/generate` - Geração assíncrona de corpus

**Endpoints planejados** (comentados):
- `/api/v1/catalog/search` - Busca no catálogo
- `/api/v1/catalog/indexer` - Indexação de documentos
- `/api/v1/completions` - Chat completions
- `/api/v1/completions/history` - Histórico de conversas

### Geração e Análise de Corpus

#### Sistema de Corpus (`src/modules/corpus/corpus.py`)

**Processamento multithread**:
```python
def doc_with_articles(path: str, page_init: int = 1, page_final: int = -1):
    doc_info = DocService.info(path)
    doc_file = DocService.pdf_content(doc['path'], page_init, page_final)
    doc['articles'] = Legislation.split_into_articles(doc_file)
    return doc
```

**Features do sistema de corpus**:
- **Extração automática de artigos**: Regex pattern matching para estrutura legal
- **Anotação inteligente**: LLM auxilia na categorização e resumo
- **Processamento assíncrono**: ThreadPoolExecutor para performance
- **Controle de progresso**: Shared memory counters para tracking
- **Exportação CSV**: Formato estruturado para análise posterior

### Sistema de Catálogação

#### Módulo de Catálogo (`src/modules/catalog/`)

**Classe Catalog** (`catalog.py`):
```python
@dataclass
class Catalog:
    id: int = 0
    path: str = ""
    name: str = ""
    size: int = 0
    pages: int = 1
    mimetype: str = ""
    title: str = ""
    resume: str = ""
    categories: str = ""
```

**Funcionalidades**:
- **Indexação automática**: Metadados extraídos automaticamente
- **Categorização**: Classificação por área jurídica
- **Busca semântica**: Integração com ChromaDB
- **Repositório de dados**: Persistência e recuperação otimizada

## 📊 Stack Tecnológico Detalhado

### Core Framework
- **Flask 3.0.3**: Framework web Python com suporte assíncrono
- **Python 3.9+**: Linguagem base com type hints

### Processamento de Documentos
- **pdfplumber 0.11.1**: Extração precisa de texto de PDFs
- **PDFMiner.six**: Parser avançado de estrutura PDF
- **PyPDF2 3.0.1**: Manipulação de metadados PDF

### Machine Learning & NLP
- **scikit-learn 1.5.0**: Classificação e vetorização
- **spaCy 3.7.5**: Processamento de linguagem natural
- **NLTK 3.8.1**: Toolkit de processamento linguístico
- **transformers** (via Ollama): Modelos transformer

### Banco de Dados
- **ChromaDB 0.5.3**: Banco vetorial com HNSW indexing
- **SQLite**: Banco relacional para metadados
- **chroma-hnswlib 0.7.3**: Otimização de indexação

### Integração LLM
- **ollama 0.3.3**: Cliente para modelos locais
- **openai 1.10.0**: Cliente oficial OpenAI
- **httpx 0.27.0**: Cliente HTTP assíncrono

### Utilitários e Suporte
- **asyncio**: Programação assíncrona nativa
- **joblib 1.4.2**: Serialização de modelos ML
- **tqdm 4.66.2**: Barras de progresso
- **python-dotenv 1.0.1**: Configuração via variáveis de ambiente

## 🗂️ Estrutura de Diretórios

```
sibila/
├── src/                    # Código fonte principal
│   ├── config/            # Configurações (Ollama, OpenAI)
│   ├── models/            # Integrações com LLMs
│   ├── modules/           # Módulos funcionais
│   │   ├── analysis/      # Análise jurídica
│   │   ├── catalog/       # Sistema de catalogação
│   │   ├── corpus/        # Geração de corpus
│   │   ├── database/      # Bancos de dados
│   │   ├── document/      # Processamento de documentos
│   │   ├── nlp/          # Processamento de linguagem
│   │   ├── prompts/      # Sistema de prompts
│   │   ├── response/     # Formatação de respostas
│   │   └── viz/          # Visualizações
│   ├── routes/           # Endpoints da API
│   ├── routines/         # Rotinas de migração
│   ├── utils/            # Utilitários diversos
│   └── server.py         # Configuração Flask
├── dataset/              # Dados de treinamento
│   ├── sources/         # Documentos fonte (PDFs)
│   ├── corpus/          # Corpus processado (CSV)
│   └── _library/        # Biblioteca de referência
├── data/                # Persistência de dados
│   └── .chromadb/       # Banco vetorial ChromaDB
├── tests/               # Testes automatizados
└── main.py             # Ponto de entrada da aplicação
```

## 🔄 Fluxo de Dados do Sistema

### 1. **Ingestão de Documentos**
```
PDF Input → pdfplumber → Text Extraction → Metadata Generation → SQLite Storage
```

### 2. **Processamento de Corpus**
```
Legal Documents → Article Splitting → LLM Annotation → ChromaDB Indexing → CSV Export
```

### 3. **Pipeline RAG**
```
User Query → Embedding Generation → Vector Search → Context Retrieval → LLM Completion → Structured Response
```

### 4. **Análise Jurídica**
```
Legal Text → Category Classification → Normative Type → Efficacy Analysis → Structured Metadata
```

## ⚙️ Configuração Avançada

### Variáveis de Ambiente (.env)
```bash
OPENAI_API_KEY=        # Chave API OpenAI (opcional)
OLLAMA_PROXY_URL=      # URL proxy Ollama (opcional)
```

### Parâmetros do Modelo Ollama
```python
temperature = 0.5                    # Controle de aleatoriedade (0.0-1.0)
max_tokens = 4096                   # Limite de tokens de saída
context = 2048                      # Janela de contexto
diffusion_of_hallucination = 0.8   # Anti-alucinação (0.0-1.0)
diversification_rate = 0.0         # Taxa de diversificação
penalty_rate = 1.1                 # Penalização de repetição
```

## 🎯 Casos de Uso Específicos

### 1. **Análise de Legislação**
- Processamento automático da Constituição Federal
- Extração de artigos e incisos
- Categorização por área jurídica
- Geração de resumos e palavras-chave

### 2. **Busca Semântica em Documentos**
- Consultas em linguagem natural
- Recuperação baseada em similaridade
- Citação automática de fontes
- Ranking de relevância

### 3. **Assistente Jurídico IA**
- Respostas baseadas apenas em documentos
- Prevenção de alucinações
- Formato de resposta estruturado
- Rastreabilidade de fontes

## 🚀 Roadmap e Funcionalidades Planejadas

### Implementadas ✅
- [x] Pipeline completo de processamento de PDF
- [x] Integração dual LLM (Ollama + OpenAI)
- [x] Sistema de corpus jurídico
- [x] Banco vetorial ChromaDB
- [x] API REST básica
- [x] Sistema de classificação NLP
- [x] Análise de documentos legais

### Em Desenvolvimento 🔄
- [ ] Endpoints de busca e completions
- [ ] Interface web frontend
- [ ] Sistema de cache inteligente
- [ ] Métricas de performance
- [ ] Testes automatizados

### Planejado 📋
- [ ] Suporte a múltiplos formatos (DOCX, TXT)
- [ ] Sistema de usuários e permissões
- [ ] Dashboard de analytics
- [ ] Deployment containerizado
- [ ] CI/CD pipeline

## 🎓 Conceitos Técnicos Avançados

### RAG (Retrieval Augmented Generation)
O sistema implementa RAG através da combinação de:
- **Retrieval**: ChromaDB para busca vetorial
- **Augmentation**: Context injection nos prompts
- **Generation**: LLM (Ollama/OpenAI) para respostas

### Embeddings e Similaridade
- Vetorização de documentos usando modelos transformer
- Busca por similaridade cossenoidal
- Indexação HNSW para performance

### Anti-Alucinação
- Prompts restritivos: "baseado apenas no documento"
- Parâmetro `diffusion_of_hallucination`
- Validação de respostas contra fonte

Para inicializar o servidor em modo de desenvolvimento: `python main.py`  
Para desativar hot reload: `python main.py --no-reload`
