import streamlit as st
import pandas as pd
import plotly.express as px

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

# main section
title_color = '#46494C'
title_font_size = '35'
title_font_weight = '100'
title_font_style = 'normal'
title_align = 'left'
title_text = 'Historic Home Values by ZIP Code'

# paragraph text
st.markdown(
    f"<p style='color:{title_color}; font-size:{title_font_size}px; font-weight:{title_font_weight}; font-style:{title_font_style}; display:in-line; text-align:{title_align};'>{title_text}", unsafe_allow_html=True)


df = pd.read_csv('Processed_data/historic_value.csv')
st.dataframe(df)
