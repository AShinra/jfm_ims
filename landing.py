import streamlit as st
from streamlit_option_menu import option_menu
from common import connect_to_mongodb
from product_mgt import add_item                                                                                                                                                                                                            


def main(username, rights):

    client = connect_to_mongodb()
    with st.sidebar:
        if rights=='admin':
            options_list=['Product Management', 'Stock Management', 'Tracking & Reports', 'Search & Filters', 'User Management']
            icons_list=['box2-fill', 'bag-fill', 'body-text', 'search', 'people-fill']
        elif rights=='sub-admin':
            options_list=['Entry', 'Archive', 'Summary', 'Client Management']
            icons_list=['pencil-square', 'archive', 'journals', 'gear']
        else:
            options_list=['Archive', 'Summary']
            icons_list=['archive', 'journals']

        st.sidebar.header(f':red[Welcome :blue[*{username.title()}*]] 👤')
        selected = option_menu(
            menu_title='JFM Inventory',
            menu_icon='list-columns',
            options=options_list,
            icons=icons_list
        )
        btn_clearcache = st.button(':orange[**Clear Cache**]', use_container_width=True)
    
    # client_list = []
    if selected=='Product Management':
        with st.sidebar:
            pm_select = option_menu(
                menu_title='Items',
                options=['Add', 'Edit', 'Remove', 'Assign SKU'],
                icons=['plus-lg', 'pencil', 'x-lg', 'upc'],
            )
            
    elif selected=='Stock Management':
        with st.sidebar:
            sm_select = option_menu(
                menu_title='Stocks',
                options=['Add', 'Deduct', 'Adjust'],
                icons=['plus-lg', 'x-lg', 'pencil']
            )
    elif selected=='Tracking & Reports':
        with st.sidebar:
            tr_select = option_menu(
                menu_title='Reports',
                options=['Current Stock', 'Low Stock', 'Transaction History', 'Inventory Valuation'],
                icons=['box-seam-fill', 'exclamation-diamond', 'hourglass-split', 'ui-checks']
            )


        
    
    
    
    

