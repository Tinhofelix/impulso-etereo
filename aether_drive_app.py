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
# BANCO DE DADOS (MEMÓRIA)
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
            "distancia": 0.4
        },

        "22222222222": {
            "cpf": "22222222222",
            "nome": "Ana Lima",
            "tipo": "motorista",
            "saldo": 0.0,
            "nota": 4.8,
            "distancia": 0.8
        }

    }

# =====================================
# USUÁRIO LOGADO
# =====================================

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

# =====================================
# HISTÓRICO
# =====================================

if "historico" not in st.session_state:
    st.session_state.historico = []

# =====================================
# CONFIGURAÇÕES DA EMPRESA
# =====================================

if "taxa_empresa" not in st.session_state:
    st.session_state.taxa_empresa = 15

if "faturamento_empresa" not in st.session_state:
    st.session_state.faturamento_empresa = 0.0

# =====================================
# MENU LATERAL
# =====================================

st.sidebar.title("🚖 Impulso Etéreo")

st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "Login / Cadastro",
        "Painel Passageiro",
        "Painel Motorista",
        "Painel Administrador"
    ]
)

st.sidebar.markdown("---")

if st.session_state.usuario_logado:

    usuario = st.session_state.usuario_logado

    st.sidebar.success(
        f"👤 {usuario['nome']}"
    )

    st.sidebar.write(
        f"Tipo: {usuario['tipo'].capitalize()}"
    )

    if st.sidebar.button("🚪 Sair"):

        st.session_state.usuario_logado = None

        st.success("Logout realizado com sucesso!")

        st.rerun()

else:

    st.sidebar.info("Nenhum usuário logado.")

st.sidebar.markdown("---")

st.sidebar.metric(
    "Taxa da Plataforma",
    f"{st.session_state.taxa_empresa}%"
)

st.sidebar.metric(
    "Faturamento",
    f"R$ {st.session_state.faturamento_empresa:.2f}"
)

st.sidebar.markdown("---")

st.sidebar.caption("Impulso Etéreo • Versão 2.0"

# =====================================
# LOGIN / CADASTRO
# =====================================

if pagina == "Login / Cadastro":

    st.title("🔐 Login e Cadastro")

    col1, col2 = st.columns(2)

    # ==========================
    # LOGIN
    # ==========================

    with col1:

        st.subheader("Entrar")

        cpf_login = st.text_input(
            "CPF",
            key="cpf_login"
        )

        if st.button(
            "Entrar",
            use_container_width=True,
            type="primary"
        ):

            cpf_login = cpf_login.strip()

            if cpf_login in st.session_state.usuarios:

                st.session_state.usuario_logado = (
                    st.session_state.usuarios[cpf_login]
                )

                st.success(
                    f"Bem-vindo, {st.session_state.usuario_logado['nome']}!"
                )

                st.rerun()

            else:

                st.error("CPF não encontrado.")

    # ==========================
    # CADASTRO
    # ==========================

    with col2:

        st.subheader("Novo Cadastro")

        nome = st.text_input(
            "Nome completo"
        )

        cpf = st.text_input(
            "CPF",
            key="cpf_cadastro"
        )

        tipo = st.selectbox(
            "Tipo de conta",
            [
                "passageiro",
                "motorista"
            ]
        )

        if st.button(
            "Cadastrar",
            use_container_width=True
        ):

            cpf = cpf.strip()

            if nome == "" or cpf == "":

                st.warning(
                    "Preencha todos os campos."
                )

            elif cpf in st.session_state.usuarios:

                st.error(
                    "Este CPF já está cadastrado."
                )

            else:

                novo_usuario = {

                    "cpf": cpf,
                    "nome": nome,
                    "tipo": tipo,
                    "saldo": 50.0 if tipo == "passageiro" else 0.0,
                    "nota": 5.0 if tipo == "motorista" else 0.0,
                    "distancia": round(
                        random.uniform(0.3, 3.0),
                        2
                    )

                }

                st.session_state.usuarios[cpf] = novo_usuario

                st.success(
                    "Cadastro realizado com sucesso!"
                )

                st.balloons()
                   
