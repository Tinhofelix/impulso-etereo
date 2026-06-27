import streamlit as st
import sqlite3
import random
import time

# Configuração da página idêntica à original
st.set_page_config(page_title="Impulso Etéreo", page_icon="🔮", layout="wide")

# Inicialização profissional do Banco de Dados
def verificar_banco():
    conn = sqlite3.connect("aether_drive.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            nome TEXT,
            tipo TEXT,
            cpf TEXT,
            verificado TEXT,
            biometria TEXT,
            saldo REAL
        )
    """)
    conn.commit()
    conn.close()

verificar_banco()

# --- ESTADO DA SESSÃO (Para lembrar quem está logado) ---
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

# --- MENU LATERAL IDÊNTICO À FOTO ---
st.sidebar.title("Impulso Etéreo")
st.sidebar.markdown("---")
pagina = st.sidebar.radio("Navegação", ["Login / Cadastro", "Painel Passageiro", "Painel Administrador"])
st.sidebar.markdown("---")

# Exibe o status do usuário logado no menu lateral
if st.session_state.usuario_logado:
    st.sidebar.success(f"👤 Logado: {st.session_state.usuario_logado['nome']}")
else:
    st.sidebar.write("Nenhum usuário logado.")

st.sidebar.markdown("---")
# Indicadores técnicos do painel que estavam na foto
st.sidebar.code("📁 Banco: aether_drive.db")
st.sidebar.code("🛠️ Demonstração administrativa do Senhor: aether_BR26")

# --- 1. TELA DE LOGIN / CADASTRO COM AS DUAS COLUNAS DA FOTO ---
if pagina == "Login / Cadastro":
    st.caption("Autenticação com CPF + validação biométrica facial (selfie simulada).")
    
    col1, col2 = st.columns(2)
    
    # Coluna 1: Entrar na plataforma
    with col1:
        st.header("Entrar")
        cpf_login = st.text_input("CPF cadastrado", "000.000.000-00", key="login_cpf")
        
        if st.button("Entrar na plataforma", use_container_width=True, type="primary"):
            conn = sqlite3.connect("aether_drive.db")
            cursor = conn.cursor()
            cursor.execute("SELECT nome, tipo, saldo FROM usuarios WHERE cpf = ?", (cpf_login,))
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                st.session_state.usuario_logado = {"nome": resultado[0], "tipo": resultado[1], "saldo": resultado[2]}
                st.success(f"👋 Bem-vindo de volta, {resultado[0]}!")
                st.rerun()
            else:
                st.error("❌ CPF não encontrado. Faça o cadastro ao lado primeiro.")

    # Coluna 2: Novo Cadastro Completo
    with col2:
        st.header("Novo cadastro")
        nome_novo = st.text_input("Nome completo", "pedro felix")
        # Escrevendo "passenger" para evitar conflito com filtros de tradução do navegador
        tipo_novo = st.selectbox("Tipo de conta", ["passenger", "motorista"])
        cpf_novo = st.text_input("CPF", "000.000.000-00", key="cadastro_cpf")
        selfie_novo = st.text_input("Token da Selfie (biometria)", "selfie_pedro_ok")
        saldo_inicial = st.number_input("Saldo inicial (passageiro)", value=50.00, step=10.00)
        
        if st.button("Cadastrar e Validar por IA", use_container_width=True):
            with st.spinner("IA executando prova de vida e checagem de antecedentes..."):
                time.sleep(1.5)
                
                conn = sqlite3.connect("aether_drive.db")
                cursor = conn.cursor()
                id_gerado = f"USR-{random.randint(100, 999)}"
                
                cursor.execute("""
                    INSERT OR REPLACE INTO usuarios (id, nome, tipo, cpf, verificado, biometria, saldo)
                    VALUES (?, ?, ?, ?, 'sim', 'sim', ?)
                """, (id_gerado, nome_novo, tipo_novo, cpf_novo, saldo_inicial))
                conn.commit()
                conn.close()
                
                st.success(f"🎉 Conta criada com sucesso! Biometria aprovada para {nome_novo}.")

# --- 2. PAINEL DO PASSAGEIRO ---
elif pagina == "Painel Passageiro":
    st.title("🗺️ Solicitar Viagem Preditiva")
    if st.session_state.usuario_logado:
        st.write(f"Olá {st.session_state.usuario_logado['nome']}, seu saldo atual é de R$ {st.session_state.usuario_logado['saldo']:.2f}")
    
    destino = st.text_input("Para onde vamos hoje?", "Av. Paulista, São Paulo")
    
    if st.button("Chamar App Inteligente", type="primary"):
        st.markdown("---")
        st.subheader("⚡ Correspondência de IA Concluída!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Motorista Selecionado", "Roberto Cruz (★ 4.9)")
        c2.metric("Distância até você", "0.49 km")
        c3.metric("Valor Estimado", "R$ 8,53")
        st.info("🔮 Veículo preditivo em deslocamento. Tempo de espera: *2 minutos*.")

# --- 3. PAINEL ADMINISTRADOR ---
elif pagina == "Painel Administrador":
    st.title("📈 Relatório de Ganhos da Plataforma")
    st.write("Acompanhe a sua taxa de 15% como dono em tempo real.")
    
    caixa1, caixa2 = st.columns(2)
    caixa1.metric("Seu Lucro Líquido Retido (15%)", "R$ 1,28", delta="Faturamento Ativo")
    caixa2.metric("Repasse Líquido do Motorista (85%)", "R$ 7,25")
    st.success("💰 Transações Pix liquidadas e seguras pelo motor da rede.")