import streamlit as st
import streamlit.components.v1 as components
from datetime import date, timedelta

# Configurar a página sem o modo wide e definir o ícone
st.set_page_config(
    page_title="Gerar Programação de Atividades",
    page_icon="📅",
    layout="centered"
)

# Adicionar título com ícone
st.title("📅 Gerar Programação de Atividades")

# Adicionando CSS
st.markdown("""
    <style>
    .stTabs [role="tab"] {
        font-size: 1.2rem;
        padding: 10px;
    }
    .stTabs [role="tab"]::before {
        content: '🔍 ';
        margin-right: 5px;
    }
    .stTabs [role="tab"]:nth-child(2)::before {
        content: '📅 ';
    }
    .stTabs [role="tab"]:nth-child(3)::before {
        content: '📊 ';
    }
    .description-div {
        padding: 5px;
        background-color: #cccccc;  /* Cor um pouco mais escura */
        text-align: center;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .generated-table {
        width: 100%;
        border-collapse: collapse.
    }
    .generated-table th, .generated-table td {
        border: 1px solid black.
        padding: 8px.
        text-align: center.  /* Centraliza o texto nas células */
    }
    .generated-table th {
        background-color: #f2f2f2.
    }
    .zebra-striping tbody tr:nth-child(even) {
        background-color: #f9f9f9.
    }
    .zebra-striping tbody tr:nth-child(odd) {
        background-color: #ffffff.
    }
    .header-row {
        background-color: #404040.
        color: white.
    }
    .header-row-description {
        background-color: #5a5a5a.
        color: white.
    }
    </style>
    """, unsafe_allow_html=True)

def load_html(file_path, servidores, atividades, veiculos, primeiro_dia, dias_da_semana, ulsav, supervisao, semana_do_mes, mes_por_extenso, ano):
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()
        # Inserir as listas de servidores, atividades e veículos no HTML
        html = html.replace("const people = [];", f"const people = {servidores};")
        html = html.replace("const activities = [];", f"const activities = {atividades};")
        html = html.replace("const vehicles = [];", f"const vehicles = {veiculos};")
        html = html.replace("const primeiroDia = '';", f"const primeiroDia = '{primeiro_dia}';")
        html = html.replace("const daysOfWeek = [];", f"const daysOfWeek = {dias_da_semana};")
        html = html.replace("const ulsav = '';", f"const ulsav = '{ulsav}';")
        html = html.replace("const supervisao = '';", f"const supervisao = '{supervisao}';")
        html = html.replace("const semanaDoMes = '';", f"const semanaDoMes = '{semana_do_mes}';")
        html = html.replace("const mesPorExtenso = '';", f"const mesPorExtenso = '{mes_por_extenso}';")
        html = html.replace("const ano = '';", f"const ano = '{ano}';")
        return html

def read_items_from_file(file, skip_first_two_lines=False):
    lines = file.readlines()
    if skip_first_two_lines:
        lines = lines[2:]  # Skip the first two lines
    return [line.decode('utf-8', errors='ignore').strip() for line in lines if line.strip()]

def buscar_dados():
    st.markdown("### Carregar Servidores")
    file_servidores = st.file_uploader("Carregar Servidores", type=["txt"], key="servidores")

    servidores = []
    multiselect_servidores = st.empty()

    if file_servidores is not None:
        servidores = read_items_from_file(file_servidores, skip_first_two_lines=True)

    if servidores:
        selected_servidores = multiselect_servidores.multiselect("Selecione os servidores:", servidores, default=servidores)
    else:
        selected_servidores = multiselect_servidores.multiselect("Selecione os servidores:", [])

    st.markdown("---")

    st.markdown("### Carregar Atividades")
    file_atividades = st.file_uploader("Carregar Atividades", type=["txt"], key="atividades")

    atividades = []
    multiselect_atividades = st.empty()

    if file_atividades is not None:
        atividades = read_items_from_file(file_atividades)

    if atividades:
        selected_atividades = multiselect_atividades.multiselect("Selecione as atividades:", atividades, default=atividades)
    else:
        selected_atividades = multiselect_atividades.multiselect("Selecione as atividades:", [])

    st.markdown("---")

    st.markdown("### Carregar Veículos")
    file_veiculos = st.file_uploader("Carregar Veículos", type=["txt"], key="veiculos")

    veiculos = []
    multiselect_veiculos = st.empty()

    if file_veiculos is not None:
        veiculos = read_items_from_file(file_veiculos)

    if veiculos:
        selected_veiculos = multiselect_veiculos.multiselect("Selecione os veículos:", veiculos, default=veiculos)
    else:
        selected_veiculos = multiselect_veiculos.multiselect("Selecione os veículos:", [])

    return selected_servidores, selected_atividades, selected_veiculos

