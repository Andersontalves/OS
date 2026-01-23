# 📋 Planejamento: Rompimento e Manutenções

## 🎯 Objetivo

Adicionar dois novos tipos de Ordens de Serviço no sistema:
- **Rompimento**: Com prazo em horas, contagem regressiva e porta da placa/OLT
- **Manutenções**: Com prazo em horas e contagem regressiva

**Alterações Adicionais**:
- Adicionar coluna "Cidade" nas tabelas de O.S (Normal e Rompimento/Manutenções)
- Adicionar relógio do Brasil no bot Telegram

**Observações Importantes**:
- ✅ **Rompimento**: Adiciona pergunta de **motivo** (com "Rompimento" como opção), depois **prazo** e **porta da placa/OLT** ao fluxo existente
- ✅ **Manutenções**: Adiciona pergunta de **motivo** (com "Manutenções" como opção), depois **prazo** e **porta da placa/OLT** ao fluxo existente
- ✅ **Cidade**: Adicionar coluna nas **duas seções** do site (O.S Normal e Rompimento/Manutenções)
- ✅ **Ordem do fluxo**: Motivo → Prazo → Porta → Localização → Cidade → Fotos → PPPOE

---

## 📊 Estrutura Atual vs Nova

### Estrutura Atual
- **Tipo de O.S**: Único fluxo genérico
- **Menu Telegram**: Apenas "📋 Abrir Nova O.S."
- **Campos**: Motivo (Caixa sem sinal, Ampliação, Sinal Alto)
- **Dashboard**: Uma única tabela com todas as O.S

### Estrutura Nova
- **Tipos de O.S**: 
  - O.S Normal (fluxo atual)
  - Rompimento (novo) - **adiciona** pergunta de prazo e porta da placa ao fluxo existente
  - Manutenções (novo) - **adiciona** pergunta de prazo ao fluxo existente
- **Menu Telegram**: 3 opções + relógio do Brasil
- **Campos Adicionais**: 
  - Prazo em horas (rompimento/manutenção)
  - Porta da Placa/OLT (rompimento e manutenções)
  - Tipo de O.S
- **Dashboard**: Duas seções (O.S Normal + Rompimento/Manutenções)
- **Tabelas**: Coluna "Cidade" adicionada em ambas as seções

---

## 🗄️ 1. BANCO DE DADOS

### 1.1. Alterações no Model `OrdemServico`

**Arquivo**: `backend/app/models/ordem_servico.py`

**Novos Campos**:
```python
# Tipo de O.S
tipo_os = Column(
    String(20),
    nullable=False,
    default="normal",
    index=True
)  # Valores: "normal", "rompimento", "manutencao"

# Prazo (apenas para rompimento e manutenção)
prazo_horas = Column(Integer, nullable=True)  # Prazo em horas
prazo_fim = Column(DateTime, nullable=True)  # Data/hora limite calculada

# Porta da Placa/OLT (para rompimento e manutenções)
porta_placa_olt = Column(String(50), nullable=True)  # Porta da placa/Porta da OLT
```

**Constraint Atualizado**:
```python
__table_args__ = (
    CheckConstraint(
        "status IN ('aguardando', 'em_andamento', 'concluido')",
        name="check_status_valido"
    ),
    CheckConstraint(
        "tipo_os IN ('normal', 'rompimento', 'manutencao')",
        name="check_tipo_os_valido"
    ),
)
```

**Novos Métodos**:
```python
@property
def tempo_restante_minutos(self) -> Optional[int]:
    """Tempo restante até o prazo (apenas para rompimento/manutenção)"""
    if not self.prazo_fim or self.tipo_os == "normal":
        return None
    agora = datetime.utcnow()
    if agora > self.prazo_fim:
        return 0  # Prazo vencido
    delta = self.prazo_fim - agora
    return int(delta.total_seconds() / 60)

@property
def prazo_vencido(self) -> bool:
    """Verifica se o prazo foi vencido"""
    if not self.prazo_fim or self.tipo_os == "normal":
        return False
    return datetime.utcnow() > self.prazo_fim
```

### 1.2. Migration Script

**Arquivo**: `backend/migrate_add_tipo_prazo.py` (novo)

```python
# Script para adicionar novos campos ao banco existente
# Executar uma vez para atualizar schema
```

---

## 🤖 2. TELEGRAM BOT

### 2.1. Novos Estados de Conversação

**Arquivo**: `telegram-bot/bot.py`

**Estados Adicionais**:
```python
(
    # Estados existentes...
    CONFIRMACAO,
    # Novos estados
    PRAZO_HORAS,    # Informar prazo em horas (só para Rompimento/Manutenções)
    PORTA_PLACA,    # Informar porta da placa/OLT (só para Rompimento)
) = range(10)  # Ajustar range
```

### 2.2. Novo Menu Principal

**Função**: `get_main_menu_keyboard()`

**Antes**:
```python
[
    [KeyboardButton("📋 Abrir Nova O.S.")],
    [KeyboardButton("❓ Ajuda"), KeyboardButton("❌ Cancelar Operação")]
]
```

