# 📊 Manual do Usuário - Monitoramento

## 🎯 O Que Você Pode Fazer

Como usuário de **Monitoramento**, você tem acesso de **visualização** para acompanhar todas as Ordens de Serviço em tempo real.

---

## 🔐 Como Acessar o Sistema

1. Abra o navegador e acesse: **https://seu-site-render.onrender.com**
2. Faça login com suas credenciais:
   - **Usuário**: (fornecido pelo administrador)
   - **Senha**: (fornecida pelo administrador)
3. Clique em **"Entrar"**

---

## 📋 Funcionalidades Disponíveis

### 1. **Dashboard** (Página Inicial)

Ao fazer login, você verá o **Dashboard** com:

- **Estatísticas Gerais**:
  - Quantidade de O.S Aguardando
  - Quantidade de O.S Em Andamento
  - Quantidade de O.S Concluídas
  - Quantidade de O.S sem sinal

- **Seção de Rompimento e Manutenções**:
  - O.S de Rompimento (Aguardando e Em Andamento)
  - O.S de Manutenções (Aguardando e Em Andamento)
  - Tabela com detalhes: Prazo, Tempo Restante, Porta Placa/OLT, etc.

- **Tabela de O.S Normais**:
  - Lista todas as O.S normais com status, técnicos, cidade, etc.

### 2. **Ordens de Serviço**

Clique em **"Ordens de Serviço"** no menu para ver a lista completa.

#### **Filtros Disponíveis**:
- **Status**: Filtrar por Aguardando, Em Andamento ou Concluído
- Clique em **"Aplicar Filtros"** para atualizar a lista

#### **Visualizar Detalhes**:
- Clique no botão **"Ver Detalhes"** de qualquer O.S
- Você verá:
  - Status da O.S
  - Motivo de abertura
  - Localização (com link para Google Maps)
  - **Fotos**:
    - **O.S Normal**: Power Meter, Caixa, Print O.S (se disponível)
    - **Rompimento**: Foto do Rompimento (não tem Power Meter nem Print O.S)
    - **Manutenções**: Foto do Local da Manutenção (não tem Power Meter nem Print O.S)
    - Comprovação (quando finalizada)
  - Técnico de Campo e Executor
  - PPPOE (disponível apenas para O.S Normal e Manutenções - não aparece para Rompimento)
  - Prazo e Tempo Restante (apenas para Rompimento/Manutenções)
  - Porta(s) Placa/OLT (todas as portas listadas - pode ter múltiplas portas separadas por vírgula)
  - Datas (Criado, Iniciado, Concluído) - todas no horário do Brasil
  - Tempos (Espera, Execução, Total)

---

## ⚠️ O Que Você NÃO Pode Fazer

- ❌ **Não pode assumir** O.S
- ❌ **Não pode finalizar** O.S
- ❌ **Não pode editar** O.S
- ❌ **Não pode excluir** O.S
- ❌ **Não pode gerenciar** usuários

**Você tem acesso somente para visualização e monitoramento.**

---

## 💡 Dicas de Uso

### **Acompanhar O.S de Rompimento/Manutenções**:
1. No Dashboard, vá até a seção **"Rompimento e Manutenções"**
2. Veja o **Prazo** definido (ex: 4h) e o **Tempo Restante** em tempo real (atualiza automaticamente)
3. O **Tempo Restante** nunca será maior que o **Prazo** definido
4. O.S com prazo vencido aparecem em vermelho
5. Clique em **"Ver Detalhes"** para ver todas as portas afetadas (pode ter múltiplas portas)
6. **Diferenças importantes**:
   - **Rompimento**: Não tem Power Meter, Print O.S nem PPPOE
   - **Manutenções**: Não tem Power Meter nem Print O.S, mas tem PPPOE

### **Filtrar O.S por Status**:
1. Vá em **"Ordens de Serviço"**
2. Selecione o status desejado no filtro
3. Clique em **"Aplicar Filtros"**

### **Atualizar Dados**:
- Clique no botão **"🔄 Atualizar"** para recarregar os dados
- O Dashboard atualiza automaticamente a cada minuto

---

## 📱 Acessar pelo Celular

O sistema funciona perfeitamente no celular! Basta acessar a mesma URL pelo navegador do celular.

---

## 🆘 Problemas ou Dúvidas?

Entre em contato com o **Administrador do Sistema**.

---

**Última atualização**: Janeiro 2026
