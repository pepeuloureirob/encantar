# Encantar Cerimonial

Sistema web desenvolvido em Python com Flask para gerenciamento do **Encantar Cerimonial**.

## Funcionalidades

### Site Público

- Página Inicial
- Sobre Nós
- Serviços
- Eventos Já Realizados
- Feedback dos Clientes
- Solicitar Orçamento
- Botão flutuante do WhatsApp
- Botão do Instagram
- Botão Voltar ao Topo
- Layout Responsivo

### Painel Administrativo

- Login seguro
- Dashboard
- Cadastro de Eventos
- Edição de Eventos
- Exclusão de Eventos
- Upload de imagens
- Aprovação de Feedbacks
- Exclusão de Feedbacks
- Alteração do WhatsApp
- Alteração do Instagram
- Alteração dos textos do site
- Alteração das imagens do site
- Alteração da senha

---

# Tecnologias

- Python 3.12
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Gunicorn

---

# Estrutura

```
Encantar-Cerimonial/

app.py
requirements.txt
runtime.txt
Procfile
README.md

database/

instance/

static/
    css/
    js/
    imagens/
    uploads/

templates/

models/

utils/
```

---

# Instalação Local

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/encantar-cerimonial.git
```

Entre na pasta:

```bash
cd encantar-cerimonial
```

Crie um ambiente virtual:

Windows

```bash
python -m venv venv
```

Linux

```bash
python3 -m venv venv
```

Ative o ambiente.

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python app.py
```

O sistema estará disponível em

```
http://127.0.0.1:5000
```

---

# Banco de Dados

O banco SQLite será criado automaticamente na primeira execução.

Não é necessário criar tabelas manualmente.

---

# Login Inicial

Na primeira execução será criado automaticamente:

Administrador

```
admin
```

Senha

```
admin123
```

**Importante:** altere essa senha imediatamente após o primeiro login.

---

# Publicando no GitHub

Inicialize o Git:

```bash
git init
```

Adicione os arquivos:

```bash
git add .
```

Faça o commit:

```bash
git commit -m "Primeira versão"
```

Crie um repositório no GitHub e conecte:

```bash
git remote add origin https://github.com/SEU-USUARIO/encantar-cerimonial.git
```

Envie:

```bash
git branch -M main
git push -u origin main
```

---

# Publicando no Render

1. Crie uma conta no Render.

2. Clique em **New Web Service**.

3. Conecte ao GitHub.

4. Selecione o repositório.

5. Configure:

Build Command

```
pip install -r requirements.txt
```

Start Command

```
gunicorn app:app
```

Runtime

```
Python
```

---

# Variáveis de Ambiente

Crie:

```
SECRET_KEY
```

Exemplo

```
3e7ca9a0d19a0b3c9e8e5f3c4a19b8b76c2e
```

Também é possível configurar:

```
FLASK_ENV=production
```

---

# Atualizando o Sistema

Depois de alterar o código:

```bash
git add .
git commit -m "Atualização"
git push
```

O Render fará o deploy automaticamente.

---

# Segurança

- Senhas com hash
- Rotas protegidas
- Sessões seguras
- Upload seguro
- Proteção básica contra ataques comuns

---

# Licença

Uso exclusivo do Encantar Cerimonial.
