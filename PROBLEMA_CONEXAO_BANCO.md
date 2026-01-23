# ⚠️ Problema de Conexão com Banco de Dados

## 🔍 O Que Está Acontecendo

O backend está tentando conectar ao Supabase, mas está falhando com o erro:
```
could not translate host name "db.cowurbzofreatfgwmfwp.supabase.co" to address
```

Isso significa que o computador não consegue resolver o DNS do Supabase.

## ✅ Soluções

### **Opção 1: Verificar Conexão com Internet**

1. Verifique se você está conectado à internet
2. Tente acessar: https://db.cowurbzofreatfgwmfwp.supabase.co no navegador
3. Se não abrir, pode ser problema de rede/DNS

### **Opção 2: Usar SQLite Local (Temporário)**

Se não conseguir conectar ao Supabase agora, você pode usar SQLite local para testar:

Edite `backend/.env` e mude:
```env
# De:
DATABASE_URL=postgresql://postgres:%40Nder0211@db.cowurbzofreatfgwmfwp.supabase.co:5432/postgres

# Para:
DATABASE_URL=sqlite:///./os_sistema_teste.db
```

**Nota**: Isso cria um banco local separado, não usa o Supabase.

### **Opção 3: Verificar DATABASE_URL**

Verifique se o `DATABASE_URL` no `backend/.env` está correto:
- URL deve estar completa
- Senha deve estar codificada corretamente (use `%40` para `@`)
- Porta deve ser `5432` ou `6543` (depende do Supabase)

### **Opção 4: Testar Conexão Manualmente**

Execute no terminal:
```bash
cd backend
python -c "from app.database import engine; engine.connect(); print('Conexao OK!')"
```

## 🚀 Solução Rápida para Testar o Site

Mesmo com erro de conexão, o servidor pode iniciar. Tente acessar:
- http://localhost:8000

Se o servidor iniciou (mesmo com aviso), o site deve abrir. Algumas funcionalidades que precisam do banco podem não funcionar, mas você pode ver o frontend.

## 📝 Próximos Passos

1. Verifique sua conexão com internet
2. Tente acessar o Supabase no navegador
3. Se não funcionar, use SQLite local temporariamente
4. Ou aguarde a conexão voltar

---

**Dica**: O bot de teste está funcionando! Você pode testar o bot no Telegram enquanto resolve o problema do banco.
