# 🧪 Como Testar Tudo Localmente (Bot + Site)

## ✅ Bot de Teste Criado!

Seu bot de teste está pronto: **@Soparatestesbot**

Token configurado no arquivo `.env.local` ✅

---

## 🚀 Passo a Passo para Testar Tudo Localmente

### **1. Configurar Backend Local**

#### 1.1. Criar arquivo `.env` no backend

Na pasta `backend/`, crie um arquivo `.env` com:

```env
# Database (use Supabase ou SQLite local)
DATABASE_URL=postgresql://usuario:senha@host:5432/database
# OU para SQLite local:
# DATABASE_URL=sqlite:///./os_sistema.db

# Secret Key (gere uma nova para testes)
SECRET_KEY=sua_secret_key_aqui_para_testes

# Cloudinary
CLOUDINARY_URL=sua_url_cloudinary_aqui
```

#### 1.2. Executar migração do banco (se necessário)

```bash
cd backend
python migrate_add_tipo_prazo.py
```

#### 1.3. Iniciar o backend

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

O backend vai rodar em: **http://localhost:8000**

---

### **2. Configurar Bot de Teste**

#### 2.1. Verificar `.env.local`

O arquivo `.env.local` já está criado com seu token de teste ✅

#### 2.2. Atualizar Cloudinary no `.env.local`

Edite `telegram-bot/.env.local` e adicione sua URL do Cloudinary:

```env
CLOUDINARY_URL=sua_url_cloudinary_real_aqui
```

#### 2.3. Iniciar o bot

```bash
cd telegram-bot
python bot.py
```

Você deve ver: `📝 Usando configuração de TESTE (.env.local)`

---

### **3. Testar o Site Localmente**

#### 3.1. O backend já serve o frontend!

Quando você rodar o backend (`uvicorn app.main:app`), ele já serve os arquivos HTML do frontend.

#### 3.2. Acessar o site

Abra no navegador:
- **http://localhost:8000** (página inicial/login)
- **http://localhost:8000/dashboard.html** (dashboard)
- **http://localhost:8000/os-list.html** (lista de O.S)

#### 3.3. Fazer login

- Use suas credenciais de admin
- Se não tiver, crie um usuário admin primeiro

---

## 📋 Checklist Completo de Testes

### ✅ Backend
- [ ] Backend rodando em `http://localhost:8000`
- [ ] Migração executada (campos novos adicionados)
- [ ] API respondendo em `/api/v1/`
- [ ] Frontend sendo servido em `/`

### ✅ Bot de Teste
- [ ] Bot rodando localmente
- [ ] Mensagem "📝 Usando configuração de TESTE" aparece
- [ ] Consegue conversar com @Soparatestesbot no Telegram
- [ ] Menu mostra botões "Rompimento" e "Manutenções"
- [ ] Comando `/hora` funciona

### ✅ Testes no Bot
- [ ] Testar fluxo "📋 Abrir Nova O.S." (normal)
- [ ] Testar fluxo "🔧 Rompimento" (deve pedir prazo e porta)
- [ ] Testar fluxo "⚙️ Manutenções" (deve pedir prazo e porta)
- [ ] Verificar se O.S são criadas no banco
- [ ] Verificar se dados estão corretos (prazo, porta, tipo)

### ✅ Testes no Site
- [ ] Fazer login no site
- [ ] Verificar dashboard mostra estatísticas
- [ ] Verificar `os-list.html` mostra coluna "Cidade"
- [ ] Verificar dashboard mostra seção "Rompimento e Manutenções"
- [ ] Verificar tabela de Rompimento/Manutenções mostra dados corretos
- [ ] Verificar contagem regressiva funciona

---

## 🔧 Comandos Rápidos

### Terminal 1 - Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### Terminal 2 - Bot
```bash
cd telegram-bot
python bot.py
```

### Terminal 3 - Migração (se necessário)
```bash
cd backend
python migrate_add_tipo_prazo.py
```

---

## 🌐 URLs Locais

- **Backend API**: http://localhost:8000/api/v1
- **Site (Login)**: http://localhost:8000
- **Dashboard**: http://localhost:8000/dashboard.html
- **Lista O.S**: http://localhost:8000/os-list.html
- **Bot de Teste**: @Soparatestesbot (no Telegram)

---

## ⚠️ Importante

1. **Banco de Dados**: 
   - Se usar Supabase, os dados serão compartilhados entre produção e teste
   - Se usar SQLite local, será isolado

2. **Cloudinary**: 
   - Pode usar o mesmo da produção (fotos serão salvas lá)

3. **Token do Bot**: 
   - ✅ Token de teste está no `.env.local` (não vai para produção)
   - ✅ Token de produção continua no Render

---

## 🐛 Troubleshooting

### Bot não conecta
- Verifique se `.env.local` existe e tem o token correto
- Verifique se a mensagem "📝 Usando configuração de TESTE" aparece

### Backend não inicia
- Verifique se a porta 8000 está livre
- Verifique se `.env` existe no backend
- Verifique se DATABASE_URL está correto

### Site não carrega
- Verifique se backend está rodando
- Verifique console do navegador (F12) para erros
- Verifique se está acessando `http://localhost:8000`

### Bot não cria O.S
- Verifique se backend está rodando
- Verifique se `API_BASE_URL` no `.env.local` está como `http://localhost:8000`
- Verifique logs do bot para erros

---

## ✅ Quando Tudo Estiver Funcionando

1. Teste todos os fluxos
2. Verifique se dados estão sendo salvos corretamente
3. Verifique se frontend mostra tudo corretamente
4. Quando estiver satisfeito:
   - Faça commit das mudanças
   - Faça push para GitHub
   - Render vai fazer deploy automaticamente
   - Bot de produção vai usar o código atualizado

---

## 💡 Dica

Mantenha o bot de teste sempre rodando localmente para testes rápidos! Só faça deploy para produção quando tiver certeza que está tudo funcionando.
