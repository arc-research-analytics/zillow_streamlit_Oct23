import streamlit as st

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
        span[data-baseweb="tag"] {
            background-color: #46494C 
            }
        div.stActionButton{visibility: hidden;}
    </style>
"""

st.markdown(custom_page_styling, unsafe_allow_html=True)

st.header("Coming soon!")
