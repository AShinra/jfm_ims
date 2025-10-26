import streamlit as st
from streamlit_option_menu import option_menu
import common
from datetime import date

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

    cols = st.columns([1,1,1,1])

    with cols[0]:
        with st.container(border=True):
            item_name = st.text_input(
                label='Item Name',
                key='item_name',
            )

            item_size = st.text_input(
                label='Size',
                key='item_size'
            )

            item_manufacturer = st.text_input(
                label='Manufacturer',
                key='item_manufacturer'
            )
        with st.container(border=True):
            item_add_btn = st.button(
                label='Add Item',
                key='item_add_btn',
                width='stretch'
            )
    
    if item_add_btn:
        document = {
            'item_name':st.session_state['item_name'],
            'size':st.session_state['item_size'],
            'manufacturer':st.session_state['item_manufacturer'],
            'date_added':(date.today()).isoformat()
        }

        collection = common.get_collection('items')
        collection.insert_one(document)

        # clear input fields after adding
        for key in ['item_name', 'item_size', 'item_manufacturer']:
            st.session_state[key] = ''
        
        st.rerun()

        
        




def edit_item():
    st.subheader('Edit Items')


def remove_item():
    st.subheader('Remove Items')


def sku():
    st.subheader('Assign SKU')


