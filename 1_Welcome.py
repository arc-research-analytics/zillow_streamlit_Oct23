import streamlit as st
from PIL import Image
import base64

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
        button[title="View fullscreen"]{
            visibility: hidden;
            }

        div.stActionButton{visibility: hidden;}
    </style>
"""

st.markdown(custom_page_styling, unsafe_allow_html=True)


# functions, calls to set background image
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-repeat: no-repeat;
    }
    .stApp::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            to top, 
            rgba(197, 195, 198, 0), 
            rgba(197, 195, 198, 0.8), 
            rgba(197, 195, 198, 1)
        );
        pointer-events: none;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


set_background('./Other/atl_streets.png')

# dashboard title styling variables
dash_title_color = '#46494C'
dash_title_font_size = '32'
dash_title_font_weight = '600'
line_height1 = '70'
title_align = 'left'
title_font_style = 'normal'
dash_text = 'Welcome to the Atlanta Zillow Dashboard!'

# dashboard title
st.markdown(
    f"<p style='color:{dash_title_color}; font-size:{dash_title_font_size}px; font-weight:{dash_title_font_weight}; line-height:{line_height1}px; font-style:{title_font_style}; display:in-line; text-align:{title_align};'>{dash_text}</p>", unsafe_allow_html=True)

# paragraph styling variables
paragraph_color = '#606266'
paragraph_font_size = '20'
paragraph_font_weight = '100'
paragraph_line_height = '30'
paragraph_align = 'left'
paragraph_font_style = 'normal'
link_style = 'color:#606266; font-weight:900; text-decoration:none;'

# paragraph text
text_1 = 'This desktop app is built to explore Zillow\'s home value and rent index datasets. Browse the five visuals via the left-hand sidebar navigation menu. All data has been downloaded to the ZIP code level and is current as of October 2023. Read more about Zillow\'s home value methodology <a href="https://www.zillow.com/research/methodology-neural-zhvi-32128/" style="' + \
    link_style + '">here</a> and rent index methodology <a href="https://www.zillow.com/research/methodology-zori-repeat-rent-27092/" style="' + link_style + '">here</a>.'
st.markdown(
    f"<p style='color:{paragraph_color}; font-size:{paragraph_font_size}px; font-weight:{paragraph_font_weight}; line-height:{paragraph_line_height}px; font-style:{paragraph_font_style}; display:in-line; text-align:{paragraph_align};'>{text_1}", unsafe_allow_html=True)

st.write("")
text_2 = 'This dashboard is powered by Streamlit and built by the Atlanta Regional Commission\'s Research & Analytics Department.'
st.markdown(
    f"<p style='color:{paragraph_color}; font-size:{paragraph_font_size}px; font-weight:{paragraph_font_weight}; line-height:{paragraph_line_height}px; font-style:{paragraph_font_style}; display:in-line; text-align:{paragraph_align};'>{text_2}", unsafe_allow_html=True)

# cover page logo background
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
col1, col2, col3 = st.sidebar.columns([1, 1, 1])
logo_width = 90

with col2:
    # first logo
    image = Image.open('Other/arc2.png')
    st.image(image, width=logo_width)

    # paragraph styling variables
    plus_color = '#FFFFFF'
    plus_font_size = '40'
    plus_font_weight = '100'
    plus_line_height = '40'
    plus_align = 'center'
    plus_font_style = 'normal'

    # paragraph text
    text_3 = '+'
    st.markdown(
        f"<p style='color:{plus_color}; font-size:{plus_font_size}px; font-weight:{plus_font_weight}; line-height:{plus_line_height}px; font-style:{plus_font_style}; display:in-line; text-align:{plus_align};'>{text_3}", unsafe_allow_html=True)

    # second logo
    image = Image.open('Other/zillow_logo_BW.png')
    st.image(image, width=logo_width)
