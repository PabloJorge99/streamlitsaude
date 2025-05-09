import streamlit as st
import pandas as pd
from datetime import datetime

# Base de dados simulada
if "users" not in st.session_state:
    st.session_state.users = {
        "rh@empresa.com": "gestor",
        "joao@empresa.com": "funcionario",
        "maria@empresa.com": "funcionario"
    }

if "agendamentos" not in st.session_state:
    st.session_state.agendamentos = []

if "atestados" not in st.session_state:
    st.session_state.atestados = []

# Função de login
def login():
    st.title("Sistema de Saúde Corporativo")
    email = st.text_input("Email corporativo")
    if st.button("Entrar"):
        tipo = st.session_state.users.get(email)
        if tipo:
            st.session_state.email = email
            st.session_state.tipo_usuario = tipo
            st.success(f"Bem-vindo, {tipo.title()}!")
            st.rerun()
        else:
            st.error("Email não cadastrado no sistema.")

# Área do funcionário
def funcionario_view():
    st.title("Área do Funcionário")

    aba = st.sidebar.radio("Menu", [
    "Agendar Consulta", 
    "Atendimento Online", 
    "Meus Agendamentos", 
    "Enviar Atestado",
    "Dicas de Saúde"
])

    if aba == "Agendar Consulta":
        st.subheader("Agendamento de Consulta")
        tipo = st.radio("Tipo de consulta", ["Online", "Presencial"])
        data = st.date_input("Data desejada")
        hora = st.time_input("Horário")
        motivo = st.text_area("Motivo da consulta")

        st.subheader("Escolha sua Especialidade e Médico")

        especialidades = {
            "Clínico Geral": ["Dr. João Silva", "Dra. Camila Rocha"],
            "Cardiologista": ["Dra. Paula Fernandes"],
            "Ortopedista": ["Dr. Lucas Monteiro"],
            "Psicólogo": ["Dra. Ana Souza", "Dr. Rafael Lima"]
        }

        especialidade = st.selectbox("Escolha a especialidade", list(especialidades.keys()))
        medico = st.selectbox("Escolha o médico", especialidades[especialidade])

        st.success(f"Você selecionou {medico} ({especialidade})")


        if st.button("Confirmar Agendamento"):
            st.session_state.agendamentos.append({
                "email": st.session_state.email,
                "tipo": tipo,
                "data": str(data),
                "hora": str(hora),
                "motivo": motivo
            })
            st.success("Consulta agendada com sucesso!")

    elif aba == "Atendimento Online":
        st.subheader("Chat com médico (simulado)")
        st.info("Seu médico entrará em contato no horário agendado.")
        st.text_area("Mensagem", placeholder="Descreva seus sintomas ou dúvidas...")

    elif aba == "Meus Agendamentos":
        st.subheader("Histórico de Agendamentos")
        dados = [a for a in st.session_state.agendamentos if a["email"] == st.session_state.email]
        if dados:
            st.table(pd.DataFrame(dados))
        else:
            st.info("Nenhum agendamento encontrado.")

    elif aba == "Enviar Atestado":
        st.subheader("Envio de Atestado Médico")
        nome_funcionario = st.text_input("Seu nome")
        arquivo_atestado = st.file_uploader("Envie o arquivo do atestado (PDF ou imagem)", type=["pdf", "png", "jpg"])
    
        if st.button("Enviar") and nome_funcionario and arquivo_atestado:
            atestado_data = {
                "nome": nome_funcionario,
                "data_envio": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "nome_arquivo": arquivo_atestado.name,
                "arquivo": arquivo_atestado.getvalue()
            }
    
            if "atestados" not in st.session_state:
                st.session_state.atestados = []
    
            st.session_state.atestados.append(atestado_data)
            st.success("Atestado enviado com sucesso!")


    elif aba == "Dicas de Saúde":
        st.subheader("🩺 Dicas de Saúde por nossos médicos")

        dicas = [
            {
                "titulo": "Importância da Hidratação",
                "conteudo": "Beber pelo menos 2 litros de água por dia melhora o funcionamento do organismo e evita doenças renais.",
                "autor": "Dr. João Silva - Clínico Geral"
            },
            {
                "titulo": "Caminhada diária de 30 minutos",
                "conteudo": "A atividade física regular ajuda no controle do peso e reduz o risco de doenças cardíacas.",
                "autor": "Dra. Paula Fernandes - Cardiologista"
            },
            {
                "titulo": "Sono e produtividade",
                "conteudo": "Dormir de 7 a 8 horas por noite melhora o foco e reduz o estresse.",
                "autor": "Dra. Ana Souza - Psicóloga"
            }
        ]

        for dica in dicas:
            st.markdown(f"### {dica['titulo']}")
            st.write(dica["conteudo"])
            st.caption(f"*{dica['autor']}*")
            st.divider()


# Área do RH
def gestor_view():
    st.title("Painel de Gestão (RH)")

    aba = st.sidebar.radio("Menu", ["Atestados", "Dados de Atendimento"])

    if aba == "Atestados":
        st.subheader("Atestados Recebidos")
    
        if "atestados" in st.session_state and st.session_state.atestados:
            for idx, atestado in enumerate(st.session_state.atestados):
                with st.expander(f"{atestado['nome']} - {atestado['data_envio']}"):
                    st.write(f"Nome do arquivo: {atestado['nome_arquivo']}")
                    st.download_button(
                        label="📥 Baixar Atestado",
                        data=atestado["arquivo"],
                        file_name=atestado["nome_arquivo"]
                    )
        else:
            st.info("Nenhum atestado enviado.")


    elif aba == "Dados de Atendimento":
        st.subheader("Resumo de Agendamentos")
        df = pd.DataFrame(st.session_state.agendamentos)
        if not df.empty:
            resumo = df.groupby("tipo").size().reset_index(name="Quantidade")
            st.table(resumo)
            st.bar_chart(resumo.set_index("tipo"))
        else:
            st.info("Nenhum agendamento registrado.")

# Lógica principal
if "email" not in st.session_state:
    login()
else:
    st.sidebar.image("logo_empresa.png" width = "80px")
    
    if st.session_state.tipo_usuario == "funcionario":
        funcionario_view()
    else:
        gestor_view()

    # Botão de logout
    if st.sidebar.button("Sair"):
        del st.session_state.email
        del st.session_state.tipo_usuario
        st.rerun()
