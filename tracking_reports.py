import streamlit as st
from streamlit_option_menu import option_menu

def tracking_reports(client):
    st.title('Tracking & Reports')
    cola, colb = st.columns([1, 1])
    with cola:
        tr_select = option_menu(
            menu_title=None,
            options=['Current Stock', 'Low Stock', 'History', 'Valuation'],
            icons=['box-seam-fill', 'exclamation-diamond', 'hourglass-split', 'ui-checks'],
            orientation='horizontal',
            styles={
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px 10px",
                    "--hover-color": "#262730"},
                "nav-link-selected": {
                    "background-color": "#676b6ee6",  # highlight color
                    "font-weight": "bold"}})