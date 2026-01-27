import streamlit as st
from streamlit_option_menu import option_menu
from my_stocks.delivery import delivery
from my_stocks.qa import qa_checking
from common import get_collection

def stock_management():
    st.markdown('# Stock Management')
    cola, colb = st.columns([1, 1])
    with cola:
        sm_select = option_menu(
            menu_title=None,
            options=['Delivery', 'QA Checking'],
            icons=['truck', 'clipboard2-check'],
            orientation='horizontal',
            styles={
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px 0px",
                    "--hover-color": "#262730"},
                "nav-link-selected": {
                    "background-color": "#676b6ee6",  # highlight color
                    "font-weight": "bold"}})
        
    if sm_select=='Delivery':
        delivery()
    elif sm_select=='QA Checking':
        qa_checking()