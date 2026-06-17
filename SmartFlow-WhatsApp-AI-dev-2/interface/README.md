# Projeto Flask Básico

Projeto de ChatBot com interface para gerenciar suas IAS

---

## Pré-requisitos

- **Python** (3.6+ recomendado)
- **pip** (gerenciador de pacotes do Python)

---

## Instalação

1. **Clonar este repositório**:

   ```bash
   git clone https://github.com/matt-gama/chatbot-interface-curso.git
   cd chatbot-interface-curso
   ```

2. **Criar e ativar ambiente virtual**:

   No **Linux/Mac**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   No **Windows**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

```env
DATABASE_URL=
FERNET_KEY=
```

- **DATABASE_URL**: URL de conexão com o banco de dados (ex.: `postgresql://usuario:senha@localhost:5432/meubanco`)
- **FERNET_KEY**: Chave utilizada para criptografia (você pode gerar uma chave usando a biblioteca `cryptography`)

---

## Executando a aplicação

Após instalar as dependências e configurar o arquivo `.env`, basta executar:

```bash
python app/app.py
```

Isso iniciará o servidor Flask em modo de desenvolvimento. Para acessar a aplicação, abra o navegador em [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Observações

- Se desejar parar de usar o ambiente virtual, basta **desativá-lo**:
  - Linux/Mac: `deactivate`
  - Windows: `deactivate`
- Certifique-se de não versionar o arquivo `.env` (adicione-o ao seu `.gitignore` para evitar o vazamento de credenciais).

