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

# =====================================
# LOGIN / CADASTRO
# =====================================

if pagina == "Login / Cadastro":

    st.title("🔐 Login e Cadastro")

    col1, col2 = st.columns(2)

    # =====================================
    # LOGIN
    # =====================================

    with col1:

        st.subheader("Entrar")

        cpf_login = st.text_input(
            "CPF",
            key="cpf_login"
        ).strip()

        if st.button(
            "Entrar",
            use_container_width=True,
            type="primary"
        ):

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

    # =====================================
    # CADASTRO
    # =====================================

    with col2:

        st.subheader("Novo Cadastro")

        nome = st.text_input(
            "Nome completo",
            key="novo_nome"
        )

        cpf = st.text_input(
            "CPF",
            key="novo_cpf"
        ).strip()

        tipo = st.selectbox(
            "Tipo de conta",
            (
                "passageiro",
                "motorista"
            )
        )

        if st.button(
            "Cadastrar",
            use_container_width=True
        ):

            if nome == "" or cpf == "":

                st.warning("Preencha todos os campos.")

            elif cpf in st.session_state.usuarios:

                st.error("Este CPF já está cadastrado.")

            else:

                novo_usuario = {

                    "cpf": cpf,

                    "nome": nome,

                    "tipo": tipo,

                    "saldo": 50.0 if tipo == "passageiro" else 0.0,

                    "nota": 5.0 if tipo == "motorista" else 0.0,

                    "distancia": round(
                        random.uniform(0.3, 5.0),
                        2
                    ),

                    "online": True

                }

                st.session_state.usuarios[cpf] = novo_usuario

                st.session_state.notificacoes.append(
                    f"Novo usuário cadastrado: {nome}"
                )

                st.success("Cadastro realizado com sucesso!")

                st.balloons()

                st.rerun()

    st.markdown("---")

    st.subheader("📊 Resumo da Plataforma")

    passageiros = sum(
        1 for u in st.session_state.usuarios.values()
        if u["tipo"] == "passageiro"
    )

    motoristas = sum(
        1 for u in st.session_state.usuarios.values()
        if u["tipo"] == "motorista"
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "👥 Passageiros",
        passageiros
    )

    c2.metric(
        "🚗 Motoristas",
        motoristas
    )

# =====================================
# PAINEL DO PASSAGEIRO
# =====================================

elif pagina == "Painel Passageiro":

    st.title("🚖 Painel do Passageiro")

    if not st.session_state.usuario_logado:
        st.warning("Faça login primeiro.")
        st.stop()

    usuario = st.session_state.usuario_logado

    if usuario["tipo"] != "passageiro":
        st.error("Esta conta não pertence a um passageiro.")
        st.stop()

    st.success(f"Olá, {usuario['nome']}")

    col1, col2 = st.columns(2)

    col1.metric(
        "💰 Saldo",
        f"R$ {usuario['saldo']:.2f}"
    )

    col2.metric(
        "🚖 Corridas",
        len(st.session_state.historico)
    )

    st.markdown("---")

    # =====================================
    # RECARGA
    # =====================================

    st.subheader("💳 Adicionar Saldo")

    valor_recarga = st.number_input(
        "Valor da Recarga",
        min_value=10.0,
        value=20.0,
        step=10.0
    )

    if st.button("Adicionar Saldo"):

        usuario["saldo"] += valor_recarga

        st.session_state.extrato.append({

            "tipo": "Recarga",

            "valor": valor_recarga

        })

        st.success(
            f"Saldo atualizado para R$ {usuario['saldo']:.2f}"
        )

        st.rerun()

    st.markdown("---")

    # =====================================
    # SOLICITAR CORRIDA
    # =====================================

    st.subheader("📍 Solicitar Corrida")

    origem = st.text_input(
        "Origem",
        "Minha localização"
    )

    destino = st.text_input(
        "Destino",
        "Av. Paulista"
    )

    valor_corrida = round(
        random.uniform(8, 30),
        2
    )

    st.metric(
        "Valor Estimado",
        f"R$ {valor_corrida:.2f}"
    )

    if st.button(
        "🚖 Chamar Motorista",
        type="primary"
    ):

        if usuario["saldo"] < valor_corrida:

            st.error("Saldo insuficiente.")

            st.stop()

        motoristas = [

            motorista

            for motorista in st.session_state.usuarios.values()

            if motorista["tipo"] == "motorista"

            and motorista.get("online", True)

        ]

        if len(motoristas) == 0:

            st.error("Nenhum motorista disponível.")

            st.stop()

        motorista = min(

            motoristas,

            key=lambda m: m["distancia"]

        )

        taxa = (
            valor_corrida *
            st.session_state.config["taxa_empresa"]
            / 100
        )

        ganho_motorista = valor_corrida - taxa

        usuario["saldo"] -= valor_corrida

        motorista["saldo"] += ganho_motorista

        st.session_state.config["faturamento"] += taxa

        viagem = {

            "passageiro": usuario["nome"],

            "motorista": motorista["nome"],

            "origem": origem,

            "destino": destino,

            "valor": valor_corrida

        }

        st.session_state.historico.append(viagem)

        st.session_state.extrato.append({

            "tipo": "Corrida",

            "valor": -valor_corrida

        })

        st.success("Motorista encontrado!")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Motorista",
            motorista["nome"]
        )

        c2.metric(
            "⭐ Nota",
            motorista["nota"]
        )

        c3.metric(
            "📍 Distância",
            f"{motorista['distancia']} km"
        )

        st.info("🚘 Motorista a caminho...")

        progresso = st.progress(0)

        etapas = [

            "📲 Procurando motorista...",

            "✅ Motorista aceitou.",

            "🚗 Motorista indo até você.",

            "📍 Motorista chegou.",

            "👤 Passageiro embarcou.",

            "🛣️ Viagem iniciada.",

            "🏁 Chegando ao destino.",

            "✅ Corrida finalizada."

        ]

        for i, etapa in enumerate(etapas):

            progresso.progress((i + 1) / len(etapas))

            st.write(etapa)

            time.sleep(0.7)

        st.success("🎉 Corrida concluída!")

        st.metric(
            "Novo Saldo",
            f"R$ {usuario['saldo']:.2f}"
        )

    st.markdown("---")

    # =====================================
    # HISTÓRICO
    # =====================================

    st.subheader("📜 Histórico")

    if len(st.session_state.historico) == 0:

        st.info("Nenhuma corrida realizada.")

    else:

        for viagem in reversed(st.session_state.historico):

            if viagem["passageiro"] == usuario["nome"]:

                st.write(

                    f"🚖 {viagem['origem']} ➜ {viagem['destino']}"

                )

                st.caption(

                    f"Motorista: {viagem['motorista']} | "

                    f"Valor: R$ {viagem['valor']:.2f}"

                )

