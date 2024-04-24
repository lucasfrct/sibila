# ## GO lang para produção

# ! ## Maquina para armazenar as dependencias
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS environment-c-sharp-dependences
WORKDIR /app

# Copy everything
COPY ./src ./

# Restore as distinct layers
RUN dotnet restore

# ! ## Maquina para excutar o build
FROM environment-c-sharp-dependences AS environment-c-sharp-build
# Build and publish a release
RUN dotnet publish -c Release -o dist

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS environment-c-sharp
WORKDIR /app
COPY --from=environment-c-sharp-build /app/dist .
ENTRYPOINT ["dotnet", "SibilaApi.dll"]