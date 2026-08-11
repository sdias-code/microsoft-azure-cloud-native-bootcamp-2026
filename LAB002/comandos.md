Autenticar no Azure
az login

Criar o Grupo de Recursos
az group create --name $RESOURCE_GROUP --location $LOCATION

Listar todos os Grupos de Recursos da sua conta em uma tabela:
az group list --output table


Criar o Azure Container Registry (ACR)
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

Visualizar acr criados dentro do seu grupo de recursos:
az acr list --resource-group $RESOURCE_GROUP --output table
az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP
az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query "loginServer" --output tsv

Build Local da Imagem:
docker build -t api-dotnet-fotos:v1 .
docker build -t ${IMAGE_NAME}:${TAG} .

Rodar o Container Localmente, obs. passar arquivo .env para dentro do container:
docker run -d -p 8080:80 \
  --name api-teste-local \
  -v "$(pwd)/.env:/app/.env" \
  api-dotnet-fotos:v1


Compilar e Enviar a Imagem via ACR (Sem Docker Local)
az acr build --registry $ACR_NAME --image ${IMAGE_NAME}:${TAG} .
az acr build --registry "meuacrnamecointainer" --image api-dotnet-fotos:v1 .

Autenticar o seu Docker local no ACR do Azure:
az acr login --name silviodiasmsappfotos

Compilar e Taguear a imagem localmente para o Azure:
docker build -t silviodiasmsappfotos.azurecr.io/api-dotnet-fotos:v1 .

Enviar a imagem pronta para o Azure (Push):
docker push silviodiasmsappfotos.azurecr.io/api-dotnet-fotos:v1

Criar o ambiente e rodar o container na Azure:
az containerapp up \
  --name "minha-api-net-fotos" \
  --resource-group "lab002-brazilsouth-dio-api-dotnet-fotos" \
  --location "brazilsouth" \
  --environment "meu-ambiente-api-fotos" \
  --image "silviodiasmsappfotos.azurecr.io/api-dotnet-fotos:v1" \
  --target-port 80 \
  --ingress external \
  --env-vars \
    AZURE_SQL_SERVER="enderecodoseubanco.database.windows.net" \
    AZURE_SQL_DATABASE="free-sql-db-3616982" \
    AZURE_SQL_USERNAME="sdiascode" \
    AZURE_SQL_PASSWORD='sua-senha-real-aqui' \
    AZURE_ACCOUNT_NAME="lab001sdiascode" \
    AZURE_CONTAINER_NAME="fotos"

Criar o Azure Container App
az extension add --name containerapp --upgrade

Registrar o provedor de recursos no Azure:
az provider register --namespace Microsoft.App

