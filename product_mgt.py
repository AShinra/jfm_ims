import streamlit as st
from streamlit_option_menu import option_menu

def product_management():
    st.title('Product Management')
    cola, colb = st.columns([1, 1])
    with cola:
        pm_select = option_menu(
            menu_title=None,
            options=['Add', 'Edit', 'Remove', 'Assign SKU'],
            icons=['plus-lg', 'pencil', 'x-lg', 'upc'],
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
    
    if pm_select=='Add':
        add_item()
    elif pm_select=='Edit':
        edit_item()
    if pm_select=='Remove':
        remove_item()
    if pm_select=='Assign SKU':
        sku()


def add_item():
    st.subheader('Add Items')
    


def edit_item():
    st.subheader('Edit Items')


def remove_item():
    st.subheader('Remove Items')


def sku():
    st.subheader('Assign SKU')