**Depois**:
```python
[
    [KeyboardButton("📋 Abrir Nova O.S.")],
    [KeyboardButton("🔧 Rompimento")],
    [KeyboardButton("⚙️ Manutenções")],
    [KeyboardButton("❓ Ajuda"), KeyboardButton("❌ Cancelar Operação")]
]
```

### 2.3. Novos Handlers

#### 2.3.1. Handler para Rompimento
```python
async def abrir_rompimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia fluxo de Rompimento - adiciona ao fluxo existente"""
    context.user_data.clear()
    context.user_data["tipo_os"] = "rompimento"
    
    # Pedir prazo em horas primeiro
    await update.message.reply_text(
        "🔧 *Rompimento*\n\n"
        "⏰ Informe o *prazo em HORAS* para resolução:\n"
        "Exemplo: 2 (para 2 horas)",
        parse_mode="Markdown"
    )
    return PRAZO_HORAS
```

#### 2.3.1.1. Handler para Receber Prazo (Rompimento)
```python
async def receive_prazo_horas_rompimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe prazo em horas para Rompimento e depois pede porta"""
    try:
        horas = int(update.message.text.strip())
        if horas <= 0:
            await update.message.reply_text("❌ Digite um número maior que zero.")
            return PRAZO_HORAS
        
        # Calcular data limite
        from datetime import datetime, timedelta
        prazo_fim = datetime.utcnow() + timedelta(hours=horas)
        
        context.user_data["prazo_horas"] = horas
        context.user_data["prazo_fim"] = prazo_fim.isoformat()
        
        # Pedir porta da placa/OLT
        await update.message.reply_text(
            f"✅ Prazo definido: *{horas} horas*\n"
            f"⏰ Limite: {prazo_fim.strftime('%d/%m/%Y %H:%M')}\n\n"
            "🔌 Agora informe a *Porta da Placa/Porta da OLT*:\n"
            "Exemplo: 1/1/1 ou 0/1/2",
            parse_mode="Markdown"
        )
        return PORTA_PLACA
    except ValueError:
        await update.message.reply_text("❌ Digite apenas números.")
        return PRAZO_HORAS
```

#### 2.3.1.2. Handler para Receber Porta da Placa (Rompimento e Manutenções)
```python
async def receive_porta_placa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe porta da placa/OLT e continua com fluxo normal (localização)"""
    porta = update.message.text.strip()
    context.user_data["porta_placa_olt"] = porta
    
    # Continuar com fluxo normal (localização)
    location_keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📍 Enviar Localização (GPS)", request_location=True)],
         [KeyboardButton("❌ Cancelar Operação")]],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    
    await update.message.reply_text(
        f"✅ Porta registrada: *{porta}*\n\n"
        "📍 Agora envie sua *LOCALIZAÇÃO ATUAL*:",
        parse_mode="Markdown",
        reply_markup=location_keyboard
    )
    return LOCALIZACAO
```

#### 2.3.2. Handler para Manutenções
```python
async def abrir_manutencao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia fluxo de Manutenções"""
    context.user_data.clear()
    context.user_data["tipo_os"] = "manutencao"
    
    # Pedir prazo em horas
    await update.message.reply_text(
        "⚙️ *Manutenções*\n\n"
        "⏰ Informe o *prazo em HORAS* para resolução:\n"
        "Exemplo: 4 (para 4 horas)",
        parse_mode="Markdown"
    )
    return PRAZO_HORAS
```

#### 2.3.3. Handler para Receber Prazo (Manutenções)
```python
async def receive_prazo_horas_manutencao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe prazo em horas para Manutenções e depois pede porta"""
    try:
        horas = int(update.message.text.strip())
        if horas <= 0:
            await update.message.reply_text("❌ Digite um número maior que zero.")
            return PRAZO_HORAS
        
        # Calcular data limite
        from datetime import datetime, timedelta
        prazo_fim = datetime.utcnow() + timedelta(hours=horas)
        
        context.user_data["prazo_horas"] = horas
        context.user_data["prazo_fim"] = prazo_fim.isoformat()
        
        # Pedir porta da placa/OLT
        await update.message.reply_text(
            f"✅ Prazo definido: *{horas} horas*\n"
            f"⏰ Limite: {prazo_fim.strftime('%d/%m/%Y %H:%M')}\n\n"
            "🔌 Agora informe a *Porta da Placa/Porta da OLT*:\n"
            "Exemplo: 1/1/1 ou 0/1/2",
            parse_mode="Markdown"
        )
        return PORTA_PLACA
    except ValueError:
        await update.message.reply_text("❌ Digite apenas números.")
        return PRAZO_HORAS
```

### 2.4. Ajustes no Fluxo Existente

