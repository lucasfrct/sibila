# Sibila Sínica

As sibilas eram figuras da mitologia inspiradas pelos deuses para profetizar.

Esse repositório é um exemplo de aplicação capaz de responder perguntas baseadas em documentos fornecidos pelo usuário.

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

A aplicação estará disponível em `http://localhost:5000`

### 📖 Guia Completo
Para instruções detalhadas, consulte: **[SETUP_LOCAL.md](./SETUP_LOCAL.md)**

## Estrutura de containers

- `ollama`: A LLM pode ser acessada em <http://localhost:11434>

### Para Executar a aplicação

Tudo está sendo construído em docker, e `docker-compose` é o gerenciador para rodar tudo em desenvolvimento

```docker-compose up -d```

### Ambiente de desenvolvimento

Para rodar a aplicação em desenvolvimento, basta rodar o comando abaixo

``` python ./main.py ```

Para rodar a aplicação sem hot reload, basta rodar o comando abaixo

``` python ./main.py --no-reload ```

### Estrutura de diretórios

- `./data`: A pasta é a persistência dos bancos de dados usados no projeto
- `./dataset`: A pasta com os arquivos de treinamento do modelo e inicialização do banco de dados

### LLM Llama 3

O Meta treinou o Llama 3 com uma contagem de tokens de mais de 15 trilhões de tokens.

O modelo 8B tem um limite de conhecimento de março de 2023.

O modelo 70B tem um limite de conhecimento de dezembro de 2023.

Os modelos usam Grouped-Query Attention (GQA).

SFT é uma técnica de treinamento que permite que o modelo seja treinado em um conjunto de dados de treinamento muito maior do que o que pode ser armazenado na memória de uma única GPU.

### Anotações

- classificador: <https://medium.com/@andsouit/classificador-de-inten%C3%A7%C3%A3o-com-o-tensorflow-f7fbc854f643>
- LM Studio = interface web para conversar com  o LLM
- Hugging Face: Tom Jobbins
- repositório de livros de tecnologia: <https://github.com/free-educa/books/blob/main/books/Design_Patterns.pdf>
