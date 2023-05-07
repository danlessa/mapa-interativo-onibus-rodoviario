import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib
from matplotlib.cm import Set2
from tqdm.auto import tqdm
import pandas as pd
import streamlit as st

coords_path = 'data/2022-12-17 15:52:24.006277-coords.json'
data_path = 'data/2022-12-17 14:46:49.632892-output.json'
routes_path = 'data/2022-12-18 01:33:21.284286-company-routes.json'
SLUG_PATH = 'data/slug_df.csv.xz'

WIDTH = 800
HEIGHT = 900
COLOR_SCALE = px.colors.qualitative.Set1
POINT_SIZE = 5
LAYOUT = dict(
    autosize=True,
    #minreducedwidth=600,
    #minreducedheight=400,
    #width=WIDTH, 
    #height=HEIGHT,
    mapbox = {
        'accesstoken': st.secrets['MAPBOX_TOKEN'],
        'style': 'mapbox://styles/danlessa/clhdiwox000ll01o3a3xs6fvp',
        'zoom': 3},
    legend=dict(
        orientation='h',
       # font = dict(size = 10)
    ),
    showlegend = True

)

px.set_mapbox_access_token(st.secrets['MAPBOX_TOKEN'])





@st.cache_resource
def load_data() -> pd.DataFrame:
    slug_df = pd.read_csv(SLUG_PATH)
    # categories = set(slug_df.company)
    # n_colors = len(categories)
    # colors = px.colors.sample_colorscale("turbo", [n/(n_colors -1) for n in range(n_colors)])
    # colors = {category: colors[i] for i, category in enumerate(categories)}
    # slug_df = slug_df.assign(company_color=lambda df: df.company.map(colors))
    return slug_df

@st.cache_resource
def plot_map_per_slug(slug_df, slug, src_as_reference=True):
    def get_slug_fig_df(slug_df, slug, src_as_reference):
        if src_as_reference:
            city_query = f"src == '{slug}'"
            reference_col = 'dst'
            adjacent_col = 'src'
        else:
            city_query = f"dst == '{slug}'"
            reference_col = 'src'
            adjacent_col = 'dst'
        QUERY = f"{city_query} & align_to_src == {src_as_reference}"
        fig_df = slug_df.query(QUERY).reset_index()
        return reference_col, adjacent_col, fig_df

    reference_col, adjacent_col, fig_df = get_slug_fig_df(slug_df, slug, src_as_reference)


    if src_as_reference:
        title = f"Pontos de destino saindo de {slug}"
    else:
        title = f"Pontos de origem indo até {slug}"

    fig = px.scatter_mapbox(fig_df,
                        lon=f'{reference_col}_x',
                        lat=f'{reference_col}_y', 
                        color='company',
                        hover_name=reference_col,
                        title=title,
                        color_discrete_sequence=COLOR_SCALE,
                        )

    fig.update_traces(marker=dict(size=POINT_SIZE))
    fig.update_layout(**LAYOUT)
    return fig
    

@st.cache_resource
def plot_map_per_org(slug_df, companies: list[str]):

    fig_df = slug_df[slug_df.company.isin(companies)]

    fig = px.scatter_mapbox(fig_df,
                        lon=f'src_x',
                        lat=f'src_y', 
                        color='company',
                        title="Pontos de origem por empresa",
                        color_discrete_sequence=COLOR_SCALE)

    fig.update_traces(marker=dict(size=POINT_SIZE))
    fig.update_layout(**LAYOUT)
    return fig