import streamlit as st
from streamlit_option_menu import option_menu
import welcome
import home_value
import forecasts
import zori

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


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():

        with st.sidebar:
            app = option_menu(
                menu_title='Dashboard Menu',
                menu_icon='arrow-90deg-down',
                options=['Welcome', 'Home Values',
                         'Home Value Forecasts', 'Rent Index'],
                icons=['bookmark-dash', 'house-door',
                       'graph-up', 'cash-stack'],
                default_index=0,
                styles={
                    'container': {'background-color': '#46494C'},
                    "nav-link": {"--hover-color": "#909093", "color": "#FFFFFF"},
                    "nav-link-selected": {"background-color": "#FF7F11"}
                }
            )

        if app == 'Welcome':
            welcome.app()
        elif app == 'Home Values':
            home_value.app()
        elif app == 'Home Value Forecasts':
            forecasts.app()
        elif app == 'Rent Index':
            zori.app()

    # run the function
    run()
