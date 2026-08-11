# LAB002 — API de Fotos (Azure Blob Storage + SQL Server)

API REST em **ASP.NET Core 8** para gerenciar uma galeria de fotos na nuvem. As imagens são armazenadas no **Azure Blob Storage** e os metadados (título, descrição, data e URL) persistidos no **Azure SQL Server**.

Este projeto é a evolução em container do backend desenvolvido no **LAB001** (`api/`). O código-fonte completo está em `LAB001-v2/api/`.

## 🔧 Tecnologias

- **ASP.NET Core 8** (Minimal APIs)
- **Azure.Storage.Blobs** — upload, acesso e exclusão de imagens no Blob Storage
- **Azure.Identity** — autenticação gerenciada com `DefaultAzureCredential` (sem chaves hardcoded)
- **Microsoft.Data.SqlClient** — acesso ao Azure SQL Server
- **Docker** — containerização da API (imagem publicada no Azure Container Registry)

## 🧱 Arquitetura

```
        Frontend (React/Vite)
                │  HTTP
                ▼
         API (container) ──► Azure Blob Storage (imagens)
                │
                ▼
        Azure SQL Server (metadados)
```

**Fluxo de upload**: o frontend envia `multipart/form-data` (título + descrição + imagem) → a API salva a imagem em um container de blobs com nome aleatório → a URL resultante e os metadados são gravados no SQL Server → o registro é devolvido ao frontend.

## 📍 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/photos` | Lista todas as fotos (ordenadas por data de upload) |
| `GET` | `/api/photos/{id}` | Busca uma foto pelo id |
| `POST` | `/api/photos` | Publica uma foto (`multipart/form-data`: `titulo`, `descricao`, `imagem`) |
| `PUT` | `/api/photos/{id}` | Atualiza título e descrição |
| `DELETE` | `/api/photos/{id}` | Exclui a foto (registro no banco + blob no storage) |

Regras de validação:

- `titulo` e `imagem` são obrigatórios.
- A imagem deve ter no máximo **1 MB** (formato `png`/`jpg`/`jpeg`).
- Blobs são criados com acesso privado; a URL é exposta por conveniência do lab.

## ⚙️ Configuração

As variáveis de ambiente controlam a conexão com os serviços da Azure. No container elas são injetadas pelo **Azure Container App** (ver `help.md`):

| Variável | Descrição |
|---|---|
| `AZURE_ACCOUNT_NAME` | Nome da conta de armazenamento (Blob) |
| `AZURE_CONTAINER_NAME` | Container de blobs (padrão: `fotos`) |
| `AZURE_SQL_SERVER` | Servidor SQL (`*.database.windows.net`) |
| `AZURE_SQL_DATABASE` | Banco de dados |
| `AZURE_SQL_USERNAME` | Usuário (autenticação SQL) |
| `AZURE_SQL_PASSWORD` | Senha (injetada como secret) |

## 🚀 Execução local

```bash
cd LAB001-v2/api
cp .env.example .env   # preencha com seus dados da Azure
dotnet run             # API em http://localhost:5080
```

Requisições de teste: arquivo `Api.http` (REST Client no VS Code).

## 🐳 Execução em container (Azure)

Imagem publicada e gerenciada via **Azure Container Registry** + **Azure Container Apps**. O passo a passo completo está em [`help.md`](./help.md).

1. Build: `docker build -t meuacr.azurecr.io/api-fotos:v1 .`
2. Push: `az acr login` → `docker push` (Repo: `api-fotos`)
3. Deploy: `az containerapp create` (porta 80, ingress externo, identidade gerenciada + secrets)
4. Acessar: `https://<nome-capp>.<regiao>.azurecontainerapps.io/api/photos`

## 📁 Estrutura

```
LAB001-v2/api/
├── Program.cs                    # Configuração e endpoints (Minimal API)
├── Api.csproj                    # Dependências NuGet
├── Dockerfile                    # Imagem multi-stage .NET 8
├── .dockerignore
├── .env.example
├── Models/Photo.cs               # Entidade Photo + DTO de atualização
├── Services/
│   ├── BlobStorageService.cs     # Upload/exclusão de blobs (DefaultAzureCredential)
│   └── SqlPhotoRepository.cs     # CRUD no Azure SQL Server
└── Properties/launchSettings.json
```

## 📌 Observações

- **Autenticação**: o Blob Storage usa `DefaultAzureCredential`, logo o Container App precisa de uma **identidade gerenciada** com a role `Storage Blob Data Contributor` (ver `help.md`). O SQL usa autenticação nativa via usuário/senha.
- **CORS**: liberado apenas para `http://localhost:5173` (frontend Vite local). Se consumir de outro host, ajuste a política em `Program.cs`.
- Projeto do bootcamp **Microsoft Azure Cloud Native (DIO)** — LAB002.

## 🖼️ Evidências

![Grupo de recursos](./img/grupo%20de%20recursos.png)

![Grupo lab002](./img/grupo%20lab002.png)

![Acesso à API via Postman](./img/acesso%20api%20via%20postman.png)