**Modificar**: `confirmation()` para incluir novos campos:
```python
os_data = {
    # ... campos existentes ...
    "tipo_os": context.user_data.get("tipo_os", "normal"),
    "prazo_horas": context.user_data.get("prazo_horas"),
    "prazo_fim": context.user_data.get("prazo_fim"),
    "porta_placa_olt": context.user_data.get("porta_placa_olt"),  # Apenas para rompimento
}
```

**Modificar**: ConversationHandler para incluir novos estados:
```python
def get_prazo_handler(context):
    """Retorna handler correto baseado no tipo_os"""
    tipo = context.user_data.get("tipo_os")
    if tipo == "rompimento":
        return receive_prazo_horas_rompimento
    elif tipo == "manutencao":
        return receive_prazo_horas_manutencao
    return None

# Nota: Ambos os handlers (rompimento e manutenções) levam ao estado PORTA_PLACA
# O handler receive_porta_placa funciona para ambos os tipos

conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("abrir_os", abrir_os),
        MessageHandler(filters.Regex("^📋 Abrir Nova O.S.$"), abrir_os),
        MessageHandler(filters.Regex("^🔧 Rompimento$"), abrir_rompimento),
        MessageHandler(filters.Regex("^⚙️ Manutenções$"), abrir_manutencao),
    ],
    states={
        PRAZO_HORAS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & ~filters.Regex("^❌"),
                lambda u, c: get_prazo_handler(c)(u, c) if get_prazo_handler(c) else None
            )
        ],
        PORTA_PLACA: [
            MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^❌"), receive_porta_placa)  # Para rompimento e manutenções
        ],
        LOCALIZACAO: [MessageHandler(filters.LOCATION, receive_location)],
        CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^❌"), receive_cidade)],
        MOTIVO: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^❌"), receive_motivo)],
        POWER_METER: [MessageHandler(filters.PHOTO, receive_power_meter)],
        CAIXA: [MessageHandler(filters.PHOTO, receive_caixa)],
        PRINT_OS: [MessageHandler(filters.PHOTO, receive_print_os)],
        PPPOE: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^❌"), receive_pppoe)],
        CONFIRMACAO: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^❌"), confirmation)],
    },
    fallbacks=[
        CommandHandler("cancelar", cancel),
        MessageHandler(filters.Regex("^❌ Cancelar Operação$"), cancel)
    ],
)
```

### 2.5. Contagem Regressiva no Bot

**Nova Função**: `send_countdown_updates()`
```python
async def send_countdown_updates(context: ContextTypes.DEFAULT_TYPE, os_id: int, prazo_fim: datetime):
    """Envia atualizações de contagem regressiva"""
    while True:
        agora = datetime.utcnow()
        if agora >= prazo_fim:
            # Prazo vencido - notificar
            await context.bot.send_message(
                chat_id=context.user_data.get("chat_id"),
                text=f"⏰ *Prazo Vencido!*\n\nO.S {os_id} ultrapassou o prazo.",
                parse_mode="Markdown"
            )
            break
        
        tempo_restante = prazo_fim - agora
        horas = int(tempo_restante.total_seconds() / 3600)
        minutos = int((tempo_restante.total_seconds() % 3600) / 60)
        
        # Enviar atualização a cada hora
        await asyncio.sleep(3600)  # 1 hora
        await context.bot.send_message(
            chat_id=context.user_data.get("chat_id"),
            text=f"⏰ *Tempo Restante:* {horas}h {minutos}m",
            parse_mode="Markdown"
        )
```

---

## 🔌 3. BACKEND API

### 3.1. Schema Atualizado

**Arquivo**: `backend/app/schemas/ordem_servico.py`

**OrdemServicoCreate**:
```python
class OrdemServicoCreate(BaseModel):
    # ... campos existentes ...
    tipo_os: Optional[str] = "normal"  # "normal", "rompimento", "manutencao"
    prazo_horas: Optional[int] = None  # Apenas para rompimento/manutenção
    prazo_fim: Optional[datetime] = None  # Calculado no backend se não fornecido
    porta_placa_olt: Optional[str] = None  # Para rompimento e manutenções
```

**OrdemServicoResponse**:
```python
class OrdemServicoResponse(BaseModel):
    # ... campos existentes ...
    tipo_os: str
    prazo_horas: Optional[int] = None
    prazo_fim: Optional[datetime] = None
    porta_placa_olt: Optional[str] = None  # Para rompimento e manutenções
    tempo_restante_min: Optional[int] = None
    prazo_vencido: bool = False
```

**OrdemServicoListItem**:
```python
class OrdemServicoListItem(BaseModel):
    # ... campos existentes ...
    tipo_os: str
    prazo_horas: Optional[int] = None
    prazo_fim: Optional[datetime] = None
    porta_placa_olt: Optional[str] = None  # Para rompimento e manutenções
    cidade: Optional[str] = None  # Já existe, mas garantir que está no schema
```

### 3.2. Endpoint de Criação Atualizado

**Arquivo**: `backend/app/routes/os.py`

