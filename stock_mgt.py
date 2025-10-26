import streamlit as st
from streamlit_option_menu import option_menu

def stock_management():
    st.title('Stock Management')
    cola, colb = st.columns([1, 1])
    with cola:
        sm_select = option_menu(
            menu_title=None,
            options=['Add', 'Deduct', 'Adjust'],
            icons=['plus-lg', 'x-lg', 'pencil'],
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