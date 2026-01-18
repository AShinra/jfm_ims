import streamlit as st
from streamlit_option_menu import option_menu
from common import get_collection
from datetime import date
import pandas as pd

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
    with colb:
        collection = get_collection("items")
        documents = collection.find({})

        df = pd.DataFrame(documents)
        st.dataframe(df)
    
    if pm_select=='Add':
        add_item()
    elif pm_select=='Edit':
        edit_item()
    if pm_select=='Remove':
        remove_item()
    if pm_select=='Assign SKU':
        sku()


def add_item():

    # --- Reset inputs before rendering if requested ---
    if "clear_inputs" in st.session_state and st.session_state.clear_inputs:
        for key in ['item_name', 'item_manufacturer']:
            st.session_state[key] = ''
        st.session_state['item_size'] = 1
        st.session_state['unit_size'] = 'GRAMS'
        st.session_state.clear_inputs = False

    cols = st.columns([1,1,1,1])

    with cols[0]:
        with st.container(border=True):
            item_name = st.text_input(
                label='Item Name',
                key='item_name',
            )

            col1, col2 = st.columns(2)
            with col1:
                item_size = st.number_input(
                    label='Size',
                    key='item_size',
                    min_value=1,
                    step=1,
                    format="%d"
                )

            with col2:
                unit_size = st.selectbox(
                    label='Unit',
                    options=[
                        'GRAMS',
                        'KG',
                        'ML',
                        'LTR',
                        'OZ',
                        'GAL',
                        'SACK'],
                    key='unit_size')

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

        collection = get_collection('items')

        query = {
            'item_name':st.session_state['item_name'].upper(),
            'size':f"{st.session_state['item_size']} {st.session_state['unit_size']}",
            'manufacturer':st.session_state['item_manufacturer'].upper()}

        if collection.find_one(query):
            st.warning("⚠️ This item already exists!")
        else:
            collection.insert_one({
                **query,
                'date_added':(date.today()).isoformat()})

            # Flag to clear on next rerun
            st.session_state.clear_inputs = True
            st.rerun()

        
        




def edit_item():
    st.subheader('Edit Items')

def remove_item():
    st.subheader('Remove Items')


def sku():
    st.subheader('Assign SKU')


