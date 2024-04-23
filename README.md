# Sibila (Profetisa)

As sibilas eram figuras da mitologia grega, mulheres proféticas que supostamente possuíam o dom da profecia e faziam previsões do futuro. Elas eram conhecidas por serem inspiradas pelos deuses e frequentemente consultadas para obter orientação divina.

Esse repositório é uma exemplo de aplicaçaão capaz de responder perguntas baseadas em documentos fornecidos pelo usuário.

## Estrutura de diretórios

- `./lexicon`: Possui um compilado dos verbetes da lingua portugesa

- `./bookcase`: Diretório usado para armazenar arquivos ou documentos de teste

- `./library`: Diretório usado para armazenar os livros no formato pdf. Somente conteúdo em pdf deve estar nesse diretório.

- `./docs`: Diretório usado para armazenar documentos gerais tendo como subdiretórios os formatos dos documentos.
Por exempo: para arquivos .txt, um diretótio `./docs/txt` deve ser usado, para arquivos .csv um diretório `./docs/csv` deve ser usado.

- `./data`: A pasta é a persistência dos bancos de dados usados no projeto

## Estrutura de containers

- `librarian`: Container para responder perguntas relacionados com os documentos informados
- `ollama`: LLM usada para fazer o embedding do texto. Acesso em <http://localhost:11434>
- `chatbot`: Um container da Lobe-chat foi usado apra poder conversar com ollama model. Acessso em <http://localhost:3210>

## Para Executar a aplicação

Tudo está sendo construido em docker, e `docker-compose` é o gerenciador para rodar tudo em desenvolvimento
```docker-compse up -d```

Consulta sobre os documentos via terminal: `docker compose exec librarian`
Consulta sobre os documentos via api: <http://localhost:2000>
Consulta sobre os documentos via chat: <http://localhost:3210>
Consulta ao modelo ollama via chat: <http://localhost:3210>

## Anotações

- LM Studio = interface web para conversar com  o LLM
- huging face: Tom jobbins
- wizard: vicuna 7B
- visualizer: <https://playground.tensorflow.org/#activation=tanh&batchSize=10&dataset=circle&regDataset=reg-plane&learningRate=0.03&regularizationRate=0&noise=0&networkShape=4,2&seed=0.19714&showTestData=false&discretize=false&percTrainData=50&x=true&y=true&xTimesY=false&xSquared=false&ySquared=false&cosX=false&sinX=false&cosY=false&sinY=false&collectStats=false&problem=classification&initZero=false&hideText=false>
- repositório de livros de tecnologia: <https://github.com/free-educa/books/blob/main/books/Design_Patterns.pdf>