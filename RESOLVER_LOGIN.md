# 🔐 Como Resolver o Problema de Login

## 🔍 Problema

Você está recebendo "Erro interno do servidor" ao tentar fazer login. Isso geralmente acontece porque:

1. **O banco de dados não está acessível** (problema de conexão com Supabase) ⚠️ **CONFIRMADO**
2. **O usuário admin não existe no banco**

## ✅ Solução Rápida

### **Passo 1: Testar Conexão com Banco**

Execute o script de teste:

```bash
cd backend
python testar_banco.py
```

Este script vai:
- ✅ Testar se consegue conectar ao Supabase
- ✅ Verificar se o usuário admin existe
- ✅ Criar o admin se não existir

### **Passo 2: Verificar Credenciais**

Se o script funcionar, use estas credenciais:

- **Usuário**: `admin`
- **Senha**: `admin123`

### **Passo 3: Se o Banco Não Conectar**

Se o script mostrar erro de conexão, você tem 2 opções:

#### **Opção A: Verificar Internet e DATABASE_URL**

1. Verifique se está conectado à internet
2. Verifique se o `DATABASE_URL` no `backend/.env` está correto
3. Tente acessar o Supabase no navegador

#### **Opção B: Usar SQLite Local (Temporário) ⭐ RECOMENDADO**

Se não conseguir conectar ao Supabase, use SQLite local para testar:

**Método Rápido:**
1. Execute: `USAR_SQLITE_LOCAL.bat` (vai criar um arquivo de configuração)
2. Ou edite `backend/.env` manualmente e mude:
   ```env
   DATABASE_URL=sqlite:///./os_sistema_teste.db
   ```
3. Execute o script de teste:
   ```bash
   cd backend
   python testar_banco.py
   ```
4. Reinicie o backend

**Nota**: SQLite cria um banco local separado, não usa o Supabase. Mas permite testar tudo localmente!

## 🚀 Testar Agora

1. Execute: `cd backend && python testar_banco.py`
2. Se funcionar, tente fazer login novamente no site
3. Se não funcionar, siga as opções acima

## 📝 Outros Usuários Padrão

Se o admin não funcionar, você também pode tentar:

- **Usuário**: `monitor` | **Senha**: `monitor123`
- **Usuário**: `tecnico1` | **Senha**: `tecnico123`

---

**Dica**: O script `testar_banco.py` vai criar o usuário admin automaticamente se ele não existir!
