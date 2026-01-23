# 🧪 Como Testar o Bot sem Interferir na Produção

## ⚠️ Problema

Se você tentar rodar o bot localmente com o **mesmo TOKEN** do bot de produção, vai acontecer:
- ❌ Conflito entre os dois bots
- ❌ Mensagens podem ir para qualquer um dos dois
- ❌ Estados de conversação podem se misturar

## ✅ Soluções

### **Opção 1: Criar Bot de Teste Separado (RECOMENDADO)**

Esta é a melhor opção porque permite testar sem afetar a produção.

#### Passo 1: Criar Bot de Teste no Telegram

1. Abra o Telegram e procure por **@BotFather**
2. Envie `/newbot`
3. Escolha um nome para o bot de teste (ex: "OS Sistema Teste")
4. Escolha um username (ex: "os_sistema_teste_bot")
5. **Copie o TOKEN** que o BotFather fornecer

#### Passo 2: Criar arquivo `.env` de teste local

Crie um arquivo `.env.local` ou `.env.test` na pasta `telegram-bot/`:

```env
# Bot de TESTE (não interfere com produção)
TELEGRAM_BOT_TOKEN=SEU_TOKEN_DO_BOT_DE_TESTE_AQUI

# API local ou de desenvolvimento
API_BASE_URL=http://localhost:8000

# Cloudinary (pode usar o mesmo)
CLOUDINARY_URL=sua_url_cloudinary_aqui
```

#### Passo 3: Modificar `config.py` para usar arquivo de teste

Você pode modificar temporariamente o `config.py`:

```python
import os
from dotenv import load_dotenv

# Carregar .env.local se existir (para testes), senão .env normal
if os.path.exists('.env.local'):
    load_dotenv('.env.local')
else:
    load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_ENDPOINT_CREATE_OS = f"{API_BASE_URL}/api/v1/os"
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
MAX_LOCATION_PRECISION_METERS = 5.0
MIN_POWER_METER_DBM = -21.0
```

#### Passo 4: Rodar o bot de teste

```bash
cd telegram-bot
python bot.py
```

**Vantagens:**
- ✅ Não interfere com produção
- ✅ Pode testar livremente
- ✅ Pode ter múltiplos usuários testando
- ✅ Não precisa desligar produção

---

### **Opção 2: Desligar Produção Temporariamente**

Se você não quiser criar um bot de teste, pode desligar o bot de produção temporariamente.

#### Passo 1: Parar o bot de produção no Render

1. Acesse o dashboard do Render
2. Vá para o serviço do bot (`os-sistema-bot`)
3. Clique em **"Manual Deploy"** → **"Suspend"** ou pare o serviço

#### Passo 2: Rodar localmente

```bash
cd telegram-bot
python bot.py
```

#### Passo 3: Testar

- Use o mesmo bot no Telegram
- Teste todas as funcionalidades
- Quando terminar, ligue a produção novamente

**Desvantagens:**
- ❌ Produção fica offline durante os testes
- ❌ Usuários reais não podem usar o bot
- ⚠️ Precisa lembrar de ligar produção depois

---

### **Opção 3: Usar Variável de Ambiente**

Você pode criar um script de teste que sobrescreve o token:

#### Criar `test_bot.py`:

```python
import os
import sys

# Definir token de teste antes de importar config
os.environ['TELEGRAM_BOT_TOKEN'] = 'SEU_TOKEN_DE_TESTE_AQUI'
os.environ['API_BASE_URL'] = 'http://localhost:8000'

# Agora importar e rodar o bot
from bot import main

if __name__ == "__main__":
    main()
```

Rodar:
```bash
python test_bot.py
```

---

## 🎯 Recomendação

**Use a Opção 1 (Bot de Teste Separado)** porque:
- É a forma mais segura
- Permite testar sem afetar usuários reais
- Você pode manter ambos rodando simultaneamente
- É a prática padrão em desenvolvimento

## 📝 Checklist para Testar

- [ ] Criar bot de teste no BotFather
- [ ] Criar `.env.local` com token de teste
- [ ] Modificar `config.py` para carregar `.env.local`
- [ ] Rodar backend localmente (`python -m uvicorn app.main:app`)
- [ ] Rodar bot de teste (`python bot.py`)
- [ ] Testar fluxo "Rompimento"
- [ ] Testar fluxo "Manutenções"
- [ ] Testar comando `/hora`
- [ ] Verificar se dados são salvos corretamente no banco
- [ ] Verificar se frontend mostra os dados corretamente

## 🔄 Quando Estiver Pronto para Produção

1. Teste tudo localmente primeiro
2. Quando confirmar que está funcionando:
   - Faça commit das mudanças
   - Faça push para GitHub
   - O Render vai fazer deploy automaticamente
   - O bot de produção vai usar o código atualizado

---

## 💡 Dica Extra

Você pode manter o bot de teste sempre rodando localmente para testes rápidos, e só fazer deploy para produção quando tiver certeza que está tudo funcionando!