**Modificar**: `create_os()`
```python
# Calcular prazo_fim se não fornecido
if os_data.tipo_os in ["rompimento", "manutencao"] and os_data.prazo_horas:
    if not os_data.prazo_fim:
        from datetime import timedelta
        os_data.prazo_fim = datetime.utcnow() + timedelta(hours=os_data.prazo_horas)

new_os = OrdemServico(
    # ... campos existentes ...
    tipo_os=os_data.tipo_os or "normal",
    prazo_horas=os_data.prazo_horas,
    prazo_fim=os_data.prazo_fim,
    porta_placa_olt=os_data.porta_placa_olt,  # Para rompimento e manutenções
)
```

### 3.3. Novo Endpoint para Filtrar por Tipo

**Arquivo**: `backend/app/routes/os.py`

```python
@router.get("", response_model=List[OrdemServicoListItem])
def list_os(
    # ... parâmetros existentes ...
    tipo_os: Optional[str] = Query(None, description="Filtrar por tipo"),
    # ...
):
    # Adicionar filtro por tipo
    if tipo_os:
        query = query.filter(OrdemServico.tipo_os == tipo_os)
```

### 3.4. Endpoint de Relatórios Atualizado

**Arquivo**: `backend/app/routes/relatorios.py`

**Novos Campos no Dashboard**:
```python
class DashboardResponse(BaseModel):
    # ... campos existentes ...
    rompimento_aguardando: int
    rompimento_em_andamento: int
    manutencao_aguardando: int
    manutencao_em_andamento: int
    tempo_execucao_rompimento_medio: Optional[int]  # Em minutos
    tempo_execucao_manutencao_medio: Optional[int]  # Em minutos
```

---

## 🎨 4. FRONTEND

### 4.1. Atualizar Tabela de O.S Normal

**Arquivo**: `frontend/os-list.html`

**Adicionar coluna "Cidade" na tabela existente**:
```html
<thead>
    <tr>
        <th>Número O.S</th>
        <th>Status</th>
        <th>Cidade</th>  <!-- NOVA COLUNA -->
        <th>Técnico Campo</th>
        <th>Técnico Executor</th>
        <th>PPPOE</th>
        <th>Criado Em</th>
        <th>Ações</th>
    </tr>
</thead>
<tbody>
    ${osList.map(os => `
        <tr>
            <td><strong>${os.numero_os}</strong></td>
            <td><span class="badge badge-${os.status}">${getStatusLabel(os.status)}</span></td>
            <td>${os.cidade || '-'}</td>  <!-- NOVA COLUNA -->
            <td>${os.tecnico_campo_nome || 'N/A'}</td>
            <td>${os.tecnico_executor_nome || '-'}</td>
            <td>${os.pppoe_cliente}</td>
            <td>${formatDateTime(os.criado_em)}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="openOSDetails(${os.id})">Ver Detalhes</button>
            </td>
        </tr>
    `).join('')}
</tbody>
```

**Nota**: O campo `cidade` já existe no schema `OrdemServicoListItem`, apenas precisa ser exibido na tabela.

### 4.2. Nova Seção no Dashboard

**Arquivo**: `frontend/dashboard.html`

**Adicionar após a seção de O.S Normal**:
```html
<!-- Seção Rompimento e Manutenções -->
<div class="card mb-4">
    <h3 class="mb-3">🔧 Rompimento e Manutenções</h3>
    
    <!-- Stats Cards -->
    <div class="grid grid-4 mb-3">
        <div class="card">
            <div class="text-muted">Rompimento Aguardando</div>
            <h2 id="stat-rompimento-aguardando">0</h2>
        </div>
        <div class="card">
            <div class="text-muted">Rompimento Em Andamento</div>
            <h2 id="stat-rompimento-andamento">0</h2>
        </div>
        <div class="card">
            <div class="text-muted">Manutenção Aguardando</div>
            <h2 id="stat-manutencao-aguardando">0</h2>
        </div>
        <div class="card">
            <div class="text-muted">Manutenção Em Andamento</div>
            <h2 id="stat-manutencao-andamento">0</h2>
        </div>
    </div>
    
    <!-- Tabela de Rompimento e Manutenções -->
    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Número O.S</th>
                    <th>Tipo</th>
                    <th>Status</th>
                    <th>Cidade</th>
                    <th>Prazo</th>
                    <th>Tempo Restante</th>
                    <th>Porta Placa/OLT</th>  <!-- Para rompimento e manutenções -->  <!-- Para rompimento e manutenções -->
                    <th>Técnico Campo</th>
                    <th>Técnico Executor</th>
                    <th>PPPOE</th>
                    <th>Criado Em</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody id="rompimento-manutencao-tbody">
                <!-- Preenchido via JavaScript -->
            </tbody>
        </table>
    </div>
</div>
```

### 4.3. JavaScript para Contagem Regressiva

**Arquivo**: `frontend/js/api.js` ou novo arquivo `frontend/js/countdown.js`

