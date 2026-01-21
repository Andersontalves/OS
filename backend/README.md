# Backend FastAPI

API completa para o Sistema de Ordens de Serviço.

## 🚀 Instalação

1. Criar ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:
```bash
copy .env.example .env
# Edite o arquivo .env com suas credenciais
```

4. Inicializar banco de dados:
```bash
python init_db.py
```

## ▶️ Executar

```bash
python -m uvicorn app.main:app --reload
```

A API estará disponível em:
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

## 📚 Endpoints Principais

### Autenticação
- `POST /api/v1/auth/login` - Login e obtenção de JWT
- `GET /api/v1/auth/me` - Informações do usuário autenticado

### Ordens de Serviço
- `POST /api/v1/os` - Criar O.S (Telegram bot)
- `GET /api/v1/os` - Listar O.S
- `GET /api/v1/os/{id}` - Detalhes de uma O.S
- `PATCH /api/v1/os/{id}/assumir` - Assumir O.S
- `PATCH /api/v1/os/{id}/finalizar` - Finalizar O.S
- `PATCH /api/v1/os/{id}` - Editar O.S (Admin)
- `DELETE /api/v1/os/{id}` - Deletar O.S (Admin)

### Relatórios
- `GET /api/v1/relatorios/dashboard` - Estatísticas e métricas

## 👥 Usuários Padrão

Após rodar `init_db.py`:

| Username | Password | Role | Descrição |
|----------|----------|------|-----------|
| admin | admin123 | admin | Acesso total |
| monitor | monitor123 | monitoramento | Somente leitura |
| tecnico1 | tecnico123 | execucao | Assumir/Finalizar O.S |
| tecnico2 | tecnico123 | execucao | Assumir/Finalizar O.S |
| campo1 | campo123 | campo | Telegram (não usa web) |

## 🔒 Autenticação

Todas as rotas (exceto `/auth/login`) requerem autenticação via JWT:

```
Authorization: Bearer <seu_token_jwt>
```

## 🌍 Deploy (Railway)

1. Conecte o repositório no Railway
2. Configure as variáveis de ambiente
3. O deploy será automático!

Variáveis necessárias:
```
DATABASE_URL=postgresql://...
JWT_SECRET=...
CLOUDINARY_URL=...
```
