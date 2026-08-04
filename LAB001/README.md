# 📸 Galeria de Fotos — Azure Cloud Native (LAB001)

Aplicação **Python + Streamlit** para upload e gerenciamento de imagens na nuvem **Microsoft Azure**. As imagens são armazenadas no **Azure Blob Storage** (com autenticação via **RBAC / `az login`**) e os metadados (título, descrição e URL da imagem) são persistidos no **Azure SQL Database**.

O sistema permite **cadastrar**, **editar**, **excluir** (com confirmação) e **listar** fotos em uma galeria responsiva (desktop, tablet e celular).

---

## 📌 Funcionalidades

- ✅ Upload de imagem para o **Azure Blob Storage** (autenticação via CLI/RBAC, sem chaves)
- ✅ Criação automática do container `fotos`
- ✅ Limite de **1 MB** por arquivo
- ✅ Registro dos metadados no **Azure SQL Database** (`dbo.Fotos`)
- ✅ Listagem das fotos em galeria **responsiva** (4 colunas desktop, 2 tablet, 1 celular)
- ✅ **Edição** de título e descrição
- ✅ **Exclusão** com confirmação do usuário
- ✅ Validações e logs detalhados no console

---

## 🧱 Tecnologias Utilizadas

| Camada            | Tecnologia                                                        |
|-------------------|-------------------------------------------------------------------|
| Linguagem         | Python 3.12                                                       |
| Interface Web     | Streamlit 1.60                                                    |
| Armazenamento     | Azure Blob Storage (RBAC / `az login`)                            |
| Banco de Dados    | Azure SQL Database (SQL Server)                                   |
| Driver de Banco   | pymssql (FreeTDS, sem necessidade de driver ODBC)                 |
| Autenticação      | Azure CLI (`DefaultAzureCredential`)                              |
| Gerenciamento de  | python-dotenv                                                      |
| Dependências      | requirements.txt                                                   |

---

## 📁 Estrutura do Projeto

```
LAB001/
├── app.py              # Orquestração principal da aplicação Streamlit
├── config.py           # Variáveis de ambiente, constantes e logging
├── database.py         # Conexão e operações CRUD no Azure SQL
├── storage.py          # Upload de imagens para o Blob Storage
├── ui.py               # Componentes de interface e CSS da galeria
├── query1.md           # Script SQL para criação da tabela Fotos
├── requirements.txt    # Dependências do projeto
├── .env.example        # Modelo de variáveis de ambiente
└── screen/             # Screenshots do sistema em funcionamento
```

---

## ⚙️ Pré-requisitos

- Conta **Microsoft Azure** com acesso ao portal
- **Azure CLI** instalado e autenticado
- Python 3.10+
- Recursos criados no Azure:
  - **Storage Account** (com RBAC)
  - **Azure SQL Database** (com autenticação SQL nativa)

---

## 🚀 Como Executar

### 1. Clone o repositório e acesse o diretório

```bash
git clone https://github.com/sdias-code/microsoft-azure-cloud-native-bootcamp-2026
cd SEU_REPOSITORIO/LAB001
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o `.env.example` para `.env` e preencha com seus dados:

```bash
cp .env.example .env
```

```env
# Azure Storage - Sem Chaves, usando seu 'az login'
AZURE_ACCOUNT_NAME="seu-account-name"
AZURE_CONTAINER_NAME="fotos"

# Azure SQL Server - Autenticação SQL nativa
AZURE_SQL_SERVER="seu-servidor.database.windows.net"
AZURE_SQL_DATABASE="seu-banco"
AZURE_SQL_USERNAME="seu-usuario"
AZURE_SQL_PASSWORD="sua-senha"
```

> ⚠️ **Nunca suba o arquivo `.env` para o GitHub** — ele contém credenciais. Mantenha-o no `.gitignore`.

### 5. Autentique-se no Azure

```bash
az login
```

O `DefaultAzureCredential` usará a sessão do `az login` para autenticar o acesso ao Blob Storage (RBAC). Apenas a conexão com o banco de dados usa as credenciais do `.env`.

### 6. Crie a tabela no banco de dados

Execute o script `query1.md` (ou o SQL abaixo) no **Query Editor** do Azure SQL:

```sql
IF OBJECT_ID('dbo.Fotos', 'U') IS NOT NULL
    DROP TABLE dbo.Fotos;

CREATE TABLE dbo.Fotos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titulo NVARCHAR(200) NOT NULL,
    descricao NVARCHAR(MAX) NOT NULL,
    data_upload DATETIME NOT NULL DEFAULT GETDATE(),
    imagem_url NVARCHAR(500) NOT NULL
);
```

### 7. Execute a aplicação

```bash
streamlit run app.py
```

Acesse no navegador: **http://localhost:8501**

---

## ☁️ Acesso ao Portal Azure

1. Acesse [https://portal.azure.com](https://portal.azure.com)
2. **Storage accounts** → sua conta → seção **Containers** → container `fotos`
3. **SQL databases** → seu banco → **Query editor** para consultar/gerenciar a tabela `dbo.Fotos`

Para consultar os dados da tabela:

```sql
SELECT * FROM dbo.Fotos ORDER BY data_upload DESC;
```

---

## 🖼️ Diagrama de Funcionamento

```
┌──────────────┐     1. Upload      ┌────────────────────┐
│   Usuário    │ ─────────────────► │ Streamlit (app.py) │
│  (Navegador) │                     └────────┬───────────┘
└──────────────┘                              │
                                              │
                    2. Autenticação via az login / DefaultAzureCredential
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │  Azure Blob Storage     │
                                 │  (container "fotos")    │
                                 └─────────────────────────┘
                                              │
                                              │ 3. Gera URL da imagem
                                              ▼
                                 ┌─────────────────────────┐
                                 │  Azure SQL Database      │
                                 │  (tabela dbo.Fotos)     │
                                 └─────────────────────────┘
                                              │
                                              │ 4. SELECT / UPDATE / DELETE
                                              ▼
                                        Galeria exibida
                                        ao usuário
```

**Fluxo do upload:**
1. O usuário preenche título, descrição e seleciona a imagem (máx. 1 MB)
2. O app autentica via `az login` (RBAC) e faz upload do arquivo para o Blob Storage
3. O app gera a URL única do blob e insere os metadados na tabela `dbo.Fotos`
4. A galeria lista as fotos lendo o banco, exibindo título, descrição e imagem

---

## 🖥️ Screenshots do Sistema

> Screenshots disponíveis na pasta [`screen/`](screen/).

### Sistema de Upload de Fotos
![Sistema de upload de fotos](screen/sistema%20de%20upload%20de%20fotos.png)

### Galeria de Fotos
![Galeria de fotos](screen/galeria%20de%20fotos.png)

### Edição e Exclusão
![Edição e exclusão](screen/edicao%20e%20exclusao.png)

### Script SQL para criação da tabela
![Script SQL](screen/script%20sql.png)

### Consulta ao banco no Portal Azure
![Dados do banco](screen/dados%20do%20banco.png)

---

## 🤝 Contribuição

Sinta-se à vontade para abrir *issues* ou *pull requests* com melhorias, correções e novas funcionalidades.

## 📄 Licença

Este projeto é parte do bootcamp **Microsoft Azure Cloud Native 2026** da [DIO](https://www.dio.me/). Consulte a licença do repositório principal.
