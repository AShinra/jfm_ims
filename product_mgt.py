import streamlit as st
from streamlit_option_menu import option_menu
from common import get_collection
from datetime import date, datetime
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
        ''''''
        
    
    if pm_select=='Add':
        add_item()
    elif pm_select=='Edit':
        edit_item()
    if pm_select=='Remove':
        remove_item()
    if pm_select=='Assign SKU':
        sku()


def add_item():

    collection = get_collection('main_categories')
    documents = collection.find({})
    for document in documents:
        category_options = document['categories']

    # --- Reset inputs before rendering if requested ---
    if "clear_inputs" in st.session_state and st.session_state.clear_inputs:
        for key in ['product_name', 'variant', 'brand', 'manufacturer', 'brand_name', 'main_cat', 'sub_cat']:
            st.session_state[key] = ''
        st.session_state['item_size'] = 1
        st.session_state['unit_size'] = 'GRAMS'
        st.session_state.clear_inputs = False

    cols = st.columns([1, 3])

    with cols[0]:
        with st.container(border=True):
            product_label, product_data = st.columns([3.5, 6.5])
            with product_label:
                st.write('Product')
            with product_data:
                product = st.text_input(
                    label=':red[*]Product Name',
                    label_visibility='collapsed',
                    key='product_name')
            
            variant_label, variant_data = st.columns([3.5, 6.5])
            with variant_label:    
                st.write('Variant')
            with variant_data:
                variant = st.text_input(
                    label=':red[*]Variant',
                    label_visibility='collapsed',
                    key='variant')
            
            brand_label, brand_data = st.columns([3.5, 6.5])
            with brand_label:
                st.write('Brand')
            with brand_data:
                brand = st.text_input(
                    label=':red[*]Brand Name',
                    label_visibility='collapsed',
                    key='brand_name')
            
            cols1, cols2 = st.columns(2)
            with cols1:
                size_label, size_data = st.columns([3, 7])
                with size_label:
                    st.write('Size')
                with size_data:
                    item_size = st.number_input(
                        label='Size',
                        label_visibility='collapsed',
                        key='item_size',
                        min_value=1,
                        step=1,
                        format="%d")
            with cols2:
                unit_label, unit_data = st.columns([3, 7])
                with unit_label:
                    st.write('Unit')
                with unit_data:
                    unit_size = st.selectbox(
                    label='Unit',
                    label_visibility='collapsed',
                    options=[
                        'GRAMS',
                        'KG',
                        'ML',
                        'LTR',
                        'OZ',
                        'GAL',
                        'SACK'],
                    key='unit_size')


            
            manufacturer_label, manufacturer_data = st.columns([3.5, 6.5])
            with manufacturer_label:
                st.write('Manufacturer')
            with manufacturer_data:
                manufacturer = st.text_input(
                    label=':red[*]Manufacturer',
                    label_visibility='collapsed',
                    key='manufacturer')
                
            maincat_label, maincat_data = st.columns([3.5, 6.5])
            with maincat_label:
                st.write('Category')
            with maincat_data:
                main_category = st.selectbox(
                    label='Main Category',
                    label_visibility='collapsed',
                    options=category_options,
                    placeholder='Select Main Category',
                    index=None,
                    key='main_cat')
                
            if main_category:

                collection = get_collection('sub_categories')
                document = collection.find_one({'category':main_category})
                sub_cat_options = document['data']

                subcat_label, subcat_data = st.columns([3.5, 6.5])
                with subcat_label:
                    st.write('Sub')
                with subcat_data:
                    sub_category = st.selectbox(
                        label='Sub Category',
                        label_visibility='collapsed',
                        options=sub_cat_options,
                        placeholder='Select Sub Category',
                        index=None,
                        key='sub_cat')

           

        
            item_add_btn = st.button(
                label='Add Item',
                key='item_add_btn',
                width='stretch'
            )

    with cols[1]:
        # collection = get_collection("items")
        # documents = collection.find({})
            
        # df = pd.DataFrame(documents)
        # st.dataframe(df, hide_index=True)

        collection = get_collection("items")
        documents = collection.find({})
        all_items = []
        for document in documents:
            _items = {}
            _items['Product'] = document['product']
            _items['Variant'] = document['variant']
            _items['Brand'] = document['brand']
            _items['Size'] = f"{document['size']['value']} {document['size']['unit']}"
            _items['Manufacturer'] = document['manufacturer']
            all_items.append(_items)
        
        df = pd.DataFrame(all_items)
        st.dataframe(df, hide_index=True)

            
    
    if item_add_btn:

        collection = get_collection('items')

        if product in [None, ''] or brand in [None, ''] or manufacturer in [None, ''] or variant in [None, '']:
            st.toast('⚠️ Missing Item Information')
        else:

            product = product.upper()
            variant = variant.upper()
            brand = brand.upper()
            manufacturer = manufacturer.upper()

            query = {
                'product':product,
                'variant':variant,
                'brand':brand,
                'manufacturer':manufacturer,
                'category':{
                    'main':main_category,
                    'sub':sub_category},
                'size':{
                    'value':item_size,
                    'unit':unit_size}}
            
            if collection.find_one(query):
                st.warning("⚠️ This item already exists!")
            else:
                collection.insert_one({
                    **query,
                    'created_at':datetime.now(),
                    'updated_at':datetime.now(),
                    'status':'',
                    'sku':''})
            
                st.session_state.clear_inputs = True
                st.rerun()
       

        # if collection.find_one(query):
        #     st.warning("⚠️ This item already exists!")
        # else:
        #     collection.insert_one({
        #         **query,
        #         'date_added':(date.today()).isoformat()})

        #     # Flag to clear on next rerun
        #     st.session_state.clear_inputs = True
        #     st.rerun()

        
        




def edit_item():
    st.subheader('Edit Items')

def remove_item():
    st.subheader('Remove Items')


def sku():
    st.subheader('Assign SKU')


