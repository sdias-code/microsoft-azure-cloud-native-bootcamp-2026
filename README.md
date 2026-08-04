# Bootcamp Microsoft Azure Cloud Native — DIO

Este repositório centraliza todos os desafios de código, projetos práticos e laboratórios desenvolvidos durante o bootcamp **Microsoft Azure Cloud Native** da Digital Innovation One (DIO). O objetivo é construir e gerenciar soluções modernas, escaláveis e seguras utilizando os principais serviços da nuvem Microsoft Azure.

---

## 🚀 Estrutura do Bootcamp & Projetos

O bootcamp é dividido em módulos estratégicos focados na arquitetura cloud-native:

- **Labs/Lab01 - Fundamentos da Plataforma Azure**
  - *Status:* ✅ Concluído
  - *Escopo:* Criação de Contas de Armazenamento (Storage Accounts), isolamento de segurança e integração com aplicação em Python (Streamlit) para upload e gerenciamento de imagens via Blob Storage.
  - *Funcionalidades:* Upload de imagens (máx. 1 MB) com autenticação via RBAC/`az login` (sem chaves), criação automática do container `fotos`, persistência dos metadados (título, descrição, URL) no **Azure SQL Database** (`dbo.Fotos`), galeria responsiva (desktop/tablet/celular), edição de título e descrição e exclusão com confirmação.
  - *Tecnologias:* Python 3.12, Streamlit 1.60, Azure Blob Storage, Azure SQL Database (pymssql), Azure CLI (`DefaultAzureCredential`), python-dotenv.
  - *Estrutura do projeto:* `app.py` (orquestração Streamlit), `config.py` (configuração/logging), `database.py` (CRUD no Azure SQL), `storage.py` (upload no Blob Storage), `ui.py` (interface/CSS), `query1.md` (script SQL da tabela) e `screen/` (screenshots).
  
- **Labs/Lab02 - Contêineres e Orquestração na Azure**
  - *Status:* ⏳ Aguardando
  - *Escopo:* Empacotamento de aplicações e orquestração de cargas de trabalho.

- **Labs/Lab03 - Desenvolvimento e Hospedagem de Aplicações Web com o Azure ML**
  - *Status:* ⏳ Aguardando
  - *Escopo:* Provisionamento de ambientes integrados para inteligência artificial e machine learning.

- **Labs/Lab05 - Gerenciamento e Segurança de APIs na Azure**
  - *Status:* ⏳ Aguardando
  - *Escopo:* Governança, monitoramento e exposição segura de serviços de backend.

- **Labs/Lab07 - Computação Serverless, IA e Aplicações Cloud-Native**
  - *Status:* ⏳ Aguardando
  - *Escopo:* Arquiteturas orientadas a eventos (Functions) e automações na nuvem.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

- **Cloud Platform:** Microsoft Azure (Blob Storage, CLI, RBAC)
- **Linguagem:** Python
- **Interface:** Streamlit
- **Ambiente Local:** Ubuntu 20.04 LTS

---

## 🔧 Como Executar o Ambiente Local (Exemplo Lab01)

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd SEU_REPOSITORIO
   ```

2. **Configure o Ambiente Virtual do Python:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Autentique-se na Azure:**
   ```bash
   az login
   ```

4. **Execute a aplicação:**
   ```bash
   streamlit run Labs/Lab01/app.py
   ```
