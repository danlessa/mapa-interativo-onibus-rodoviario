import os
import streamlit as st
from script import load_data, plot_map_per_org, plot_map_per_slug

# Define layout

st.set_page_config(
    page_title="Origens e Destinos dos Ônibus Rodoviários do Brasil",
    page_icon=os.path.join(os.path.dirname(__file__), "assets", "icon.png"),
    layout="wide",
)

df = load_data()

st.markdown("# Origens e Destinos dos Ônibus Rodoviários do Brasil")

st.markdown('## Mapa 1: Origens e Destinos partindo/chegando em uma cidade, categorizado por empresas')
options = df.src.value_counts().keys()

slug = st.selectbox('Ponto de Referência', options)
src_as_reference = st.checkbox('Usar referência como origem (marcado) ou destino (desmarcado)')
companies = list(df.company.value_counts().keys())
companies.append('todos')

companies = st.multiselect('Empresas de ônibus', companies, default=['todos'])

if 'todos' in companies:
    fig = plot_map_per_slug(df, slug, src_as_reference)
else:
    fig = plot_map_per_org(df, companies)

st.plotly_chart(fig, use_container_width=True)

# Download data


@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")
