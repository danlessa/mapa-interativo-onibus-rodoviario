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

px.set_mapbox_access_token(st.secrets['MAPBOX_TOKEN'])


def load_data() -> pd.DataFrame:
    slug_df = pd.read_csv(SLUG_PATH)
    categories = set(slug_df.company)
    n_colors = len(categories)
    colors = px.colors.sample_colorscale("turbo", [n/(n_colors -1) for n in range(n_colors)])
    colors = {category: colors[i] for i, category in enumerate(categories)}
    slug_df = slug_df.assign(company_color=lambda df: df.company.map(colors))
    return slug_df


def plot_map_per_org(slug_df, slug, src_as_reference=True):
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
                        height=600, width=800)

    fig.update_traces(marker=dict(size=8))

    fig.update_layout(
        mapbox = {
            'accesstoken': st.secrets['MAPBOX_TOKEN'],
            'style': "outdoors", 'zoom': 3},
        showlegend = True)

    return fig