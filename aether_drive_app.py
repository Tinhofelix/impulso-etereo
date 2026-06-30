import streamlit as st
import random
import time

# ==========================
# CONFIGURAÇÃO DA PÁGINA
# ==========================
st.set_page_config(
    page_title="Impulso Etéreo",
    page_icon="🚖",
    layout="wide"
)

# ==========================
# BANCO DE DADOS (MEMÓRIA)
# ==========================
if "usuarios" not in st.session_state:
    st.session_state.usuarios = {
        "17484830720": {
            "nome": "Pedro Felix da Silva",
            "tipo": "passageiro",
            "saldo": 50.0
        },
        "11111111111": {
            "nome": "Roberto Cruz",
            "tipo": "motorista",
            "saldo": 0.0,
            "nota": 4.9,
            "distancia": 0.49
        },
        "22222222222": {
            "nome": "Ana Lima",
            "tipo": "motorista",
            "saldo": 0.0,
            "nota": 4.8,
            "distancia": 0.72
        },
        "33333333333": {
            "nome": "Carlos Mendes",
            "tipo": "motorista",
            "saldo": 0.0,
            "nota": 5.0,
            "distancia": 0.31
        }
    }

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "taxa_empresa" not in st.session_state:
    st.session_state.taxa_empresa = 15

# ==========================
# MENU LATERAL
# ==========================
st.sidebar.title("🚖 Impulso Etéreo")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Menu",
    [
        "Login / Cadastro",
        "Painel Passageiro",
        "Painel Motorista",
        "Painel Administrador"
    ]
)

st.sidebar.markdown("---")

if st.session_state.usuario_logado:
    st.sidebar.success(
        f"Logado como:\n\n{st.session_state.usuario_logado['nome']}"
    )
else:
    st.sidebar.warning("Nenhum usuário logado.")

st.sidebar.markdown("---")
st.sidebar.caption("Versão 2.0")

# ==========================
# LOGIN E CADASTRO
# ==========================
if pagina == "Login / Cadastro":

    st.title("🔐 Login e Cadastro")

    col1, col2 = st.columns(2)

    # LOGIN
    with col1:

        st.subheader("Entrar")

        cpf_login = st.text_input(
            "CPF",
            key="cpf_login"
        )

        if st.button("Entrar", use_container_width=True):

            cpf = cpf_login.replace(".", "").replace("-", "").strip()

            if cpf in st.session_state.usuarios:

                st.session_state.usuario_logado = (
                    st.session_state.usuarios[cpf]
                )

                st.success(
                    f"Bem-vindo {st.session_state.usuario_logado['nome']}!"
                )

                st.rerun()

            else:
                st.error("CPF não encontrado.")

    # CADASTRO
    with col2:

        st.subheader("Novo Cadastro")

        nome = st.text_input("Nome completo")

        tipo = st.selectbox(
            "Tipo",
            [
                "passageiro",
                "motorista"
            ]
        )

        cpf = st.text_input(
            "CPF",
            key="cpf_cadastro"
        )

        saldo = st.number_input(
            "Saldo inicial",
            min_value=0.0,
            value=50.0
        )

        if st.button(
            "Cadastrar",
            use_container_width=True
        ):

            cpf_limpo = cpf.replace(".", "").replace("-", "").strip()

            if cpf_limpo == "":
                st.error("Digite um CPF.")
            elif cpf_limpo in st.session_state.usuarios:
                st.error("Esse CPF já está cadastrado.")
            else:

                st.session_state.usuarios[cpf_limpo] = {
                    "nome": nome,
                    "tipo": tipo,
                    "saldo": saldo
                }

                st.success("Cadastro realizado com sucesso!")
# ==========================
# PAINEL DO PASSAGEIRO
# ==========================

