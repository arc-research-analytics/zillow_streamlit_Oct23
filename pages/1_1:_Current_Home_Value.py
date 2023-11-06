import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
from PIL import Image
from Other import color_functions

# set basic settings
st.set_page_config(
    page_title="Zillow Dashboard",
    page_icon=":house:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'mailto:wwright@atlantaregional.org',
        'About': '### For more information about the Atlanta Regional Commission, please visit [our website](https://atlantaregional.org/). For more metro Atlanta research, please visit [our blog](https://33n.atlantaregional.com/).'
    }
)

custom_page_styling = """
    <style>
        .reportview-container .main {visibility: hidden;}    
        footer {visibility: hidden;}
        section.main > div:has(~ footer ) {
            padding-bottom: 5px;
            padding-left: 60px;
            padding-right: 50px;
            padding-top: 60px;
        }
        [data-testid="stDecoration"] {
            background-image: linear-gradient(90deg, rgb(70, 73, 76), rgb(70, 73, 76));
            }
        [data-testid="collapsedControl"] {
            color: #FFFFFF;
            background-color: #46494C;
            } 
        [id="MainMenu"] {
            color: #FFFFFF;
            background-color: #46494C;
            } 
        div[data-baseweb="select"] > div {
            background-color: #46494C;
            }
        button[title="View fullscreen"]{
            visibility: hidden;
            }
        div.stActionButton{visibility: hidden;}
    </style>
"""

st.markdown(custom_page_styling, unsafe_allow_html=True)

# sidebar---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v
sidebar_font_size = '16'
sidebar_color = '#FFFFFF'
sidebar_font_style = 'normal'

# housing type select box title & CSS
st.sidebar.markdown(
    f"""
    <p style='text-align:center;
    color:{sidebar_color};
    font-size:{sidebar_font_size}px;
    font-style:{sidebar_font_style};
    '>Select housing category:</p>
    """,
    unsafe_allow_html=True)

# housing type select box
housing_variable = st.sidebar.selectbox(
    label='something',
    options=(
        'All Single-Family Homes',
        '1-Bedroom Homes',
        '2-Bedroom Homes',
        '3-Bedroom Homes',
        '4-Bedroom Homes',
        '5+Bedroom Homes'
    ),
    index=0,
    label_visibility='collapsed'
)

housing_variable_dict = {
    'All Single-Family Homes': 'all_BR',
    '1-Bedroom Homes': '1_BR',
    '2-Bedroom Homes': '2_BR',
    '3-Bedroom Homes': '3_BR',
    '4-Bedroom Homes': '4_BR',
    '5+Bedroom Homes': '5+BR'
}
st.sidebar.write("")

# map basemap title & CSS
st.sidebar.markdown(
    f"""
    <p style='text-align:center;
    color:{sidebar_color};
    font-size:{sidebar_font_size}px;
    font-style:{sidebar_font_style};
    '>Select basemap:</p>
    """,
    unsafe_allow_html=True)

# dropdown to select the basemap
base_map = st.sidebar.selectbox(
    label='something',
    options=('Dark', 'Light', 'Streets'),
    index=0,
    label_visibility='collapsed'
)

# dictionary to change the basemap
base_map_dict = {
    'Streets': ['road', [0, 0, 0]],
    'Light': ['light', [0, 0, 0]],
    'Dark': ['dark', [255, 255, 255]]
}

# sidebar---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^

# main section
title_color = '#46494C'
title_font_size = '35'
title_font_weight = '100'
title_font_style = 'normal'
title_align = 'left'
title_text = 'Metro Atlanta Home Values'

# paragraph text
st.markdown(
    f"<p style='color:{title_color}; font-size:{title_font_size}px; font-weight:{title_font_weight}; font-style:{title_font_style}; display:in-line; text-align:{title_align};'><b>{title_text}</b>: {housing_variable}", unsafe_allow_html=True)


# Set RGB color ramp for the mapper function
start_color = "#D7E2FF"
end_color = "#2191FB"
num_steps = 5
custom_colors = color_functions.generate_color_gradients(
    start_color, end_color, num_steps)


@st.cache_data
def load_data():

    # load the data
    gdf = gpd.read_file('Processed_data/zillow_final_SIMP.gpkg')

    # Replace 'Dekalb' with 'DeKalb'
    gdf['CountyName'] = gdf['CountyName'].replace({
        'Dekalb County': 'DeKalb County'
    })

    # return this item
    return gdf


df_init = load_data()


