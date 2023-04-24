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

st.sidebar.markdown('## Controles')
options = df.src.value_counts().keys()

slug = st.sidebar.selectbox('Ponto de Referência', options)
src_as_reference = st.sidebar.checkbox('Usar referência como origem (marcado) ou destino (desmarcado)')


companies = df.company.value_counts().keys()
companies = st.sidebar.multiselect('Empresas de ônibus', companies, default=['catarinense'])

fig_1 = plot_map_per_slug(df, slug, src_as_reference)
st.plotly_chart(fig_1)

fig_2 = plot_map_per_org(df, companies)
st.plotly_chart(fig_2)
    
# Download data


@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")
