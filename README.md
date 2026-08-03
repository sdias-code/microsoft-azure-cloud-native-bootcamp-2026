# Bootcamp Microsoft Azure Cloud Native — DIO

Este repositório centraliza todos os desafios de código, projetos práticos e laboratórios desenvolvidos durante o bootcamp **Microsoft Azure Cloud Native** da Digital Innovation One (DIO). O objetivo é construir e gerenciar soluções modernas, escaláveis e seguras utilizando os principais serviços da nuvem Microsoft Azure.

---

## 🚀 Estrutura do Bootcamp & Projetos

O bootcamp é dividido em módulos estratégicos focados na arquitetura cloud-native:

- **Labs/Lab01 - Fundamentos da Plataforma Azure**
  - *Status:* 🛠️ Em desenvolvimento
  - *Escopo:* Criação de Contas de Armazenamento (Storage Accounts), isolamento de segurança e integração com aplicação em Python (Streamlit) para upload e gerenciamento de imagens via Blob Storage.
  
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
