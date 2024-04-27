# ## Dotnet para desenvolvimento

# ! ## Maquina para armazenar as dependencias
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS environment-c-sharp-dependences
WORKDIR /app

# Copy everything
COPY ./src ./

# RUN dotnet clean --configuration Release
RUN dotnet restore

# ! ## Maquina para excutar o build
FROM environment-c-sharp-dependences AS environment-c-sharp-build

ENV ASPNETCORE_URLS=http://*:5000
ENV ASPNETCORE_ENVIRONMENT=Production
ENV DOTNET_EnableDiagnostics=0

RUN dotnet publish -c Release -o dist

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS environment-c-sharp

WORKDIR /app

ENV ASPNETCORE_URLS=http://*:5000
ENV ASPNETCORE_ENVIRONMENT=Production
ENV DOTNET_EnableDiagnostics=0

COPY --from=environment-c-sharp-build /app/dist .

EXPOSE 5000

VOLUME /app

ENTRYPOINT ["dotnet", "SibilaApi.dll"]