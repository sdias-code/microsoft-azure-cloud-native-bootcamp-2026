# LAB002 — Help: Containerizar a API e publicar no Azure (ACR + Container Apps)

Passo a passo com comandos para Linux. Substitua os valores entre `<>` pelos seus (ex.: nome do ACR, resource group, etc.).

---

## 0. Pré-requisitos

- **Docker** instalado e em execução.
- **Azure CLI** instalado (`az`).
- A conta de armazenamento (Blob) e o Azure SQL já existentes do LAB001.
- Autenticar e definir a assinatura:

```bash
az login
az account set --subscription "<ID_DA_SUBSCRIPTION>"
az account show
```

---

## 1. Acessar a pasta da API

```bash
cd LAB001-v2/api
```

> O projeto já contém um `Dockerfile` e `.dockerignore`. O `.env` local **não é copiado** para a imagem: as variáveis serão injetadas no Container App.

---

## 2. Build da imagem Docker localmente

```bash
docker build -t <seu-login-azure>.azurecr.io/api-fotos:v1 .
```

> `<seu-login-azure>` será o nome do seu registry (precisa ser **único global**). Anote-o.

Valide a imagem localmente (opcional):

```bash
docker run --rm -p 5080:80 \
  --env AZURE_ACCOUNT_NAME="<account-name>" \
  --env AZURE_CONTAINER_NAME="fotos" \
  --env AZURE_SQL_SERVER="<servidor.database.windows.net>" \
  --env AZURE_SQL_DATABASE="<banco>" \
  --env AZURE_SQL_USERNAME="<usuario>" \
  --env AZURE_SQL_PASSWORD="<senha>" \
  <seu-login-azure>.azurecr.io/api-fotos:v1
```

Teste: `curl http://localhost:5080/api/photos`

---

## 3. Definir variáveis de ambiente do Azure CLI

```bash
RESOURCE_GROUP="Lab002-<nome-do-local-regiao>"   # ex.: Lab002-brazilsouth
LOCATION="brazilsouth"
ACR_NAME="<seu-login-azure>"
CONTAINERAPP_ENV="capp-env-fotos"
CONTAINERAPP_NAME="capp-api-fotos"
IMAGE="$ACR_NAME.azurecr.io/api-fotos:v1"
```

> O Resource Group seguirá o padrão **`Lab002-<nome-do-local-regiao>`** e concentrará **todos** os recursos deste laboratório: o **Azure Container Registry (imagens Docker)** e o **Container App** (e seu ambiente).

---

## 4. Criar o Resource Group (padrão Lab002-<região>) e o ACR

Este grupo abrigará o **Container Registry** (imagems Docker) e o **Container App**:

```bash
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

az acr create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$ACR_NAME" \
  --sku Basic \
  --location "$LOCATION"
```

---

## 5. Enviar (push) a imagem para o ACR

```bash
az acr login --name "$ACR_NAME"
docker tag <seu-login-azure>-api-fotos:v1 "$IMAGE"
docker push "$IMAGE"
```

Confirme a imagem no registry:

```bash
az acr repository show-tags --name "$ACR_NAME" --repository api-fotos --output table
```

> Alternativa (build direto no Azure, sem Docker local):
> ```bash
> az acr build --registry "$ACR_NAME" --image api-fotos:v1 .   # execute em LAB001-v2/api
> ```

---

## 6. Criar o ambiente do Container Apps

```bash
az extension add --name containerapp --allow-preview true

az containerapp env create \
  --name "$CONTAINERAPP_ENV" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION"
```

---

## 7. Criar identidade gerenciada e dar acesso ao Blob Storage

A API usa `DefaultAzureCredential`: no Container App ela precisa de uma identidade gerenciada com permissão no Blob Storage.

```bash
az identity create \
  --name "id-api-fotos" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION"

IDENTITY_ID=$(az identity show --name "id-api-fotos" \
  --resource-group "$RESOURCE_GROUP" \
  --query id --output tsv)

STORAGE_RESOURCE_ID=$(az storage account show \
  --name "<account-name>" \
  --query id --output tsv)

az role assignment create \
  --assignee "$IDENTITY_ID" \
  --role "Storage Blob Data Contributor" \
  --scope "$STORAGE_RESOURCE_ID"
```

---

## 8. Criar o Container App com as variáveis de ambiente

Crie as credenciais como **secrets** (senha do SQL) e injete as demais variáveis:

```bash
# Secrets
az containerapp create \
  --name "$CONTAINERAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$CONTAINERAPP_ENV" \
  --image "$IMAGE" \
  --ingress external \
  --target-port 80 \
  --min-replicas 1 \
  --max-replicas 1 \
  --secrets "azuresql-password=<SENHA_DO_SQL>" \
  --env-vars \
    "AZURE_ACCOUNT_NAME=<account-name>" \
    "AZURE_CONTAINER_NAME=fotos" \
    "AZURE_SQL_SERVER=<servidor.database.windows.net>" \
    "AZURE_SQL_DATABASE=<banco>" \
    "AZURE_SQL_USERNAME=<usuario>" \
    "AZURE_SQL_PASSWORD=secretref:azuresql-password" \
  --user-assigned "$IDENTITY_ID"
```

---

## 9. Conferir o deployment e a URL do app

```bash
az containerapp show \
  --name "$CONTAINERAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query "properties.configuration.ingress.fqdn" --output tsv
```

URL de acesso (HTTPS): `https://<capp-api-fotos>.<region>.azurecontainerapps.io`

Teste os endpoints:

```bash
URL=$(az containerapp show --name "$CONTAINERAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query "properties.configuration.ingress.fqdn" --output tsv)

curl -s "https://$URL/api/photos"
```

---

## 10. Atualizar imagem (nova versão) e monitorar

Nova versão do código:

```bash
docker build -t "$ACR_NAME.azurecr.io/api-fotos:v2" .   # em LAB001-v2/api
az acr login --name "$ACR_NAME"
docker push "$ACR_NAME.azurecr.io/api-fotos:v2"

az containerapp update \
  --name "$CONTAINERAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --image "$ACR_NAME.azurecr.io/api-fotos:v2"
```

Logs e restarts:

```bash
az containerapp logs show \
  --name "$CONTAINERAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --tail 50

az containerapp revision list \
  --name "$CONTAINERAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query "[].{Name:name, Active:active, Created:createdTime}" --output table
```

---

## 11. Limpeza (opcional — apaga tudo criado)

```bash
az containerapp delete --name "$CONTAINERAPP_NAME" --resource-group "$RESOURCE_GROUP" --yes
az acr delete --name "$ACR_NAME" --resource-group "$RESOURCE_GROUP" --yes
az group delete --name "$RESOURCE_GROUP" --yes
```

---

> **Importante:** a autenticação do Blob Storage usa `DefaultAzureCredential`. Se preferir autenticação com **connection string/access key**, altere o `BlobStorageService` para ler uma connection string (`AZURE_STORAGE_CONNECTION_STRING`) e injete-a como secret sem criar a identidade gerenciada.