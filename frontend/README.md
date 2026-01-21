# Frontend - Sistema O.S

Painel web para gestão de ordens de serviço. Interface moderna com suporte para admin, monitoramento e execução.

## 🎨 Tecnologias

- HTML5
- CSS3 (Design System customizado)
- Vanilla JavaScript
- API REST integration

## 📁 Estrutura

```
frontend/
├── index.html          # Login
├── dashboard.html      # Dashboard com estatísticas
├── os-list.html        # Lista e gerenciamento de O.S
├── css/
│   └── style.css       # Design system completo
└── js/
    └── api.js          # Cliente da API
```

## 🚀 Como Executar

### Opção 1: Python HTTP Server (Recomendado)

```bash
cd frontend
python -m http.server 8080
```

Acesse: http://localhost:8080

### Opção 2: Abrir diretamente

Abra `index.html` no navegador (pode ter problemas de CORS)

## 🔐 Usuários Padrão

Após inicializar o backend com `init_db.py`:

| Username | Password | Role | Acesso |
|----------|----------|------|--------|
| admin | admin123 | admin | Total (CRUD, relatórios, gerenciar usuários) |
| monitor | monitor123 | monitoramento | Somente leitura |
| tecnico1 | tecnico123 | execucao | Assumir e finalizar O.S |
| tecnico2 | tecnico123 | execucao | Assumir e finalizar O.S |

## 🎯 Funcionalidades por Perfil

### Admin
- ✅ Visualizar todas as O.S
- ✅ Assumir qualquer O.S
- ✅ Finalizar qualquer O.S
- ✅ Editar qualquer O.S
- ✅ Excluir O.S
- ✅ Visualizar relatórios completos

### Monitoramento
- ✅ Visualizar todas as O.S
- ✅ Visualizar relatórios
- ❌ Não pode assumir/finalizar/editar

### Execução
- ✅ Visualizar O.S "Aguardando"
- ✅ Visualizar suas próprias O.S
- ✅ Assumir O.S disponíveis
- ✅ Finalizar suas próprias O.S
- ❌ Não pode editar/excluir

## ⚙️ Configuração

Edite `js/api.js` para alterar a URL da API:

```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
// Em produção:
// const API_BASE_URL = 'https://sua-api.railway.app/api/v1';
```

## 🌍 Deploy (Vercel)

1. Conecte o repositório no Vercel
2. Configure:
   - Root Directory: `frontend/`
   - Framework Preset: Other
3. Deploy automático!

## 📱 Responsivo

O design é totalmente responsivo e funciona perfeitamente em:
- 💻 Desktop
- 📱 Tablet
- 📱 Mobile

## 🎨 Design System

- **Tema:** Dark mode premium
- **Estilo:** Glassmorphism
- **Cores:** Paleta HSL customizada
- **Tipografia:** Inter (fallback: system fonts)
- **Componentes:** Cards, Buttons, Forms, Tables, Badges, Alerts

## 🔄 Fluxo de Uso

1. **Login** (`index.html`)
   - Insira credenciais
   - JWT armazenado no localStorage
   - Redirecionamento automático para dashboard

2. **Dashboard** (`dashboard.html`)
   - Visualizar estatísticas gerais
   - Métricas de tempo
   - Performance por técnico

3. **Ordens de Serviço** (`os-list.html`)
   - Listar todas as O.S (com filtros)
   - Ver detalhes completos
   - Assumir O.S (Execução)
   - Finalizar O.S (Execução)
   - Editar/Excluir (Admin)