```javascript
function formatTimeRemaining(prazoFim) {
    if (!prazoFim) return '-';
    
    const agora = new Date();
    const prazo = new Date(prazoFim);
    const diff = prazo - agora;
    
    if (diff <= 0) {
        return '<span style="color: var(--danger);">Vencido</span>';
    }
    
    const horas = Math.floor(diff / (1000 * 60 * 60));
    const minutos = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    if (horas < 1) {
        return `<span style="color: var(--danger);">${minutos}m</span>`;
    } else if (horas < 3) {
        return `<span style="color: var(--warning);">${horas}h ${minutos}m</span>`;
    }
    
    return `${horas}h ${minutos}m`;
}

// Atualizar contagem regressiva a cada minuto
setInterval(() => {
    updateCountdowns();
}, 60000);
```

### 4.4. Atualizar API Client

**Arquivo**: `frontend/js/api.js`

**Novo Método**:
```javascript
async getOrdensRompimentoManutencao(filters = {}) {
    const params = new URLSearchParams({ tipo_os: 'rompimento,manutencao', ...filters });
    const response = await fetch(`${API_BASE_URL}/api/v1/os?${params}`, {
        headers: this.getHeaders()
    });
    if (!response.ok) throw new Error('Erro ao buscar O.S');
    return response.json();
}
```

---

## 📝 5. FLUXO COMPLETO

### 5.1. Fluxo Rompimento

**IMPORTANTE**: O fluxo de Rompimento **adiciona** perguntas ao fluxo existente, não cria um fluxo completamente novo.

1. **Usuário clica "🔧 Rompimento"**
2. **Bot define**: `tipo_os = "rompimento"` no contexto
3. **Bot pede**: "Qual o MOTIVO da abertura desta O.S?" (com opções: Rompimento, Caixa sem sinal, Ampliação, Sinal Alto)
4. **Usuário escolhe**: "Rompimento" (ou outro motivo)
5. **Bot pede**: "Informe o prazo em HORAS"
6. **Usuário digita**: "2" (exemplo)
7. **Bot calcula**: Prazo fim = agora + 2 horas
8. **Bot pede**: "Porta da Placa/Porta da OLT"
9. **Usuário digita**: "1/1/1" (exemplo)
10. **Bot continua com fluxo normal**:
    - Localização GPS
    - Cidade
    - Fotos (Power Meter, Caixa, Print O.S)
    - PPPOE
11. **Bot mostra resumo** com motivo, prazo e porta
12. **Bot cria O.S** via API com `tipo_os="rompimento"`, `motivo_abertura="Rompimento"`, `prazo_horas=2` e `porta_placa_olt="1/1/1"`
13. **Bot inicia contagem regressiva** (envia atualizações a cada hora)

### 5.2. Fluxo Manutenções

**IMPORTANTE**: O fluxo de Manutenções **adiciona** pergunta de motivo, prazo e porta da placa ao fluxo existente.

1. **Usuário clica "⚙️ Manutenções"**
2. **Bot define**: `tipo_os = "manutencao"` no contexto
3. **Bot pede**: "Qual o MOTIVO da abertura desta O.S?" (com opções: Manutenções, Caixa sem sinal, Ampliação, Sinal Alto)
4. **Usuário escolhe**: "Manutenções" (ou outro motivo)
5. **Bot pede**: "Informe o prazo em HORAS"
6. **Usuário digita**: "4" (exemplo)
7. **Bot calcula**: Prazo fim = agora + 4 horas
8. **Bot pede**: "Porta da Placa/Porta da OLT"
9. **Usuário digita**: "1/1/1" (exemplo)
10. **Bot continua com fluxo normal**:
    - Localização GPS
    - Cidade
    - Fotos (Power Meter, Caixa, Print O.S)
    - PPPOE
11. **Bot mostra resumo** com motivo, prazo e porta
12. **Bot cria O.S** via API com `tipo_os="manutencao"`, `motivo_abertura="Manutenções"`, `prazo_horas=4` e `porta_placa_olt="1/1/1"`
13. **Bot inicia contagem regressiva** (envia atualizações a cada hora)

---

## 🔄 6. MIGRAÇÃO DE DADOS

### 6.1. Script de Migração

**Arquivo**: `backend/migrate_add_tipo_prazo.py`

```python
"""
Script para adicionar campos tipo_os, prazo e porta_placa_olt ao banco existente
- Define todas as O.S existentes como tipo_os="normal"
- Adiciona colunas tipo_os, prazo_horas, prazo_fim, porta_placa_olt
"""

from sqlalchemy import text
from app.database import engine

def migrate():
    with engine.begin() as conn:
        # Adicionar colunas
        conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS tipo_os VARCHAR(20) DEFAULT 'normal'"))
        conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS prazo_horas INTEGER"))
        conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS prazo_fim TIMESTAMP"))
        conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS porta_placa_olt VARCHAR(50)"))
        
        # Atualizar O.S existentes
        conn.execute(text("UPDATE ordens_servico SET tipo_os = 'normal' WHERE tipo_os IS NULL"))
        
        print("✅ Migração concluída!")
```

---

