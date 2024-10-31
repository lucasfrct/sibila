# Sibila Sínica (Profetisa)

As sibilas eram figuras da mitologia grega, mulheres proféticas que supostamente possuíam o dom da profecia e faziam previsões do futuro. Elas eram conhecidas por serem inspiradas pelos deuses e frequentemente consultadas para obter orientação divina.

Esse repositório é um exemplo de aplicaçaão capaz de responder perguntas baseadas em documentos fornecidos pelo usuário.

## Estrutura de diretórios

- `./data`: A pasta é a persistência dos bancos de dados usados no projeto
- `./dataset`: A pasta com os arquivos de treinamento do modelo e inicialização do banco de dados

## Estrutura de containers

- `ollama`: A LLM é o llama do facebook. Acesso em <http://localhost:11434>
- `chatbot`: Um container da Lobe-chat foi usado apra poder conversar com ollama model. Acessso em <http://localhost:3210>

## Para Executar a aplicação

Tudo está sendo construido em docker, e `docker-compose` é o gerenciador para rodar tudo em desenvolvimento
```docker-compse up -d```

``` pip freeze > requirements.txt ```

- Consulta ao modelo ollama via chat: <http://localhost:3210>
  

## Anotações

- C# Ollama <https://github.com/awaescher/OllamaSharp>
- calssificador: <https://medium.com/@andsouit/classificador-de-inten%C3%A7%C3%A3o-com-o-tensorflow-f7fbc854f643>
- chromadb Admin: <https://github.com/flanker/chromadb-admin>
- LM Studio = interface web para conversar com  o LLM
- huging face: Tom jobbins
- wizard: vicuna 7B
- visualizer: <https://playground.tensorflow.org/#activation=tanh&batchSize=10&dataset=circle&regDataset=reg-plane&learningRate=0.03&regularizationRate=0&noise=0&networkShape=4,2&seed=0.19714&showTestData=false&discretize=false&percTrainData=50&x=true&y=true&xTimesY=false&xSquared=false&ySquared=false&cosX=false&sinX=false&cosY=false&sinY=false&collectStats=false&problem=classification&initZero=false&hideText=false>
- repositório de livros de tecnologia: <https://github.com/free-educa/books/blob/main/books/Design_Patterns.pdf>