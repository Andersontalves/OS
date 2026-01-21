# 🚀 Guia Rápido de Instalação

Este guia vai te ajudar a rodar o sistema completo em sua máquina local.

## 📋 Pré-requisitos

- Python 3.10 ou superior
- PostgreSQL instalado (ou use SQLite para testes)
- (Opcional) Conta no Cloudinary
- (Opcional) Token do Bot Telegram

---

## 🔧 Passo 1: Backend API

### 1.1 Criar ambiente virtual

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 1.2 Instalar dependências

```bash
pip install -r requirements.txt
```

### 1.3 Configurar variáveis de ambiente

```bash
copy .env.example .env
```

Edite o arquivo `.env` e configure:

```env
# Para testes locais, use SQLite:
DATABASE_URL=sqlite:///./os_database.db

# Gere um secret aleatório:
JWT_SECRET=sua_chave_secreta_muito_longa_e_segura_aqui

# Deixe vazio por enquanto (teste sem upload de fotos):
CLOUDINARY_URL=
```

### 1.4 Inicializar banco de dados

```bash
python init_db.py
```

✅ Isso criará as tabelas e usuários padrão!

### 1.5 Executar o backend

```bash
python -m uvicorn app.main:app --reload
```

✅ Backend rodando em: http://localhost:8000
📖 Documentação: http://localhost:8000/docs

---

## 📱 Passo 2: Bot Telegram (Opcional)

### 2.1 Obter token do bot

1. Abra o Telegram
2. Procure por `@BotFather`
3. Envie `/newbot`
4. Siga as instruções
5. Copie o token fornecido

### 2.2 Configurar bot

```bash
cd telegram-bot
copy .env.example .env
```

Edite `.env`:

```env
TELEGRAM_BOT_TOKEN=seu_token_aqui
API_BASE_URL=http://localhost:8000
CLOUDINARY_URL=
```

### 2.3 Instalar dependências

```bash
pip install -r requirements.txt
```

### 2.4 Executar bot

```bash
python bot.py
```

✅ Bot rodando! Procure por ele no Telegram e envie `/start`

---

## 🌐 Passo 3: Frontend

### 3.1 Executar servidor HTTP

```bash
cd frontend
python -m http.server 8080
```

✅ Frontend rodando em: http://localhost:8080

### 3.2 Fazer login

Acesse http://localhost:8080 e use:

- **Username:** `admin`
- **Password:** `admin123`

---

## ✅ Verificação Rápida

### Teste 1: Dashboard
1. Faça login como `admin`
2. Você verá o dashboard (vazio por enquanto)

### Teste 2: Criar O.S via API
1. Acesse http://localhost:8000/docs
2. Clique em `POST /api/v1/auth/login`
3. Execute com:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
4. Copie o `access_token`
5. Clique em "Authorize" no topo da página
6. Cole o token
7. Agora teste criar uma O.S em `POST /api/v1/os`

### Teste 3: Bot Telegram (se configurado)
1. Abra o bot no Telegram
2. `/start`
3. `/abrir_os`
4. Siga as instruções

---

## 🐛 Problemas Comuns

### Erro de conexão com banco
- **Solução:** Use SQLite para testes: `DATABASE_URL=sqlite:///./os_database.db`

### CORS error no frontend
- **Solução:** Use `python -m http.server` ao invés de abrir o arquivo direto

### Bot não responde
- **Solução:** Verifique se o token está correto no `.env`

### API retorna 500
- **Solução:** Verifique se rodou `python init_db.py`

---

## 📚 Próximos Passos

1. Criar conta no Cloudinary para upload de fotos
2. Configurar PostgreSQL para produção
3. Deploy no Railway e Vercel

Veja o arquivo `credentials_checklist.md` para detalhes!