## 📊 7. DASHBOARD - CÁLCULOS SEPARADOS

### 7.1. Tempo Médio de Execução por Tipo

**Backend**: `backend/app/routes/relatorios.py`

```python
# Tempo médio de execução para Rompimento
tempo_exec_rompimento = (
    db.query(func.avg(
        func.extract('epoch', OrdemServico.concluido_em - OrdemServico.iniciado_em) / 60
    ))
    .filter(OrdemServico.tipo_os == "rompimento")
    .filter(OrdemServico.status == "concluido")
    .scalar()
)

# Tempo médio de execução para Manutenções
tempo_exec_manutencao = (
    db.query(func.avg(
        func.extract('epoch', OrdemServico.concluido_em - OrdemServico.iniciado_em) / 60
    ))
    .filter(OrdemServico.tipo_os == "manutencao")
    .filter(OrdemServico.status == "concluido")
    .scalar()
)
```

### 7.2. Exibição no Frontend

```html
<div class="card">
    <div class="text-muted">⚡ Tempo Médio Execução - Rompimento</div>
    <h3 id="metric-execucao-rompimento">-</h3>
</div>
<div class="card">
    <div class="text-muted">⚡ Tempo Médio Execução - Manutenções</div>
    <h3 id="metric-execucao-manutencao">-</h3>
</div>
```

---

## ✅ 8. CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Banco de Dados
- [ ] Adicionar colunas `tipo_os`, `prazo_horas`, `prazo_fim`, `porta_placa_olt` no model
- [ ] Criar script de migração
- [ ] Executar migração no Supabase
- [ ] Atualizar schemas Pydantic

### Fase 2: Backend API
- [ ] Atualizar `OrdemServicoCreate` schema
- [ ] Atualizar `create_os()` para aceitar novos campos
- [ ] Adicionar filtro por `tipo_os` em `list_os()`
- [ ] Atualizar `get_dashboard()` com estatísticas separadas
- [ ] Adicionar cálculos de tempo médio por tipo

### Fase 3: Telegram Bot
- [ ] Adicionar novos estados `PRAZO_HORAS`, `PORTA_PLACA`
- [ ] Criar handlers `abrir_rompimento()` e `abrir_manutencao()`
- [ ] Criar handlers `receive_prazo_horas_rompimento()` e `receive_prazo_horas_manutencao()`
- [ ] Criar handler `receive_porta_placa()` (só para rompimento)
- [ ] Atualizar menu principal com novos botões
- [ ] Atualizar ConversationHandler com novos estados
- [ ] Atualizar `confirmation()` para incluir novos campos (`porta_placa_olt`)
- [ ] Implementar contagem regressiva (opcional - pode ser só no frontend)

### Fase 4: Frontend
- [ ] Adicionar coluna "Cidade" na tabela de O.S Normal (`os-list.html`)
- [ ] Criar nova seção no dashboard para Rompimento/Manutenções
- [ ] Adicionar tabela separada com colunas: Tipo, Status, Cidade, Prazo, Tempo Restante, Porta Placa/OLT
- [ ] Implementar função de contagem regressiva
- [ ] Atualizar API client com novo método
- [ ] Adicionar exibição de prazo e porta nas O.S
- [ ] Adicionar métricas de tempo médio por tipo

### Fase 5: Testes
- [ ] Testar criação de O.S Rompimento via bot
- [ ] Testar criação de O.S Manutenções via bot
- [ ] Testar exibição na dashboard
- [ ] Testar contagem regressiva
- [ ] Testar filtros e relatórios

---

## 🎨 9. DETALHES DE UI/UX

### 9.1. Cores e Badges

**Rompimento**:
- Badge: Laranja/Vermelho (`#ff6b6b`)
- Ícone: 🔧

**Manutenções**:
- Badge: Azul (`#4dabf7`)
- Ícone: ⚙️

### 9.2. Indicadores de Prazo

- **Verde**: Mais de 3 horas restantes
- **Amarelo**: Entre 1-3 horas restantes
- **Vermelho**: Menos de 1 hora ou vencido

### 9.3. Tabela de Rompimento/Manutenções

**Colunas**:
1. Número O.S
2. Tipo (badge colorido)
3. Status
4. Cidade
5. Prazo (horas definidas)
6. Tempo Restante (contagem regressiva)
7. Porta Placa/OLT (apenas para rompimento)
8. Técnico Campo
9. Técnico Executor
10. PPPOE
11. Criado Em
12. Ações (Ver Detalhes)

---

## 📦 10. ARQUIVOS A MODIFICAR/CRIAR

### Modificar:
1. `backend/app/models/ordem_servico.py` - Adicionar `porta_placa_olt`
2. `backend/app/schemas/ordem_servico.py` - Adicionar `porta_placa_olt` e garantir `cidade`
3. `backend/app/routes/os.py` - Incluir `porta_placa_olt` na criação
4. `backend/app/routes/relatorios.py` - Estatísticas separadas
5. `telegram-bot/bot.py` - Novos handlers e estados
6. `frontend/dashboard.html` - Nova seção Rompimento/Manutenções
7. `frontend/os-list.html` - Adicionar coluna "Cidade" na tabela existente
8. `frontend/js/api.js` - Métodos para buscar O.S por tipo

