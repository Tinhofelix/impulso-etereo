import streamlit as st
import random
import time

# Configuração da página idêntica à original
st.set_page_config(page_title="Impulso Etéreo", page_icon="🔮", layout="wide")

# --- ESTADO DA SESSÃO (Banco de Dados na Memória da Nuvem) ---
if "banco_usuarios" not in st.session_state:
    st.session_state.banco_usuarios = {
        "17484830720": {"nome": "Pedro Felix da Silva", "tipo": "passageiro", "saldo": 50.00},
        "19399003795": {"nome": "Usuário Teste", "tipo": "passageiro", "saldo": 50.00}
    }

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

# --- MENU LATERAL IDÊNTICO ---
st.sidebar.title("Impulso Etéreo")
st.sidebar.markdown("---")
pagina = st.sidebar.radio("Navegação", ["Login / Cadastro", "Painel Passageiro", "Painel Administrador"])
st.sidebar.markdown("---")

if st.session_state.usuario_logado:
    st.sidebar.success(f"👤 Logado: {st.session_state.usuario_logado['nome']}")
else:
    st.sidebar.write("Nenhum usuário logado.")

st.sidebar.markdown("---")
st.sidebar.code("🌐 Banco: Nuvem Ativa")
st.sidebar.code("🛠️ Demonstração: aether_BR26")

# --- 1. TELA DE LOGIN / CADASTRO ---
if pagina == "Login / Cadastro":
    st.caption("Autenticação com CPF + validação biométrica facial (selfie simulada).")
    
    col1, col2 = st.columns(2)
    
    # Coluna 1: Entrar na plataforma
    with col1:
        st.header("Entrar")
        cpf_login = st.text_input("CPF cadastrado", "", key="login_cpf")
        
        if st.button("Entrar na plataforma", use_container_width=True, type="primary"):
            cpf_limpo = cpf_login.strip().replace(".", "").replace("-", "")
            
            if cpf_limpo in st.session_state.banco_usuarios:
                st.session_state.usuario_logado = st.session_state.banco_usuarios[cpf_limpo]
                st.success(f"👋 Bem-vindo de volta, {st.session_state.banco_usuarios[cpf_limpo]['nome']}!")
                st.rerun()
            else:
                st.error("❌ CPF não encontrado. Faça o cadastro ao lado primeiro ou use seu CPF já pré-configurado.")

    # Coluna 2: Novo Cadastro Completo
    with col2:
        st.header("Novo cadastro")
        nome_novo = st.text_input("Nome completo", "pedro felix")
        tipo_novo = st.selectbox("Tipo de conta", ["passageiro", "motorista"])
        cpf_novo = st.text_input("CPF", "", key="cadastro_cpf")
        selfie_novo = st.text_input("Token da Selfie (biometria)", "selfie_ok")
        saldo_inicial = st.number_input("Saldo inicial (passageiro)", value=50.00, step=10.00)
        
        if st.button("Cadastrar e Validar por IA", use_container_width=True):
            if not cpf_novo:
                st.error("⚠️ Por favor, digite um CPF para realizar o cadastro.")
            else:
                with st.spinner("IA executando prova de vida..."):
                    time.sleep(1.0)
                    cpf_novo_limpo = cpf_novo.strip().replace(".", "").replace("-", "")
                    st.session_state.banco_usuarios[cpf_novo_limpo] = {
                        "nome": nome_novo,
                        "tipo": tipo_novo,
                        "saldo": saldo_inicial
                    }
                    st.success(f"🎉 Conta criada com sucesso! O CPF {cpf_novo} já pode fazer login na coluna da esquerda.")
                    
# --- 2. PAINEL DO PASSAGEIRO ---
elif pagina == "Painel Passageiro":

    st.title("🗺️ Solicitar Viagem Preditiva")

    if st.session_state.usuario_logado:
        st.write(
            f"Olá {st.session_state.usuario_logado['nome']}, "
            f"seu saldo atual é de R$ {st.session_state.usuario_logado['saldo']:.2f}"
        )

        st.markdown("### 💳 Adicionar saldo")

        valor_recarga = st.number_input(
            "Valor da recarga",
            min_value=10.0,
            step=10.0
        )

        if st.button("Adicionar saldo"):
            st.session_state.usuario_logado["saldo"] += valor_recarga
            st.success(f"Recarga de R$ {valor_recarga:.2f} realizada com sucesso!")
            st.rerun()

    else:
        st.warning("⚠️ Você precisa fazer o login na primeira tela para ver seu saldo real.")
        st.write("Olá passageiro, seu saldo demonstrativo é de R$ 50,00")

    destino = st.text_input(
        "Para onde vamos hoje?",
        "Av. Paulista, São Paulo"
    )

    if st.button("Chamar App Inteligente", type="primary"):

        valor_corrida = 8.53

        motoristas = [
            {"nome": "Roberto Cruz", "nota": 4.9, "distancia": 0.49},
            {"nome": "Ana Lima", "nota": 4.8, "distancia": 0.72},
            {"nome": "Carlos Mendes", "nota": 5.0, "distancia": 0.31},
            {"nome": "Juliana Souza", "nota": 4.7, "distancia": 1.10},
        ]

        motorista = min(motoristas, key=lambda m: m["distancia"])

    if not st.session_state.usuario_logado:
        st.error("Faça login antes de solicitar uma viagem.")
        st.stop()

    if st.session_state.usuario_logado["saldo"] >= valor_corrida:
        st.session_state.usuario_logado["saldo"] -= valor_corrida
   else:
        st.error("Saldo insuficiente!")
        st.stop()

  st.markdown("---")
  st.subheader("⚡ Correspondência de IA Concluída!")

  c1, c2, c3 = st.columns(3)

  c1.metric(
      "Motorista Selecionado",
      f'{motorista["nome"]} (★ {motorista["nota"]})'
  )
  
  c2.metric(
      "Distância até você",
      f'{motorista["distancia"]:.2f} km'
       
  )

  c3.metric(
      "Valor Estimado",
      f"R$ {valor_corrida:.2f}"
        
  )

  st.info("🚘 Veículo preditivo em deslocamento. Tempo de espera: 2 minutos.")
# --- 3. PAINEL ADMINISTRADOR ---
elif pagina == "Painel Administrador":
    st.title("📈 Relatório de Ganhos da Plataforma")
    st.write("Acompanhe a sua taxa de 15% como dono em tempo real.")
    
    caixa1, caixa2 = st.columns(2)
    caixa1.metric("Seu Lucro Líquido Retido (15%)", "R$ 1,28", delta="Faturamento Ativo")
    caixa2.metric("Repasse Líquido do Motorista (85%)", "R$ 7,25")
    st.success("💰 Transações Pix liquidadas e seguras pelo motor da rede.") 
