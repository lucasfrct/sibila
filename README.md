# Sibila (Profetisa)

As sibilas eram figuras da mitologia grega, mulheres proféticas que supostamente possuíam o dom da profecia e faziam previsões do futuro. Elas eram conhecidas por serem inspiradas pelos deuses e frequentemente consultadas para obter orientação divina.
Esse repositório é uma exemplo de uma aplicaçaão capaz de responder perguntas baseadas em documentos escolhidos pelo usuário.

## Estrutura

### Diretório ./lexicon

Possui uma compilado dos verbetes da lingua portugesa

### Diretório ./library

Diretório usado para armazenar os livros no formato pdf

### Diretório ./docs

Diretório usado para armazenar documentos gerais tendo como subdiretórios os formatos dos documentos.
Por exempo: para arquivos .txt, um diretótio ./docs/txt deve ser usado, para arquivos .csv uma diretório ./docs/csv deve ser usado.

### Diretório ./data

A pasta './data' é a persistência dos bancos de dados usados no projeto


## Containers auxiliares

### ollama

a aplicaçao usa ollma para fazer o embedding do texto.

### Lobe-chat

Um container lobu-chat foi usado apra poder conversar com ollama model

## Para Executar a aplicação

tudo está sendo construido em docker, e docker-compose é o gerenciador para rodar tudo em desenvolvimento
``` docker-compse up -d```

## Consulta

### Consulta via terminal

-

### Consulta via chat

-

## Anotaçoões

LM Studio = interface web para conversar com  o LLM

huging face - Tom jobbins 

- wizard vicuna 7B

visualizer- <https://playground.tensorflow.org/#activation=tanh&batchSize=10&dataset=circle&regDataset=reg-plane&learningRate=0.03&regularizationRate=0&noise=0&networkShape=4,2&seed=0.19714&showTestData=false&discretize=false&percTrainData=50&x=true&y=true&xTimesY=false&xSquared=false&ySquared=false&cosX=false&sinX=false&cosY=false&sinY=false&collectStats=false&problem=classification&initZero=false&hideText=false>

<!-- https://github.com/free-educa/books/blob/main/books/Design_Patterns.pdf -->