def pydeck_map():
    gdf = df_init

    # for mapping purposes, we only want to show the final month's values, along with the ZIP, county, and geometry
    zip_column = gdf.iloc[:, 0]
    county_column = gdf.iloc[:, 1]
    geometry_column = gdf.iloc[:, -1]
    data_column = gdf[housing_variable_dict[housing_variable]]

    zillow_gdf = pd.concat([
        zip_column,
        county_column,
        geometry_column,
        data_column
    ], axis=1)

    # rename the final (data) column, which will change names whenever the data is updated
    zillow_gdf.rename(columns={
        'RegionName': 'zip_code',
        'CountyName': 'county_name',
        zillow_gdf.columns[-1]: 'data_column'
    }, inplace=True)

    # make sure we're working with a GeoDataFrame
    zillow_gdf = gpd.GeoDataFrame(zillow_gdf)

    # drop the Nan values
    zillow_gdf.dropna(subset=['data_column'], inplace=True)

    # set choropleth color
    zillow_gdf['choro_color'] = pd.cut(
        zillow_gdf['data_column'],
        bins=len(custom_colors),
        labels=custom_colors,
        include_lowest=True,
        duplicates='drop'
    )

    # format data column
    zillow_gdf['data_formatted'] = zillow_gdf['data_column'].apply(
        lambda x: '${:,.0f}'.format((x)))

    # view state variables
    latitude = 33.83
    longitude = -84.38
    zoom = 8

    # create intitial view state
    initial_view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=zoom,
        pitch=0,
        bearing=0,
        height=575
    )

    # create the geojson data layer
    geojson = pdk.Layer(
        "GeoJsonLayer",
        zillow_gdf,
        pickable=True,
        autoHighlight=True,
        highlight_color=[255, 255, 255, 128],
        opacity=0.5,
        stroked=True,
        filled=True,
        get_fill_color='choro_color',
        get_line_color=[255, 255, 255, 50],
        line_width_min_pixels=1
    )

    # create the geojson counties layer
    atl_counties = gpd.read_file('Other/atl_counties.gpkg')
    geojson_counties = pdk.Layer(
        "GeoJsonLayer",
        atl_counties,
        pickable=False,
        autoHighlight=False,
        opacity=0.75,
        stroked=True,
        filled=False,
        get_line_color=base_map_dict[base_map][1],
        line_width_min_pixels=2
    )

    # configure & customize the tooltip
    tooltip = {
        "html": "Home value index: <b>{data_formatted}</b><hr style='margin: 10px auto; opacity:0.5; border-top: 2px solid white; width:85%'>\
                    ZIP: {zip_code} <br>\
                    As part of: {county_name}",
        "style": {"background": "rgba(70,73,76,0.7)",
                  "border": "1px solid white",
                  "color": "white",
                  "font-family": "Helvetica",
                  "text-align": "center"
                  },
    }

    r = pdk.Deck(
        layers=[
            geojson,
            geojson_counties
        ],
        initial_view_state=initial_view_state,
        map_provider='mapbox',
        map_style=base_map_dict[base_map][0],
        tooltip=tooltip
    )

    return r


# define <div> columns for main area
col1, col2, col3 = st.columns([
    2,  # map column
    0.05,  # spacer column
    1  # KPI  column
])

# call mapper function
col1.pydeck_chart(pydeck_map(), use_container_width=True)

# KPIs---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v
gdf = df_init

# for mapping purposes, we only want to show the final month's values, along with the ZIP, county, and geometry
zip_column = gdf.iloc[:, 0]
county_column = gdf.iloc[:, 1]
data_column = gdf[housing_variable_dict[housing_variable]]

zillow_df = pd.concat([
    zip_column,
    county_column,
    data_column
], axis=1)

# rename the final (data) column, which will change names whenever the data is updated
zillow_df.rename(columns={
    zip_column.name: 'zip_code',
    county_column.name: 'county',
    data_column.name: 'data_column'
}, inplace=True)


# get the KPI vales for max
max_index = '${:,.0f}'.format(zillow_df['data_column'].max())
max_row = zillow_df['data_column'].idxmax()
max_zip = zillow_df.loc[max_row, 'zip_code']
max_county = zillow_df.loc[max_row, 'county']

# get the KPI vales for median
median_index = '${:,.0f}'.format(zillow_df['data_column'].median())
median_row = (zillow_df['data_column'] -
              zillow_df['data_column'].median()).abs().idxmin()
median_zip = zillow_df.loc[median_row, 'zip_code']
median_county = zillow_df.loc[median_row, 'county']

# get the KPI vales for min
min_index = '${:,.0f}'.format(zillow_df['data_column'].min())
min_row = zillow_df['data_column'].idxmin()
min_zip = zillow_df.loc[min_row, 'zip_code']
min_county = zillow_df.loc[min_row, 'county']


# kpi styles
KPI_label_font_size = '19'
KPI_label_font_color = '#46494C'
KPI_label_font_weight = '800'
min_text = 'Lowest Home Value:'
median_text = 'Median Home Value:'
max_text = 'Highest Home Value:'

KPI_value_font_size = '25'
KPI_value_font_color = '#46494C'
KPI_value_font_weight = '100'
KPI_line_height = '30'  # vertical spacing between the KPI label and value

# Max Housing Value KPI
col3.markdown(
    f"<span style='color:{KPI_label_font_color}; font-size:{KPI_label_font_size}px; font-weight:{KPI_label_font_weight}'>{max_text}</span><br><span style='color:{KPI_value_font_color}; font-size:{KPI_value_font_size}px; font-weight:{KPI_value_font_weight}; line-height: {KPI_line_height}px'>Index: {max_index}<br>ZIP: {max_zip}<br>As part of: {max_county}</span>", unsafe_allow_html=True)
col3.write("")

# Regionwide median
col3.markdown(
    f"<span style='color:{KPI_label_font_color}; font-size:{KPI_label_font_size}px; font-weight:{KPI_label_font_weight}'>{median_text}</span><br><span style='color:{KPI_value_font_color}; font-size:{KPI_value_font_size}px; font-weight:{KPI_value_font_weight}; line-height: {KPI_line_height}px'>Index: {median_index}<br>ZIP: {median_zip}<br>As part of: {median_county}</span>", unsafe_allow_html=True)
col3.write("")

# Min Housing Value KPI
col3.markdown(
    f"<span style='color:{KPI_label_font_color}; font-size:{KPI_label_font_size}px; font-weight:{KPI_label_font_weight}'>{min_text}</span><br><span style='color:{KPI_value_font_color}; font-size:{KPI_value_font_size}px; font-weight:{KPI_value_font_weight}; line-height: {KPI_line_height}px'>Index: {min_index}<br>ZIP: {min_zip}<br>As part of: {min_county}</span>", unsafe_allow_html=True)


# Zillow logo
col3.write("")
col3.write("")
image = Image.open('Other/zillow_watermark.png')
with col3:
    subcol1, subcol2, subcol3 = st.columns(3)
    subcol2.image(image, width=100)
