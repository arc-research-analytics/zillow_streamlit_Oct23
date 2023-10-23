import streamlit as st


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

    plus_color = '#FFFFFF'
    plus_font_size = '40'
    plus_font_weight = '100'
    plus_line_height = '40'
    plus_align = 'left'
    plus_font_style = 'normal'

    # paragraph text
    text_3 = 'Home values coming soon!'
    st.markdown(
        f"<p style='color:{plus_color}; font-size:{plus_font_size}px; font-weight:{plus_font_weight}; line-height:{plus_line_height}px; font-style:{plus_font_style}; display:in-line; text-align:{plus_align};'>{text_3}", unsafe_allow_html=True)