# =====================================
# PAINEL DO MOTORISTA
# =====================================

elif pagina == "Painel Motorista":

    st.title("🚗 Painel do Motorista")

    if not st.session_state.usuario_logado:
        st.warning("Faça login primeiro.")
        st.stop()

    usuario = st.session_state.usuario_logado

    if usuario["tipo"] != "motorista":
        st.error("Esta conta não pertence a um motorista.")
        st.stop()

    st.success(f"Bem-vindo, {usuario['nome']}!")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💰 Saldo",
        f"R$ {usuario['saldo']:.2f}"
    )

    c2.metric(
        "⭐ Nota",
        f"{usuario['nota']:.1f}"
    )

    c3.metric(
        "📍 Distância",
        f"{usuario['distancia']} km"
    )

    st.markdown("---")

    # ===============================
    # STATUS ONLINE
    # ===============================

    usuario["online"] = st.toggle(
        "Motorista Online",
        value=usuario.get("online", True)
    )

    if usuario["online"]:
        st.success("🟢 Você está disponível para receber corridas.")
    else:
        st.warning("🔴 Você está Offline.")

    st.markdown("---")

    # ===============================
    # ESTATÍSTICAS
    # ===============================

    total_corridas = 0
    total_ganhos = 0.0

    for viagem in st.session_state.historico:

        if viagem["motorista"] == usuario["nome"]:

            total_corridas += 1

            taxa = (
                viagem["valor"]
                * st.session_state.config["taxa_empresa"]
                / 100
            )

            total_ganhos += viagem["valor"] - taxa

    c1, c2 = st.columns(2)

    c1.metric(
        "🚖 Corridas",
        total_corridas
    )

    c2.metric(
        "💵 Ganhos",
        f"R$ {total_ganhos:.2f}"
    )

    st.markdown("---")

    # ===============================
    # HISTÓRICO
    # ===============================

    st.subheader("📜 Histórico")

    encontrou = False

    for viagem in reversed(st.session_state.historico):

        if viagem["motorista"] == usuario["nome"]:

            encontrou = True

            with st.container():

                st.write(
                    f"👤 Passageiro: {viagem['passageiro']}"
                )

                st.write(
                    f"📍 Origem: {viagem['origem']}"
                )

                st.write(
                    f"🏁 Destino: {viagem['destino']}"
                )

                st.write(
                    f"💰 Valor: R$ {viagem['valor']:.2f}"
                )

                st.markdown("---")

    if not encontrou:

        st.info("Nenhuma corrida realizada ainda.")

    st.markdown("---")

    # ===============================
    # ALTERAR DISTÂNCIA
    # ===============================

    st.subheader("📍 Atualizar Distância")

    nova_distancia = st.slider(
        "Distância até o próximo passageiro (km)",
        min_value=0.1,
        max_value=10.0,
        value=float(usuario["distancia"]),
        step=0.1
    )

    if st.button("Atualizar Distância"):

        usuario["distancia"] = round(
            nova_distancia,
            2
        )

        st.success("Distância atualizada!")

        st.rerun()

    st.markdown("---")

    # ===============================
    # EXTRATO DO MOTORISTA
    # ===============================

    st.subheader("💳 Resumo Financeiro")

    st.metric(
        "Saldo Atual",
        f"R$ {usuario['saldo']:.2f}"
    )

    st.metric(
        "Ganhos Totais",
        f"R$ {total_ganhos:.2f}"
    )

