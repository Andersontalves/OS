# 📱 Manual do Usuário - Campo (Telegram Bot)

## 🎯 O Que Você Pode Fazer

Como usuário de **Campo**, você usa o **Bot do Telegram** para criar Ordens de Serviço diretamente do local de atendimento.

---

## 📲 Como Usar o Bot

### **1. Encontrar o Bot no Telegram**

1. Abra o **Telegram** no seu celular
2. Procure pelo bot: **@SeuBotTelegram** (nome será fornecido pelo administrador)
3. Clique em **"Iniciar"** ou envie `/start`

---

## 📋 Como Criar uma O.S

### **Passo a Passo Completo**

#### **1. Iniciar Nova O.S**
- Clique no botão **"📋 Abrir Nova O.S."** no menu do bot

#### **2. Enviar Localização GPS**
- O bot pedirá sua **localização atual**
- Clique em **"📍 Enviar Localização (GPS)"**
- ⚠️ **Importante**: A precisão deve ser inferior a 5 metros
- Se a precisão for maior, tente novamente em área aberta

#### **3. Escolher Cidade**
- Selecione a cidade do atendimento:
  - Salto de Pirapora
  - Votorantim
  - Araçoiaba da Serra
  - Sarapuí
  - Sorocaba
  - Alambarí

#### **4. Escolher Motivo**
- Escolha o motivo da abertura:
  - **Rompimento** (ver instruções especiais abaixo)
  - **Manutenções** (ver instruções especiais abaixo)
  - Caixa sem sinal
  - Ampliação de atendimento
  - Sinal Alto

---

## 🔧 O.S de Rompimento

Se você escolher **"Rompimento"** como motivo:

1. **Prazo em Horas**: Digite quantas horas para resolução (ex.: `2` para 2 horas)
2. **Porta(s) da Placa/OLT**: 
   - Digite a porta (ex.: `0/1/1`)
   - **Você pode adicionar múltiplas portas** separadas por vírgula (ex.: `0/1/1, 0/1/2, 0/1/3`)
3. **Foto do Power Meter**: Envie a foto do power meter
4. **Foto do Rompimento**: Envie a foto do local do rompimento
5. **Confirmação**: Revise os dados e confirme

**⚠️ Não será pedido**: Print da O.S e PPPOE

---

## ⚙️ O.S de Manutenções

Se você escolher **"Manutenções"** como motivo:

1. **Prazo em Horas**: Digite quantas horas para resolução (ex.: `4` para 4 horas)
2. **Porta(s) da Placa/OLT**: 
   - Digite a porta (ex.: `0/1/1`)
   - **Você pode adicionar múltiplas portas** separadas por vírgula (ex.: `0/1/1, 0/1/2`)
3. **Foto do Power Meter**: Envie a foto do power meter
4. **Foto do Local da Manutenção**: Envie a foto do local onde será feita a manutenção
5. **PPPOE**: Digite o PPPOE do cliente
6. **Confirmação**: Revise os dados e confirme

**⚠️ Não será pedido**: Print da O.S

---

## 📋 O.S Normal

Se você escolher outro motivo (Caixa sem sinal, Ampliação, Sinal Alto):

1. **Foto do Power Meter**: Envie a foto
2. **Foto da Caixa**: Envie a foto da caixa
3. **Print da O.S**: Envie o print com nome/endereço do cliente
4. **PPPOE**: Digite o PPPOE do cliente
5. **Confirmação**: Revise os dados e confirme

---

## ✅ Confirmação e Envio

Após preencher todos os dados:

1. O bot mostrará um **resumo** da O.S
2. Revise os dados
3. Clique em **"✅ Confirmar"** para criar a O.S
4. Você receberá o **número da O.S** criada

---

## 🕐 Ver Hora Atual

- Envie o comando `/hora` ou `/relogio` para ver a hora atual do Brasil

---

## ❌ Cancelar Operação

A qualquer momento, você pode:
- Clicar em **"❌ Cancelar Operação"** para cancelar e voltar ao menu

---

## 💡 Dicas Importantes

### **Localização GPS**:
- ⚠️ **Sempre envie a localização GPS** - é obrigatório
- Use em área aberta para melhor precisão
- Se a precisão for maior que 5 metros, tente novamente

### **Múltiplas Portas**:
- Para **Rompimento** ou **Manutenções**, você pode informar várias portas
- Separe por vírgula: `0/1/1, 0/1/2, 0/1/3`
- Todas as portas serão salvas e aparecerão nos detalhes da O.S

### **Fotos**:
- Tire fotos claras e bem iluminadas
- Para **Rompimento**: foto do local do rompimento
- Para **Manutenções**: foto do local onde será feita a manutenção
- Para **O.S Normal**: foto da caixa

### **Prazo**:
- Digite apenas o número de horas (ex.: `2`, `4`, `8`)
- O sistema calculará automaticamente o prazo final
- O tempo restante será exibido no dashboard

---

## 🆘 Problemas ou Dúvidas?

### **Bot não responde**:
- Verifique sua conexão com a internet
- Tente enviar `/start` novamente

### **Localização não aceita**:
- Saia para área aberta
- Aguarde alguns segundos e tente novamente
- A precisão deve ser menor que 5 metros

### **Erro ao criar O.S**:
- Verifique se preencheu todos os campos obrigatórios
- Tente novamente
- Se persistir, entre em contato com o administrador

---

## 📞 Suporte

Para problemas técnicos ou dúvidas, entre em contato com o **Administrador do Sistema**.

---

**Última atualização**: Janeiro 2026
