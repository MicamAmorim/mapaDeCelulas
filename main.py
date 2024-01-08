import streamlit as st
import pandas as pd
from createmap import createMap  # Supondo que a função createMap esteja em um script chamado 'your_script.py'
import streamlit.components.v1 as components

# Configurações do tema
st.set_page_config(
    page_title="Visualizador de Mapas",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Esta é uma aplicação para visualizar mapas."
    }
)

# Define um estilo CSS para o título
title_html = """
    <style>
        .title {
            font-family: 'Comic Sans MS', 'Comic Sans', cursive; /* Escolha a fonte */
            font-style: italic; /* Estilo itálico */
        }
    </style>
    <div class='title'>Encontre a célula mais próxima de sua casa</div>
"""

# Usa st.sidebar.markdown para renderizar o HTML com o estilo CSS
st.sidebar.markdown(title_html, unsafe_allow_html=True)

uploaded_file = "Database/dados.csv"

if uploaded_file:
    # Carrega os dados para um DataFrame
    df = pd.read_csv(uploaded_file)

    for _, row in df.iterrows():
        st.sidebar.write(f"📍 {row['Nome']}: {row['Endereco']} | WhatsApp: {row['Telefone']}")
    # Chama a função para criar o mapa
    mapa = createMap(df)

    # Mostra o mapa na página
    #st.pydeck_chart(mapa)
    mapa.save('mapa.html')
    with open('mapa.html', 'r', encoding='utf-8') as f:
        html_string = f.read()
        html_string = html_string.replace('<head>', '<head><style>html, body {width: 100%; height: 100%; margin: 0; padding: 0;} #map {width: 100% !important; height: 100% !important;}</style>')

        # Exibe o mapa no Streamlit
        components.html(html_string, height=500, scrolling=True)


else:
    st.sidebar.warning("Por favor, carregue um arquivo CSV.")