### Criar:
1. `backend/migrate_add_tipo_prazo.py`
2. `frontend/js/countdown.js` (opcional)

---

## ⚠️ 11. CONSIDERAÇÕES IMPORTANTES

1. **Compatibilidade**: O.S existentes continuam funcionando (tipo_os="normal")
2. **Prazo Opcional**: Apenas Rompimento e Manutenções têm prazo
3. **Contagem Regressiva**: Pode ser implementada apenas no frontend (mais simples)
4. **Notificações**: Contagem regressiva no bot é opcional (pode ser só visual no dashboard)
5. **Validação**: Garantir que prazo_horas só é aceito para rompimento/manutenção

---

## 🚀 12. ORDEM DE IMPLEMENTAÇÃO RECOMENDADA

1. **Banco de Dados** (Fase 1)
2. **Backend API** (Fase 2)
3. **Telegram Bot** (Fase 3)
4. **Frontend** (Fase 4)
5. **Testes** (Fase 5)

---

## 📝 13. EXEMPLOS DE DADOS

### O.S Rompimento Criada:
```json
{
  "numero_os": "ROM-2026-001",
  "tipo_os": "rompimento",
  "prazo_horas": 2,
  "prazo_fim": "2026-01-22T23:00:00Z",
  "porta_placa_olt": "1/1/1",
  "cidade": "São Paulo",
  "status": "aguardando",
  ...
}
```

### O.S Manutenção Criada:
```json
{
  "numero_os": "MAN-2026-001",
  "tipo_os": "manutencao",
  "prazo_horas": 4,
  "prazo_fim": "2026-01-23T01:00:00Z",
  "porta_placa_olt": "1/1/1",
  "cidade": "São Paulo",
  "status": "aguardando",
  ...
}
```

---

---

## 🕐 14. RELÓGIO NO BOT TELEGRAM

### 14.1. Objetivo

Adicionar um relógio que mostra a hora atual do Brasil (horário de Brasília - UTC-3) no bot do Telegram.

### 14.2. Especificações

- **Fuso Horário**: UTC-3 (Brasil/Brasília) - fixo, sem horário de verão
- **Formato**: HH:MM:SS (24 horas)
- **Atualização**: A cada segundo (ou a cada minuto, conforme preferência)
- **Exibição**: No menu principal do bot ou em comando específico

### 14.3. Implementação no Bot

**Arquivo**: `telegram-bot/bot.py`

#### 14.3.1. Função para Obter Hora do Brasil

```python
from datetime import datetime
import pytz

def get_brasil_time() -> str:
    """Retorna hora atual do Brasil (UTC-3, sem horário de verão)"""
    # Fuso horário fixo UTC-3 (Brasil não tem mais horário de verão)
    brasil_tz = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(brasil_tz)
    return agora.strftime('%H:%M:%S')

def get_brasil_datetime() -> datetime:
    """Retorna datetime atual do Brasil"""
    brasil_tz = pytz.timezone('America/Sao_Paulo')
    return datetime.now(brasil_tz)
```

#### 14.3.2. Comando `/hora` ou `/relogio`

```python
async def hora_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para mostrar hora atual do Brasil"""
    hora_atual = get_brasil_time()
    data_atual = get_brasil_datetime().strftime('%d/%m/%Y')
    
    await update.message.reply_text(
        f"🕐 *Hora Atual (Brasil)*\n\n"
        f"📅 Data: {data_atual}\n"
        f"⏰ Hora: *{hora_atual}*\n\n"
        f"Fuso: UTC-3 (Brasília)",
        parse_mode="Markdown"
    )
```

#### 14.3.3. Relógio no Menu Principal (Opcional)

**Opção A - Botão no Menu**:
```python
def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("📋 Abrir Nova O.S.")],
            [KeyboardButton("🔧 Rompimento")],
            [KeyboardButton("⚙️ Manutenções")],
            [KeyboardButton("🕐 Ver Hora"), KeyboardButton("❓ Ajuda")],
            [KeyboardButton("❌ Cancelar Operação")]
        ],
        resize_keyboard=True
    )
```

**Opção B - Mostrar hora automaticamente em mensagens**:
```python
# Adicionar footer com hora em mensagens importantes
def add_time_footer(text: str) -> str:
    hora = get_brasil_time()
    return f"{text}\n\n🕐 {hora} (Brasil)"
```

#### 14.3.4. Relógio em Tempo Real (Opcional - Avançado)

Se quiser um relógio que atualiza automaticamente:

