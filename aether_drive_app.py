import streamlit as st
import random
import time

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================

st.set_page_config(
    page_title="Impulso Etéreo",
    page_icon="🚖",
    layout="wide"
)

# =====================================
# ESTADOS DA SESSÃO
# =====================================

if "usuarios" not in st.session_state:

    st.session_state.usuarios = {

        "17484830720": {
            "cpf": "17484830720",
            "nome": "Pedro Felix da Silva",
            "tipo": "passageiro",
            "saldo": 50.00,
            "nota": 5.0,
            "distancia": 0
        },

        "11111111111": {
            "cpf": "11111111111",
            "nome": "Roberto Cruz",
            "tipo": "motorista",
            "saldo": 0.0,
            "nota": 4.9,
            "distancia": 0.4,
            "online": True
        },

        "22222222222": {
            "cpf": "22222222222",
            "nome": "Ana Lima",
            "tipo": "motorista",
            "saldo": 0.0,
            "nota": 4.8,
            "distancia": 0.8,
            "online": True
        }

    }

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "historico" not in st.session_state:
    st.session_state.historico = []

if "extrato" not in st.session_state:
    st.session_state.extrato = []

if "notificacoes" not in st.session_state:
    st.session_state.notificacoes = []

if "config" not in st.session_state:

    st.session_state.config = {

        "nome_empresa": "Impulso Etéreo",
        "versao": "2.2",
        "taxa_empresa": 15,
        "faturamento": 0.0,
        "cidade": "São Paulo",
        "aceitar_corridas": True,
        "modo_manutencao": False

    }

# =====================================
# MODO MANUTENÇÃO
# =====================================

if st.session_state.config["modo_manutencao"]:

    st.error("🚧 Plataforma em manutenção.")

    st.stop()

# =====================================
# MENU LATERAL
# =====================================

st.sidebar.title(f"🚖 {st.session_state.config['nome_empresa']}")

st.sidebar.caption(
    f"Versão {st.session_state.config['versao']}"
)

st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação",
    (
        "Login / Cadastro",
        "Painel Passageiro",
        "Painel Motorista",
        "Painel Administrador"
    )
)

st.sidebar.markdown("---")

if st.session_state.usuario_logado:

    usuario = st.session_state.usuario_logado

    st.sidebar.success(f"👤 {usuario['nome']}")

    st.sidebar.write(
        f"Tipo: {usuario['tipo'].capitalize()}"
    )

    st.sidebar.metric(
        "💰 Saldo",
        f"R$ {usuario['saldo']:.2f}"
    )

    if usuario["tipo"] == "motorista":

        st.sidebar.metric(
            "⭐ Avaliação",
            usuario["nota"]
        )

    if st.sidebar.button("🚪 Sair"):

        st.session_state.usuario_logado = None

        st.rerun()

else:

    st.sidebar.info("Nenhum usuário logado.")

st.sidebar.markdown("---")

st.sidebar.metric(
    "💵 Taxa da Plataforma",
    f"{st.session_state.config['taxa_empresa']}%"
)

st.sidebar.metric(
    "📈 Faturamento",
    f"R$ {st.session_state.config['faturamento']:.2f}"
)

st.sidebar.metric(
    "🔔 Notificações",
    len(st.session_state.notificacoes)
)

st.sidebar.markdown("---")

st.sidebar.caption(
    f"📍 {st.session_state.config['cidade']}"
)


