import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

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
    '>Select ZIP code(s):</p>
    """,
    unsafe_allow_html=True)

# list containing all the metro ZIP codes (same list used to display on the maps)
zip_list = [
    '30058', '30083', '30084', '30087', '30309', '30331', '30005', '30032',
    '30033', '30088', '30236', '30296', '30017', '30041', '30307', '30327',
    '30009', '30045', '30047', '30094', '30340', '30004', '30012', '30024',
    '30071', '30080', '30092', '30097', '30152', '30297', '30316', '30519',
    '30013', '30030', '30043', '30135', '30021', '30028', '30035', '30046',
    '30273', '30305', '30339', '30019', '30022', '30039', '30044', '30076',
    '30114', '30189', '30213', '30252', '30294', '30008', '30038', '30060',
    '30062', '30122', '30064', '30066', '30168', '30075', '30067', '30068',
    '30126', '30078', '30127', '30082', '30134', '30214', '30093', '30107',
    '30096', '30101', '30102', '30188', '30034', '30106', '30144', '30040',
    '30115', '30308', '30310', '30312', '30281', '30253', '30248', '30260',
    '30238', '30288', '30291', '30269', '30303', '30215', '30228', '30274',
    '30306', '30326', '30350', '30311', '30329', '30360', '30363', '30313',
    '30337', '30338', '30314', '30344', '30315', '30341', '30342', '30317',
    '30345', '30324', '30328', '30346', '30318', '30354', '30319', '30349',
    '30518', '30183', '30205', '30290', '30268', '30187', '30052', '30336',
    '30002', '30079', '30322', '30332', '30072', '30250', '30111', '30272'
]

sorted_zip_list = sorted(zip_list)

# housing type select box
zip_select = st.sidebar.multiselect(
    label='something',
    options=sorted_zip_list,
    default=['30002'],
    max_selections=10,
    label_visibility='collapsed'
)
# sidebar---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^---^

# main section title
title_color = '#46494C'
title_font_size = '35'
title_font_weight = '500'
title_line_height = '20'
title_font_style = 'normal'
title_align = 'left'
title_text = 'Historic Home Values by ZIP Code'

# title text
st.markdown(
    f"<p style='color:{title_color}; font-size:{title_font_size}px; font-weight:{title_font_weight}; line-height:{title_line_height}px; font-style:{title_font_style}; display:in-line; text-align:{title_align};'>{title_text}", unsafe_allow_html=True)

# ---------------------
# line chart

# read in data
df = pd.read_csv('Processed_data/historic_value.csv')

# cleaning
df['RegionName'] = df['RegionName'].astype(str)
df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

df = df[df['RegionName'].isin(zip_select)]

fig = fig = px.line(
    df,
    x="Date",
    y="Index",
    color='RegionName'
)

fig.update_traces(
    mode="lines",
    hovertemplate="<br>".join([
        "<b>%{y}</b>"
    ]),
    line=dict(
        width=1
    )
)

fig.update_layout(
    showlegend=False,
    margin=dict(
        t=50,
        r=25
    ),
    hoverlabel=dict(
        bgcolor="#C5C3C6",
        bordercolor="#46494C",
        font_size=16,  # set the font size of the chart tooltip
        font_color="#46494C",
        align="left"
    ),
    yaxis=dict(
        linecolor="#46494C",
        linewidth=2,
        title=None,
        tickfont_color='#46494C',
        tickfont_size=16,
        tickformat='$,.0f',
        showgrid=False,
        zeroline=False
    ),
    xaxis=dict(
        linecolor="#46494C",
        linewidth=2,
        tickfont_color='#46494C',
        title=None,
        tickfont_size=16,
        tickformat='%b %Y',
        dtick='M3'
    ),
    height=650,
    hovermode="x unified")

col1, col2 = st.columns([3, 1])
col1.plotly_chart(fig, use_container_width=True,
                  config={'displayModeBar': False})

# KPI section---------------------------------------------------
df_summary = pd.read_csv('Processed_data/historic_value_summary.csv')

# cleaning
df_summary['RegionName'] = df_summary['RegionName'].astype(str)
df_summary = df_summary.loc[:, ~df_summary.columns.str.startswith('Unnamed')]

# calculate KPI values
max_index = '{:.2f}%'.format(df_summary['percent_change'].max())
max_row = df_summary['percent_change'].idxmax()
max_zip = df_summary.loc[max_row, 'RegionName']
max_county = df_summary.loc[max_row, 'CountyName']

# get the KPI vales for median
median_index = '{:.2f}%'.format(df_summary['percent_change'].median())
median_row = (df_summary['percent_change'] -
              df_summary['percent_change'].median()).abs().idxmin()
median_zip = df_summary.loc[median_row, 'RegionName']
median_county = df_summary.loc[median_row, 'CountyName']

# get the KPI vales for min
min_index = '{:.2f}%'.format(df_summary['percent_change'].min())
min_row = df_summary['percent_change'].idxmin()
min_zip = df_summary.loc[min_row, 'RegionName']
min_county = df_summary.loc[min_row, 'CountyName']

# KPI styling
KPI_label_font_size = '22'
KPI_label_font_color = '#46494C'
KPI_label_font_weight = '800'
max_text = 'Largest Historic Change:'
median_text = 'Median Change:'
min_text = 'Smallest Historic Change:'

KPI_value_font_size = '20'
KPI_value_font_color = '#46494C'
KPI_value_font_weight = '100'
KPI_line_height = '30'  # vertical spacing between the KPI label and value

col2.write("")
col2.write("")
# max
col2.markdown(
    f"<span style='color:{KPI_label_font_color}; font-size:{KPI_label_font_size}px; font-weight:{KPI_label_font_weight}'>{max_text}</span><br><span style='color:{KPI_value_font_color}; font-size:{KPI_value_font_size}px; font-weight:{KPI_value_font_weight}; line-height: {KPI_line_height}px'>{max_index}<br>ZIP: {max_zip}<br>As part of: {max_county}</span>",
    unsafe_allow_html=True)
col2.write("")

# median
col2.markdown(
    f"<span style='color:{KPI_label_font_color}; font-size:{KPI_label_font_size}px; font-weight:{KPI_label_font_weight}'>{median_text}</span><br><span style='color:{KPI_value_font_color}; font-size:{KPI_value_font_size}px; font-weight:{KPI_value_font_weight}; line-height: {KPI_line_height}px'>{median_index}<br>ZIP: {median_zip}<br>As part of: {median_county}</span>",
    unsafe_allow_html=True)
col2.write("")

# min
col2.markdown(
    f"<span style='color:{KPI_label_font_color}; font-size:{KPI_label_font_size}px; font-weight:{KPI_label_font_weight}'>{min_text}</span><br><span style='color:{KPI_value_font_color}; font-size:{KPI_value_font_size}px; font-weight:{KPI_value_font_weight}; line-height: {KPI_line_height}px'>{min_index}<br>ZIP: {min_zip}<br>As part of: {min_county}</span>",
    unsafe_allow_html=True)

col2.write("")
col2.write("")
image = Image.open('Other/zillow_watermark.png')
with col2:
    subcol1, subcol2, subcol3 = st.columns(3)
    subcol2.image(image, width=80)
