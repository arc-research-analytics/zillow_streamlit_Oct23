import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import pydeck as pdk


def app():
    # the custom page styling lives here:
    custom_page_styling = """
            <style>
                .reportview-container .main {visibility: hidden;}    
                footer {visibility: hidden;}
                section.main > div:has(~ footer ) {
                    padding-bottom: 5px;
                    padding-left: 60px;
                    padding-right: 10px;
                    padding-top: 50px;
                }
                [data-testid="stDecoration"] {
                    background-image: linear-gradient(90deg, rgb(70, 73, 76), rgb(70, 73, 76));
                    }
                div[data-baseweb="select"] > div {
                    background-color: #46494C;
                    }
                [data-testid="collapsedControl"] {
                    color: #FFFFFF;
                    background-color: #46494C;
                    } 
                [id="MainMenu"] {
                    color: #FFFFFF;
                    background-color: #46494C;
                    } 
                span[data-baseweb="tag"] {
                    background-color: #46494C 
                    }
                div.stActionButton{visibility: hidden;}
            </style>
        """

    st.markdown(custom_page_styling, unsafe_allow_html=True)

    # sidebar---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v---v
    st.sidebar.write("---")

    sidebar_font_size = '18'
    sidebar_color = '#FFFFFF'
    sidebar_font_style = 'normal'

    # county select
    st.sidebar.markdown(
        f"""
        <p style='text-align:center;
        color:{sidebar_color};
        font-size:{sidebar_font_size}px;
        font-style:{sidebar_font_style};
        '>Select county:</p>
        """,
        unsafe_allow_html=True)

    county_variable = st.sidebar.selectbox(
        label='',
        options=(
            'All counties',
            'Cherokee',
            'Clayton',
            'Cobb',
            'DeKalb',
            'Douglas',
            'Fayette',
            'Forsyth',
            'Fulton',
            'Gwinnett',
            'Henry',
            'Rockdale'
        ),
        index=0,
        # placeholder='Choose housing type',
        label_visibility='collapsed'
    )

    # dictionary keys are the dropdown values of the selectbox.
    # dictionary values are as follows: title text, dataframe filter text, lat, long, zoom level
    county_variable_dict = {
        'All counties': ['Metro Atlanta', '', 33.77, -84.40, 8],
        'Cherokee': ['Cherokee County', 'Cherokee County', 34.24, -84.46, 11],
        'Clayton': ['Clayton County', 'Clayton County', 33.54, -84.35, 11],
        'Cobb': ['Cobb County', 'Cobb County', 33.93, -84.55, 11],
        'DeKalb': ['DeKalb County', 'Dekalb County', 33.81, -84.21, 11],
        'Douglas': ['Douglas County', 'Douglas County', 33.71, -84.74, 11],
        'Fayette': ['Fayette County', 'Fayette County', 33.41, -84.48, 11],
        'Forsyth': ['Forsyth County', 'Forsyth County', 34.22, -84.11, 11],
        'Fulton': ['Fulton County', 'Fulton County', 33.80, -84.43, 11],
        'Gwinnett': ['Gwinnett County', 'Gwinnett County', 33.97, -84.01, 11],
        'Henry': ['Henry County', 'Henry County', 33.46, -84.15, 11],
        'Rockdale': ['Rockdale County', 'Rockdale County', 33.65, -84.03, 11]
    }

    # separator
    st.sidebar.write("")

    # housing type select
    st.sidebar.markdown(
        f"""
        <p style='text-align:center;
        color:{sidebar_color};
        font-size:{sidebar_font_size}px;
        font-style:{sidebar_font_style};
        '>Select housing category:</p>
        """,
        unsafe_allow_html=True)

    housing_variable = st.sidebar.selectbox(
        label='',
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
        'All Single-Family Homes': 'zhvi_uc_sfr.gpkg',
        '1-Bedroom Homes': 'zhvi_bdrmcnt_1.gpkg',
        '2-Bedroom Homes': 'zhvi_bdrmcnt_2.gpkg',
        '3-Bedroom Homes': 'zhvi_bdrmcnt_3.gpkg',
        '4-Bedroom Homes': 'zhvi_bdrmcnt_4.gpkg',
        '5+Bedroom Homes': 'zhvi_bdrmcnt_5.gpkg'
    }

    # sidebar---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^

    # main section

    title_color = '#46494C'
    title_font_size = '35'
    title_font_weight = '100'
    title_font_style = 'normal'
    title_align = 'left'
    title_text = f'{county_variable_dict[county_variable][0]} Home Values'

    # paragraph text
    st.markdown(
        f"<p style='color:{title_color}; font-size:{title_font_size}px; font-weight:{title_font_weight}; font-style:{title_font_style}; display:in-line; text-align:{title_align};'><b>{title_text}</b>: {housing_variable}", unsafe_allow_html=True)

    # set choropleth colors for the map
    custom_colors = [
        '#d7e2ff',  # lightest blue
        '#acc6fe',
        '#79abfd',
        '#2191fb'  # darkest blue
    ]

    # convert the above hex list to RGB values, since this is what the Pydeck map requires
    custom_colors = [tuple(int(h.lstrip('#')[i:i+2], 16)
                           for i in (0, 2, 4)) for h in custom_colors]

    def load_data():

        # load the data
        gdf = gpd.read_file(
            f'Processed_data/{housing_variable_dict[housing_variable]}',
        )

        # return this item
        return gdf

    df_init = load_data()

    def pydeck_map():
        gdf = df_init

        # for mapping purposes, we only want to show the final month's values, along with the ZIP, county, and geometry
        zip_column = gdf.iloc[:, 0]
        county_column = gdf.iloc[:, 1]
        geometry_column = gdf.iloc[:, -1]
        data_column = gdf.iloc[:, -2]

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

        # filter the dataframe based on selections
        if county_variable == 'All counties':
            zillow_gdf = zillow_gdf
        else:
            zillow_gdf = zillow_gdf[zillow_gdf['county_name']
                                    == county_variable_dict[county_variable][1]]

        # make sure we're working with a GeoDataFrame
        zillow_gdf = gpd.GeoDataFrame(zillow_gdf)

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

        # create map intitial state
        initial_view_state = pdk.ViewState(
            latitude=county_variable_dict[county_variable][2],
            longitude=county_variable_dict[county_variable][3],
            zoom=county_variable_dict[county_variable][4],
            max_zoom=5,
            min_zoom=20,
            pitch=0,
            bearing=0,
            height=550
        )
        st.write("")

        # create the geojson data layer
        geojson_data = pdk.Layer(
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
            get_line_color=[0, 0, 0],
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
            layers=[geojson_data, geojson_counties],
            initial_view_state=initial_view_state,
            map_provider='mapbox',
            map_style='road',
            tooltip=tooltip
        )

        return r

    # define <div> columns for main area
    col1, col2, col3 = st.columns([2, 1, 1])

    # call mapper function
    col1.pydeck_chart(pydeck_map(), use_container_width=True)
