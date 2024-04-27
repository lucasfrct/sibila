## é preciso dotnet 8 para ese aplaicaçao
dotnet --info

## Para craira  aplicaço
dotnet new webapi --use-controllers -o SibilaApi

# pacotes
dotnet add package Microsoft.EntityFrameworkCore.InMemory
dotnet dev-certs https --trus

## Executando a aplicação
# dotnet run --launch-profile https
dotnet watch run -v

## swagger
/swagger/index.html

## Publicando a apalicação
dotnet publish -c Release