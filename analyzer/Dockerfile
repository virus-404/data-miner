FROM mcr.microsoft.com/dotnet/aspnet:5.0
COPY bin/Release/net5.0/publish/ analyzer/
WORKDIR /analyzer
ENTRYPOINT ["dotnet", "NetCore.Docker.dll"]