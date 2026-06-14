<h1 align="center">
🤖 SmartFlow WhatsApp AI
</h1>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=28&duration=3000&color=8A2BE2&center=true&vCenter=true&width=1000&lines=Plataforma+SaaS+para+Chatbots+Inteligentes;WhatsApp+Automation+%7C+AI+%7C+RAG;FastAPI+%7C+Flask+%7C+Python;IA+Multimodal+com+Texto+e+%C3%81udio" />
</p>

<p align="center">
  Plataforma SaaS escalável para automação inteligente de atendimento via WhatsApp.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-prot%C3%B3tipo%20funcional-yellow?style=for-the-badge">

  <img src="https://img.shields.io/badge/backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">

  <img src="https://img.shields.io/badge/interface-Flask-black?style=for-the-badge&logo=flask">

  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python">

  <img src="https://img.shields.io/badge/AI-Multimodal-purple?style=for-the-badge">

  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge">
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,fastapi,flask,postgres,docker,git,vscode&theme=dark" />
</p>

---

# 🚀 Sobre o Projeto

O **SmartFlow WhatsApp AI** é uma plataforma SaaS desenvolvida para gerenciamento inteligente de chatbots no WhatsApp.

A arquitetura foi projetada para ser:

- ⚡ Escalável
- 🧩 Modular
- 🔄 Flexível
- 🗂️ Multi-instância
- 🧠 Integrável com modelos modernos de IA

A plataforma suporta processamento multimodal, incluindo:

- 💬 Texto
- 🎤 Áudio
- 🖼️ Imagens
- 🔎 RAG (Retrieval-Augmented Generation)

---

# 🧠 Principais Recursos

## ⚡ Automação Inteligente
- Processamento automático de mensagens
- Fluxos de atendimento personalizados
- Respostas contextuais com IA

---

## 🎙️ IA Multimodal
- Transcrição de áudio
- Processamento de imagens
- Integração com múltiplos modelos LLM

---

## 🧩 Arquitetura Modular
- Serviços desacoplados
- Fácil manutenção
- Escalabilidade simplificada

---

## 🗂️ Multi-instâncias

Cada instância possui:

- Prompts próprios
- Configurações independentes
- Leads separados
- Contexto individualizado

---

## 🔎 RAG + Vector Store
- Busca contextual avançada
- Recuperação inteligente de informações
- Integração com banco vetorial

---

# 🛠️ Tecnologias Utilizadas

## 🔧 Backend

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,fastapi,flask&theme=dark" />
</p>

---

## 🧠 Inteligência Artificial

<p align="center">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white">

  <img src="https://img.shields.io/badge/Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white">

  <img src="https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black">
</p>

---

## 🗄️ Banco de Dados

<p align="center">
  <img src="https://skillicons.dev/icons?i=postgres&theme=dark" />
</p>

---

## ⚙️ Ferramentas e DevOps

<p align="center">
  <img src="https://skillicons.dev/icons?i=docker,git,github,vscode&theme=dark" />
</p>

---

# 📂 Estrutura do Projeto

```bash
SmartFlow-WhatsApp-AI/
│
├── app/                 # Backend FastAPI e serviços de IA
├── interface/           # Painel administrativo Flask
├── app/service/         # Processadores, LLMs e vector store
├── app/routers/         # Rotas e webhooks
├── pyproject.toml       # Dependências do projeto
└── .env                 # Variáveis de ambiente
```

---

# ⚙️ Funcionalidades

- ✅ Recebimento de webhooks do WhatsApp
- ✅ Processamento assíncrono de mensagens
- ✅ Gerenciamento de múltiplas IAs
- ✅ Integração com LLMs
- ✅ Suporte a áudio
- ✅ Suporte a imagens
- ✅ Sistema RAG
- ✅ Painel administrativo
- 🚧 Expansão para novos providers de IA

---

# 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/smartflow

FERNET_KEY=<sua-chave>

OPENAI_API_KEY=
GEMINI_API_KEY=
HUGGINGFACE_API_TOKEN=
```

---

# 🛠️ Instalação

## 1️⃣ Criar ambiente virtual

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## 2️⃣ Instalar dependências

### Poetry

```bash
poetry install
```

### Pip

```bash
pip install -r interface/requirements.txt
```

---

# ▶️ Executando o Projeto

## 🚀 Backend

```bash
uvicorn app.main:app --reload
```

---

## 🖥️ Painel Flask

```bash
python interface/app.py
```

---

# 🧩 Arquitetura

```text
WhatsApp
   ↓
Webhook
   ↓
FastAPI
   ↓
IA / LLM
   ↓
Vector Store (RAG)
   ↓
Resposta Automatizada
```

---

# 📌 Status do Projeto

🚧 **Protótipo funcional em evolução**

Novas funcionalidades estão sendo desenvolvidas continuamente.

---

# 📄 Licença

Distribuído sob licença MIT.

---

<p align="center">
  Solução escalável para automação inteligente via WhatsApp.
</p>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:111111,100:00ADB5&height=120&section=footer"/>
