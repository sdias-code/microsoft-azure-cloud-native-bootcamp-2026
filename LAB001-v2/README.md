# LAB001-v2 — Gerenciador de Fotos na Nuvem (Azure)

Aplicação full-stack composta por dois projetos. A **API** (`.NET 8`) publica uma galeria de fotos armazenadas no **Azure Blob Storage** com metadados no **Azure SQL Server**, e o **Frontend** (React + Vite) consome essa API para listar, publicar, editar e excluir fotos na nuvem.

## 📁 Estrutura do Projeto

```
LAB001-v2/
├── api/        # Backend — Web API em ASP.NET Core (.NET 8)
└── front/      # Frontend — Aplicação React (Vite)
```

---

## 1️⃣ api — Backend (.NET 8 Web API)

API REST para gerenciamento de fotos na nuvem.

### Tecnologias
- **ASP.NET Core 8** (Minimal APIs)
- **Azure.Storage.Blobs** — upload/remoção de imagens no **Azure Blob Storage**
- **Azure.Identity** — autenticação via `DefaultAzureCredential` (usa seu `az login`, sem chaves)
- **Microsoft.Data.SqlClient** — persistência de metadados no **Azure SQL Server**
- **DotNetEnv** — leitura de variáveis de ambiente a partir do arquivo `.env`

### Endpoints

| Método   | Rota                  | Descrição                                  |
|----------|-----------------------|--------------------------------------------|
| `GET`    | `/api/photos`         | Lista todas as fotos                       |
| `GET`    | `/api/photos/{id}`    | Busca uma foto pelo id                     |
| `POST`   | `/api/photos`         | Cria uma foto (multipart/form-data)        |
| `PUT`    | `/api/photos/{id}`    | Atualiza título e descrição                |
| `DELETE` | `/api/photos/{id}`    | Exclui a foto (registro + blob)            |

O upload aceita imagens `png`/`jpeg` de até **1 MB** e salva o arquivo no Blob Storage com um nome aleatório; a URL retornada é armazenada no banco.

### Configuração do ambiente

1. Autentique-se na Azure:
   ```bash
   az login
   ```
2. Crie a conta de **Armazenamento** (Blob) e o **Azure SQL Server** + banco.
3. Copie `.env.example` para `.env` e preencha os valores:
   ```bash
   cp .env.example .env
   ```
4. Configure as variáveis em `api/.env`:

   | Variável                | Descrição                                        |
   |-------------------------|--------------------------------------------------|
   | `AZURE_ACCOUNT_NAME`    | Nome da conta de armazenamento (blob)            |
   | `AZURE_CONTAINER_NAME`  | Nome do container de blobs (padrão: `fotos`)    |
   | `AZURE_SQL_SERVER`      | Servidor SQL (ex.: `servidor.database.windows.net`) |
   | `AZURE_SQL_DATABASE`    | Nome do banco de dados                           |
   | `AZURE_SQL_USERNAME`    | Usuário do banco (autenticação SQL)              |
   | `AZURE_SQL_PASSWORD`    | Senha do banco                                   |

   > ⚠️ O `.env` **não deve ser versionado** — mantenha-o fora do Git.

5. No banco, crie a tabela usada pela API:
   ```sql
   CREATE TABLE dbo.Fotos (
       id          INT IDENTITY(1,1) PRIMARY KEY,
       titulo      NVARCHAR(200) NOT NULL,
       descricao   NVARCHAR(1000) NULL,
       data_upload DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
       imagem_url  NVARCHAR(500) NOT NULL
   );
   ```

### Como executar

Pré-requisito: **.NET 8 SDK**.

```bash
cd api
dotnet run
```

A API será publicada em `http://localhost:5080`. Você também pode testar os endpoints com o arquivo `Api.http` (ex.: via REST Client no VS Code).

---

## 2️⃣ front — Frontend (React + Vite)

Interface web para acessar a galeria de fotos da API.

### Tecnologias
- **React 18** + **Vite 5**
- **ESLint** para padronização do código

### Funcionalidades
- 📤 **Publicar foto**: envia título, descrição e imagem (até 1 MB)
- 🖼️ **Galeria**: lista as fotos armazenadas na nuvem
- ✏️ **Editar**: altera título e descrição
- 🗑️ **Excluir**: remove a foto com confirmação

O frontend roda em `http://localhost:5173` e o Vite faz proxy das requisições `/api` para `http://localhost:5080` (configurado em `vite.config.js`).

### Como executar

Pré-requisito: **Node.js** (versão 18 ou superior).

```bash
cd front
npm install
npm run dev
```

Abra `http://localhost:5173` no navegador.

---

## 🚀 Como acessar o sistema completo

1. Suba e autentique os serviços da Azure (Blob Storage + SQL Server) e configure o `api/.env`.
2. Inicie a API (terminal 1):
   ```bash
   cd api && dotnet run
   ```
3. Inicie o frontend (terminal 2):
   ```bash
   cd front && npm run dev
   ```
4. Acesse **http://localhost:5173** e gerencie suas fotos na nuvem.

---

## 🛠️ Scripts úteis

### API (`api/`)
| Comando       | Descrição            |
|---------------|----------------------|
| `dotnet run`  | Executa a API        |

### Front (`front/`)
| Comando            | Descrição                         |
|--------------------|-----------------------------------|
| `npm run dev`      | Ambiente de desenvolvimento       |
| `npm run build`    | Gera o build de produção (em `dist/`) |
| `npm run preview`  | Previews o build de produção      |
| `npm run lint`     | Roda o ESLint                     |

---

## 📌 Observações

- A autenticação no Blob Storage usa `DefaultAzureCredential`, então se preferir não usar `az login`, ajuste o `BlobStorageService` para um método alternativo (ex.: chave de acesso via connection string).
- Projeto desenvolvido como laboratório do bootcamp **Microsoft Azure Cloud Native (DIO)**.