elif pagina == "Painel Passageiro":

    st.title("🚖 Painel do Passageiro")

    if not st.session_state.usuario_logado:
        st.warning("Faça login primeiro.")
        st.stop()

    if st.session_state.usuario_logado["tipo"] != "passageiro":
        st.error("Esta conta não é de passageiro.")
        st.stop()

    usuario = st.session_state.usuario_logado

    st.success(f"Olá, {usuario['nome']}")

    st.metric(
        "💰 Saldo",
        f"R$ {usuario['saldo']:.2f}"
    )

    st.markdown("---")

    st.subheader("💳 Adicionar saldo")

    valor_recarga = st.number_input(
        "Valor",
        min_value=10.0,
        value=10.0,
        step=10.0
    )

    if st.button("Adicionar saldo"):

        usuario["saldo"] += valor_recarga

        st.success(
            f"Saldo atualizado para R$ {usuario['saldo']:.2f}"
        )

        st.rerun()

    st.markdown("---")

    st.subheader("📍 Solicitar viagem")

    origem = st.text_input(
        "Origem",
        "Minha localização"
    )

    destino = st.text_input(
        "Destino",
        "Av. Paulista"
    )

    valor_corrida = round(random.uniform(8, 30), 2)

    st.metric(
        "Valor estimado",
        f"R$ {valor_corrida:.2f}"
    )

    if st.button("🚖 Chamar motorista", type="primary"):

        if usuario["saldo"] < valor_corrida:
            st.error("Saldo insuficiente.")
            st.stop()

        motoristas = []

        for dados in st.session_state.usuarios.values():
            if dados["tipo"] == "motorista":
                motoristas.append(dados)

        motorista = min(
            motoristas,
            key=lambda m: m["distancia"]
        )

        usuario["saldo"] -= valor_corrida

        taxa = (
            valor_corrida *
            st.session_state.taxa_empresa / 100
        )

        ganho_motorista = valor_corrida - taxa

        motorista["saldo"] += ganho_motorista

        if "historico" not in st.session_state:
            st.session_state.historico = []

        st.session_state.historico.append({
            "passageiro": usuario["nome"],
            "motorista": motorista["nome"],
            "origem": origem,
            "destino": destino,
            "valor": valor_corrida
        })

        st.success("Motorista encontrado!")

        # ==========================
# STATUS DA CORRIDA
# ==========================

st.markdown("---")
st.subheader("📲 Status da Corrida")

status = [
    "🔍 Procurando motorista...",
    "✅ Motorista aceitou a corrida",
    "🚘 Motorista a caminho",
    "📍 Motorista chegou ao local",
    "👤 Passageiro embarcou",
    "🏁 Corrida finalizada"
]

barra = st.progress(0)

for i, etapa in enumerate(status):
    barra.progress((i + 1) / len(status))
    st.write(etapa)
    time.sleep(0.8)

st.success("🎉 Corrida concluída com sucesso!")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Motorista",
    motorista["nome"]
)

c2.metric(
    "Nota",
    f"⭐ {motorista['nota']}"
)

c3.metric(
    "Distância",
    f"{motorista['distancia']} km"
)

        st.info("🚘 O motorista está a caminho.")

        st.success(
            f"Novo saldo: R$ {usuario['saldo']:.2f}"
        )

        st.markdown("---")
        st.subheader("⭐ Avaliar motorista")

        nota = st.slider(
            "Sua avaliação",
            min_value=1,
            max_value=5,
            value=5,
            key="avaliacao_motorista"
        )

        if st.button("Enviar avaliação"):

            motorista["nota"] = round(
                (motorista["nota"] + nota) / 2,
                1
            )

            st.success("Obrigado pela sua avaliação!")

    if "historico" in st.session_state:

        st.markdown("---")
        st.subheader("📜 Histórico")

        for viagem in reversed(st.session_state.historico):

            st.write(
                f"🚖 {viagem['passageiro']} → "
                f"{viagem['destino']} | "
                f"Motorista: {viagem['motorista']} | "
                f"R$ {viagem['valor']:.2f}"
            )
# ==========================
# PAINEL DO MOTORISTA
# ==========================