def gerar_programacao(ulsav, supervisao, selected_servidores, selected_atividades, selected_veiculos, incluir_sabado, incluir_domingo):
    st.markdown("### Gerar Programação")
    
    st.markdown("---")
        

    st.markdown("### Informe o primeiro dia da semana")
    primeiro_dia_semana = st.date_input("Selecione a data", value=date.today(), key="primeiro_dia_semana")
    st.markdown("---")
    
    primeiro_dia_semana_formatado = primeiro_dia_semana.strftime("%d/%m/%Y")

    dias_semana_dict = {
        0: "Segunda",
        1: "Terça",
        2: "Quarta",
        3: "Quinta",
        4: "Sexta",
        5: "Sábado" if incluir_sabado else None,
        6: "Domingo" if incluir_domingo else None
    }

    dias_da_semana = []
    for i in range(7 - primeiro_dia_semana.weekday()):
        dia_atual = primeiro_dia_semana + timedelta(days=i)
        dia_semana = dias_semana_dict.get(dia_atual.weekday())
        if dia_semana:
            dia_mes = dia_atual.day
            dias_da_semana.append({"id": dia_semana.lower(), "text": f"{dia_semana} - {dia_mes}"})

    # Definir variáveis semana_do_mes, mes_por_extenso e ano
    semana_do_mes = (primeiro_dia_semana.day - 1) // 7 + 1
    
    mes_por_extenso = translate_month(primeiro_dia_semana.strftime("%B"))
    ano = primeiro_dia_semana.year

    html_content = load_html("drag_and_drop.html", selected_servidores, selected_atividades, selected_veiculos, primeiro_dia_semana_formatado, dias_da_semana, ulsav, supervisao, semana_do_mes, mes_por_extenso, ano)
    components.html(html_content, height=10000)

def translate_month(month):
    months = {
        "January": "janeiro",
        "February": "fevereiro",
        "March": "março",
        "April": "abril",
        "May": "maio",
        "June": "junho",
        "July": "julho",
        "August": "agosto",
        "September": "setembro",
        "October": "outubro",
        "November": "novembro",
        "December": "dezembro"
    }
    return months.get(month, month)

# Tabs para navegação
tab1, tab2 = st.tabs(["Buscar Dados", "Gerar Programação"])

with tab1:
    selected_servidores, selected_atividades, selected_veiculos = buscar_dados()

with tab2:
    if selected_servidores and selected_atividades and selected_veiculos:
        col1, col2 = st.columns(2)
        with col1:
            ulsav = st.text_input("ULSAV", value="SMG")
        with col2:
            supervisao = st.text_input("Supervisão", value="SFG")

        st.markdown("---")
        
        st.markdown("### Incluir final de semana")
        col1, col2 = st.columns(2)
        with col1:
            incluir_sabado = st.checkbox("Sábado", value=False)
        with col2:
            incluir_domingo = st.checkbox("Domingo", value=False)
        
        gerar_programacao(ulsav, supervisao, selected_servidores, selected_atividades, selected_veiculos, incluir_sabado, incluir_domingo)
    else:
        st.error("Por favor, vá para a aba 'Buscar Dados' e carregue os dados primeiro.")
