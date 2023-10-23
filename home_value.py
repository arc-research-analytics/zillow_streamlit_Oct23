import streamlit as st


def app():
    # the custom page styling lives here:
    custom_page_styling = """
            <style>
                .reportview-container .main {visibility: hidden;}    
                footer {visibility: hidden;}
                section.main > div:has(~ footer ) {
                    padding-bottom: 1px;
                    padding-left: 40px;
                    padding-right: 40px;
                    padding-top: 30px;
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

    st.header('Home values coming soon!')
