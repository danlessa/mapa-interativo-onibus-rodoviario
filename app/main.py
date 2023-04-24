import os
import streamlit as st
from script import load_data, plot_map_per_org

df = load_data()

# Define layout

st.set_page_config(
    page_title="Origens e Destinos dos Ônibus Rodoviários do Brasil",
    page_icon=os.path.join(os.path.dirname(__file__), "assets", "icon.png"),
    layout="wide",
)

st.markdown("# Origens e Destinos dos Ônibus Rodoviários do Brasil")

st.sidebar.markdown('## Controles')
options = df.src.value_counts().keys()

slug = st.sidebar.selectbox('Ponto de Referência', options)
plot_container = st.container()


fig = plot_map_per_org(df, slug)
st.plotly_chart(fig)


    
# Download data


@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")