```python
async def send_live_clock(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """Envia relógio que atualiza a cada minuto"""
    message_id = None
    while True:
        hora = get_brasil_time()
        data = get_brasil_datetime().strftime('%d/%m/%Y')
        
        texto = f"🕐 *{hora}*\n📅 {data}\n🇧🇷 Brasil (UTC-3)"
        
        if message_id:
            # Editar mensagem existente
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=texto,
                parse_mode="Markdown"
            )
        else:
            # Criar nova mensagem
            msg = await context.bot.send_message(
                chat_id=chat_id,
                text=texto,
                parse_mode="Markdown"
            )
            message_id = msg.message_id
        
        await asyncio.sleep(60)  # Atualizar a cada minuto
```

### 14.4. Dependências

**Arquivo**: `telegram-bot/requirements.txt`

```python
pytz>=2024.1  # Para timezone do Brasil
```

### 14.5. Alternativa Sem Biblioteca Externa

Se não quiser usar `pytz`, pode calcular manualmente:

```python
from datetime import datetime, timedelta, timezone

def get_brasil_time() -> str:
    """Retorna hora atual do Brasil (UTC-3 fixo)"""
    # UTC-3 fixo (Brasil não tem mais horário de verão)
    brasil_offset = timedelta(hours=-3)
    brasil_tz = timezone(brasil_offset)
    agora = datetime.now(brasil_tz)
    return agora.strftime('%H:%M:%S')
```

### 14.6. Uso no Resumo de O.S

**Modificar**: `confirmation()` para incluir hora:

```python
async def confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create OS via API"""
    response = update.message.text.strip()
    if "Confirmar" in response:
        hora_atual = get_brasil_time()
        await update.message.reply_text(
            f"📤 Enviando O.S...\n🕐 {hora_atual}",
            reply_markup=ReplyKeyboardRemove()
        )
        # ... resto do código ...
```

### 14.7. Exibição na Contagem Regressiva

**Modificar**: Mensagens de contagem regressiva para incluir hora:

```python
async def send_countdown_update(context, os_id, tempo_restante, prazo_fim):
    hora_atual = get_brasil_time()
    await context.bot.send_message(
        chat_id=context.user_data.get("chat_id"),
        text=(
            f"⏰ *Tempo Restante:* {tempo_restante}\n"
            f"🕐 Hora atual: {hora_atual}\n"
            f"📅 Prazo: {prazo_fim.strftime('%d/%m/%Y %H:%M')}"
        ),
        parse_mode="Markdown"
    )
```

### 14.8. Checklist Relógio

- [ ] Adicionar função `get_brasil_time()` no bot.py
- [ ] Adicionar comando `/hora` ou `/relogio`
- [ ] (Opcional) Adicionar botão "🕐 Ver Hora" no menu
- [ ] (Opcional) Mostrar hora em mensagens importantes
- [ ] Adicionar `pytz` no requirements.txt OU usar cálculo manual UTC-3
- [ ] Testar exibição correta do horário brasileiro

---

---

## 📋 RESUMO DAS ALTERAÇÕES SOLICITADAS

### ✅ Alterações Confirmadas

1. **Rompimento adiciona ao fluxo existente**:
   - ✅ Pergunta de **motivo** primeiro (com "Rompimento" como opção)
   - ✅ Pergunta de **prazo em horas** (após motivo)
   - ✅ Pergunta de **porta da placa/Porta da OLT** (após prazo)
   - ✅ Continua com fluxo normal (localização, cidade, fotos, PPPOE)

2. **Manutenções adiciona ao fluxo existente**:
   - ✅ Pergunta de **motivo** primeiro (com "Manutenções" como opção)
   - ✅ Pergunta de **prazo em horas** (após motivo)
   - ✅ Pergunta de **porta da placa/Porta da OLT** (após prazo)
   - ✅ Continua com fluxo normal (localização, cidade, fotos, PPPOE)

3. **Coluna Cidade nas tabelas**:
   - ✅ Adicionar coluna "Cidade" na tabela de **O.S Normal** (`os-list.html`)
   - ✅ Adicionar coluna "Cidade" na tabela de **Rompimento/Manutenções** (`dashboard.html`)

4. **Relógio do Brasil**:
   - ✅ Comando `/hora` ou botão no menu
   - ✅ Fuso UTC-3 fixo (sem horário de verão)
   - ✅ Exibição em mensagens importantes

### 📊 Estrutura de Campos por Tipo

| Campo | O.S Normal | Rompimento | Manutenções |
|-------|------------|------------|-------------|
| tipo_os | "normal" | "rompimento" | "manutencao" |
| prazo_horas | ❌ | ✅ | ✅ |
| porta_placa_olt | ❌ | ✅ | ✅ |
| cidade | ✅ | ✅ | ✅ |

---

## ✅ APROVAÇÃO

Este planejamento está pronto para implementação. Todos os detalhes técnicos foram mapeados, incluindo:
- ✅ Rompimento com prazo e porta da placa
- ✅ Manutenções com prazo e porta da placa
- ✅ Coluna Cidade em ambas as tabelas
- ✅ Relógio do Brasil

**Próximo passo**: Aguardar aprovação do usuário antes de iniciar a implementação.
