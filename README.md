# Sistema de Ordens de Serviço

Sistema integrado para gestão de ordens de serviço técnico em campo, com bot Telegram para abertura e painel web para execução e monitoramento.

## 📋 Estrutura do Projeto

```
os-sistema/
├── backend/          # API FastAPI + PostgreSQL
├── telegram-bot/     # Bot Telegram para técnicos de campo
├── frontend/         # Painel Web (HTML/CSS/JS)
└── README.md
```

## 🚀 Como Executar Localmente

### 1. Backend API

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs (Documentação Swagger automática)

### 2. Bot Telegram

```bash
cd telegram-bot
pip install -r requirements.txt
python bot.py
```

### 3. Frontend

```bash
cd frontend
# Abra index.html no navegador
# Ou use um servidor HTTP simples:
python -m http.server 8080
```

Acesse: http://localhost:8080

## 🔑 Variáveis de Ambiente Necessárias

Crie um arquivo `.env` em cada pasta (backend e telegram-bot):

### backend/.env
```
DATABASE_URL=postgresql://user:password@localhost:5432/os_db
JWT_SECRET=seu_secret_super_seguro_aqui_min_32_caracteres
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

### telegram-bot/.env
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOPqrstuvwxyz
API_BASE_URL=http://localhost:8000
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

## 📦 Deploy em Produção

### Railway (Backend + PostgreSQL)
1. Conecte seu repositório GitHub
2. Crie um novo projeto
3. Adicione PostgreSQL como add-on
4. Configure as variáveis de ambiente
5. Deploy automático!

### Vercel ou Railway (Frontend)
1. Conecte o repositório
2. Aponte para a pasta `frontend/`
3. Deploy automático!

## 🎯 Status do Desenvolvimento

- [x] Estrutura do projeto
- [x] Backend API completo (FastAPI + PostgreSQL)
  - [x] Models e Schemas
  - [x] Autenticação JWT
  - [x] CRUD de Ordens de Serviço
  - [x] Dashboard e Relatórios
  - [x] Controle de permissões por role
- [x] Bot Telegram completo
  - [x] Conversação guiada
  - [x] Upload de fotos (Cloudinary)
  - [x] Validação de GPS
  - [x] Integração com API
- [x] Frontend completo (HTML/CSS/JS)
  - [x] Sistema de login
  - [x] Dashboard com métricas
  - [x] Gerenciamento de O.S
  - [x] Design premium/responsivo
- [ ] Deploy em produção (aguardando credenciais)

## 🔑 Próximos Passos

Para colocar o sistema em produção, você precisará:

1. **Obter Token do Bot Telegram** (via @BotFather)
2. **Criar conta no Cloudinary** (upload de fotos)
3. **Opcional:** Criar contas no Railway e Vercel para deploy

Siga as instruções no arquivo `credentials_checklist.md` na pasta de artifacts.

## 📖 Documentação Completa

Veja o arquivo `implementation_plan.md` para arquitetura detalhada.