elif pagina == "Painel Motorista":

    st.title("🚗 Painel do Motorista")

    if not st.session_state.usuario_logado:
        st.warning("Faça login primeiro.")
        st.stop()

    if st.session_state.usuario_logado["tipo"] != "motorista":
        st.error("Esta conta não é de motorista.")
        st.stop()

    motorista = st.session_state.usuario_logado

    st.success(f"Bem-vindo, {motorista['nome']}!")

    st.metric(
        "💰 Saldo Disponível",
        f"R$ {motorista['saldo']:.2f}"
    )

    st.metric(
        "⭐ Avaliação",
        motorista.get("nota", 5.0)
    )

    st.markdown("---")

    st.subheader("📍 Status")

    status = st.selectbox(
        "Disponibilidade",
        [
            "🟢 Online",
            "🔴 Offline"
        ]
    )

    if status == "🟢 Online":
        st.success("Você está disponível para receber corridas.")
    else:
        st.warning("Você está offline.")

    st.markdown("---")

    st.subheader("📊 Estatísticas")

    historico = st.session_state.get("historico", [])

    minhas_corridas = [
        viagem
        for viagem in historico
        if viagem["motorista"] == motorista["nome"]
    ]

    quantidade = len(minhas_corridas)

    ganhos = sum(
        viagem["valor"] *
        (100 - st.session_state.taxa_empresa) / 100
        for viagem in minhas_corridas
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "🚖 Corridas realizadas",
        quantidade
    )

    c2.metric(
        "💵 Ganhos estimados",
        f"R$ {ganhos:.2f}"
    )

    st.markdown("---")

    st.subheader("📜 Histórico")

    if quantidade == 0:

        st.info("Nenhuma corrida realizada ainda.")

    else:

        for viagem in reversed(minhas_corridas):

            st.container()

            st.write(f"👤 Passageiro: {viagem['passageiro']}")
            st.write(f"📍 Origem: {viagem['origem']}")
            st.write(f"🏁 Destino: {viagem['destino']}")
            st.write(f"💰 Valor da corrida: R$ {viagem['valor']:.2f}")

            ganho = (
                viagem["valor"] *
                (100 - st.session_state.taxa_empresa)
                / 100
            )

            st.success(
                f"Recebido: R$ {ganho:.2f}"
            )

            st.markdown("---")
# ==========================
# PAINEL DO ADMINISTRADOR
# ==========================

elif pagina == "Painel Administrador":

    st.title("👑 Painel do Administrador")

    historico = st.session_state.get("historico", [])
    usuarios = st.session_state.usuarios

    passageiros = [
        u for u in usuarios.values()
        if u["tipo"] == "passageiro"
    ]

    motoristas = [
        u for u in usuarios.values()
        if u["tipo"] == "motorista"
    ]

    faturamento = sum(v["valor"] for v in historico)

    lucro = faturamento * st.session_state.taxa_empresa / 100

    st.subheader("📊 Resumo da Plataforma")

    c1, c2 = st.columns(2)

    c1.metric(
        "👥 Passageiros",
        len(passageiros)
    )

    c2.metric(
        "🚗 Motoristas",
        len(motoristas)
    )

    c3, c4 = st.columns(2)

    c3.metric(
        "🚖 Corridas",
        len(historico)
    )

    c4.metric(
        "💰 Faturamento",
        f"R$ {faturamento:.2f}"
    )

    st.metric(
        "🏦 Lucro da Empresa",
        f"R$ {lucro:.2f}"
    )

    st.markdown("---")

    st.subheader("⚙️ Comissão da Plataforma")

    st.session_state.taxa_empresa = st.slider(
        "Comissão (%)",
        min_value=0,
        max_value=30,
        value=st.session_state.taxa_empresa
    )

    st.success(
        f"Comissão atual: {st.session_state.taxa_empresa}%"
    )

    st.markdown("---")

    st.subheader("📜 Histórico de Corridas")

    if len(historico) == 0:

        st.info("Nenhuma corrida realizada.")

    else:

        for viagem in reversed(historico):

            st.write(
                f"🚖 {viagem['passageiro']} "
                f"→ {viagem['destino']}"
            )

            st.write(
                f"👨‍✈️ Motorista: {viagem['motorista']}"
            )

            st.write(
                f"💰 Valor: R$ {viagem['valor']:.2f}"
            )

            st.markdown("---")
