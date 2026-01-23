# 🚀 Configuração Automática via Script

## ✅ Método Mais Fácil

Ao invés de configurar manualmente no Render Dashboard, você pode usar o script Python que faz tudo automaticamente!

## 📋 Pré-requisitos

1. **Python instalado** (já deve ter)
2. **Bibliotecas necessárias**:
   ```bash
   cd backend
   pip install requests colorama
   ```

## 🔑 Passo 1: Obter Informações Necessárias

Você precisa de 3 informações:

### 1. API Key do Render
1. Acesse: https://dashboard.render.com
2. Vá em **Account Settings** → **API Keys**
3. Clique em **"Create API Key"**
4. **Copie o token** (começa com `rnd_...`)

### 2. Service ID do `os-sistema-api` (Backend)
1. Render Dashboard → `os-sistema-api` → **Settings**
2. Copie o **Service ID** (formato: `srv_...`)

### 3. Service ID do `os-sistema-bot` (Bot)
1. Render Dashboard → `os-sistema-bot` → **Settings**
2. Copie o **Service ID** (formato: `srv_...`)

## 🚀 Passo 2: Executar o Script

```bash
cd backend
python configurar_render_api.py
```

O script vai:
1. ✅ Pedir o API Key
2. ✅ Testar se o API Key é válido
3. ✅ Pedir o Service ID do backend
4. ✅ Pedir o Service ID do bot
5. ✅ Listar variáveis existentes
6. ✅ Adicionar `RENDER_API_KEY` e `RENDER_BOT_SERVICE_ID`
7. ✅ Atualizar tudo automaticamente

## 📝 Exemplo de Execução

```
🔧 Configurador Automático - Render API
============================================================

ℹ️  Passo 1: API Key do Render
  1. Acesse: https://dashboard.render.com
  2. Vá em Account Settings → API Keys
  3. Clique em 'Create API Key'
  4. Copie o token (começa com 'rnd_...')

Cole o API Key do Render: rnd_xxxxxxxxxxxxx
ℹ️  Testando API Key...
✅ API Key válido!

ℹ️  Passo 2: Service ID do os-sistema-api (Backend)
  Este é o serviço onde vamos adicionar as variáveis.
  1. No Render Dashboard, vá no serviço
  2. Vá em Settings
  3. Role até 'Service ID'
  4. Copie o ID (formato: 'srv_...')

Cole o Service ID do os-sistema-api (Backend): srv_xxxxxxxxxxxxx

ℹ️  Passo 2: Service ID do os-sistema-bot (Bot Telegram)
  Este é o serviço que será reiniciado quando o bot estiver offline.
  1. No Render Dashboard, vá no serviço
  2. Vá em Settings
  3. Role até 'Service ID'
  4. Copie o ID (formato: 'srv_...')

Cole o Service ID do os-sistema-bot (Bot Telegram): srv_yyyyyyyyyyyyy

ℹ️  Obtendo variáveis de ambiente existentes...
✅ Encontradas 5 variáveis existentes

ℹ️  Adicionando/atualizando variáveis:
  RENDER_API_KEY = rnd_xxxxx...
  RENDER_BOT_SERVICE_ID = srv_yyyyyyyyyyyyy

Resumo das variáveis que serão configuradas:
Total: 7 variáveis
  • DATABASE_URL = postgresql...
  • JWT_SECRET = ***
  • RENDER_API_KEY = rnd_xxxxx...xxxx
  • RENDER_BOT_SERVICE_ID = srv_yyyyyyyyyyyyy
  ...

⚠️  ATENÇÃO: Isso vai substituir TODAS as variáveis de ambiente!
   Variáveis existentes serão mantidas, mas novas serão adicionadas.

Continuar? (s/n): s

ℹ️  Atualizando variáveis de ambiente...
✅ Variáveis de ambiente atualizadas com sucesso!

✅ ============================================================
✅ Configuração concluída com sucesso!
✅ ============================================================

ℹ️  Próximos passos:
  1. O serviço os-sistema-api vai reiniciar automaticamente
  2. Aguarde 1-2 minutos
  3. Teste clicando em 'Destravar Bot' no site
  4. Se o bot estiver offline, ele será reiniciado automaticamente!
```

## ✅ Pronto!

Após executar o script:
1. O Render vai reiniciar o serviço `os-sistema-api` automaticamente
2. Aguarde 1-2 minutos
3. Teste clicando em **"🔧 Destravar Bot"** no site
4. Se o bot estiver offline, ele será reiniciado automaticamente!

## 🐛 Troubleshooting

### Erro: "API Key inválido"
- Verifique se copiou o token completo
- Certifique-se de que o token não expirou
- Crie um novo token se necessário

### Erro: "Serviço não encontrado"
- Verifique se o Service ID está correto
- Certifique-se de que está copiando o ID do serviço correto

### Erro: "ModuleNotFoundError: No module named 'requests'"
```bash
pip install requests colorama
```

## 💡 Vantagens do Script

- ✅ **Automático**: Não precisa ir no Dashboard
- ✅ **Seguro**: Mantém todas as variáveis existentes
- ✅ **Rápido**: Configura em segundos
- ✅ **Validação**: Testa API Key antes de usar
- ✅ **Visual**: Mostra resumo antes de confirmar
