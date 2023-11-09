import streamlit as st
import geopandas as gpd
import pandas as pd
import pydeck as pdk
from Other import color_functions

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
        [data-testid="stExpanderToggleIcon"] {
            color: #46494C;
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
    '>Select forecast timeline:</p>
    """,
    unsafe_allow_html=True)

# forecast timeline select box
timeline_variable = st.sidebar.selectbox(
    label='something',
    options=(
        '1-month outlook',
        '3-month outlook',
        '12-month outlook'
    ),
    index=2,
    label_visibility='collapsed'
)

# dictionary to retrieve the correct column depending on user selection
timeline_dict = {
    '1-month outlook': '1month_forecast',
    '3-month outlook': '3month_forecast',
    '12-month outlook': '12month_forecast'
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
title_text = 'Metro Atlanta Home Value Forecasts'

# paragraph text
st.markdown(
    f"<p style='color:{title_color}; font-size:{title_font_size}px; font-weight:{title_font_weight}; font-style:{title_font_style}; display:in-line; text-align:{title_align};'><b>{title_text}</b>: {timeline_variable}", unsafe_allow_html=True)


# Set RGB color ramp for the mapper function
start_color = "#D7E2FF"
end_color = "#2191FB"
num_steps = 7
custom_colors = color_functions.generate_color_gradients(
    start_color, end_color, num_steps)


gdf = gpd.read_file('Processed_data/forecasts.gpkg')

# Replace 'Dekalb' with 'DeKalb'
gdf['CountyName'] = gdf['CountyName'].replace({
    'Dekalb County': 'DeKalb County'
})

# don't need the BaseDate column
gdf.drop(columns='BaseDate', inplace=True)

# do some cleaning
gdf.rename(columns={
    'RegionName': 'zip_code',
    'CountyName': 'county_name'
}, inplace=True)

gdf = gpd.GeoDataFrame(gdf)

# set choropleth color
gdf['choro_color'] = pd.cut(
    gdf[timeline_dict[timeline_variable]],
    bins=len(custom_colors),
    labels=custom_colors,
    include_lowest=True,
    duplicates='drop'
)

# format data column
gdf['data_formatted'] = gdf[timeline_dict[timeline_variable]].apply(
    lambda x: '{:.1f}%'.format((x)))

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
    height=550
)

# create the geojson data layer
geojson = pdk.Layer(
    "GeoJsonLayer",
    gdf,
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
    "html": "Forecasted change in home value: <b>{data_formatted}</b><hr style='margin: 10px auto; opacity:0.5; border-top: 2px solid white; width:85%'>\
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

st.pydeck_chart(r, use_container_width=True)

st.markdown("""
  <style>
    /*Border around expander*/
    .streamlit-expander {
        border: 1px solid #46494C;
        }
    /*border for hover*/
    .streamlit-expander:hover {
        border: 1px solid #FFFFFF;
        }
    /*font styling for expander body*/
    .streamlit-expander p {
        font-size: 16px;
        color: #46494C;
        }
    /*font styling for expander header only*/
    .streamlit-expanderHeader p {
      font-size: 18px;
      color: #46494C;
        }
  </style>
""", unsafe_allow_html=True)

expander_header = "Methodology note"

link_style = 'color:#606266; font-weight:900; text-decoration:none;'

# paragraph text
text_1 = 'From Zillow\'s methodology page: systematic error, or consistently over or underpredicting an event or the future, is the enemy of clear-eyed decision-making. Reducing systematic error in housing price forecasts during this environment centers around more flexibility and accurately capturing turning points versus seasonal trends. For more information on how this forecast model was developed, please visit <a href="https://www.zillow.com/research/methodology-neural-zhvi-32128/" style="' + \
    link_style + '">this page</a>.'


with st.expander(expander_header):
    st.markdown(
        f"<p style='text-align:left;'>{text_1}", unsafe_allow_html=True)
