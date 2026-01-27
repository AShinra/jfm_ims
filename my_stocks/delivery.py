import streamlit as st
from common import thin_gradient_line, get_collection, clear_popup, delete_popup, exists_popup, success_popup, deliveries_popup, modify_delivery_popup
import pandas as pd
from datetime import datetime, date

  
def delivery():
    supplier_options = []
    supplier_collection = get_collection('suppliers')
    documents = supplier_collection.find({})
    for document in documents:
         supplier_options.append(document['name'])

    items_collection = get_collection('sku')
    documents = items_collection.find({})
    for document in documents:
        sku_options = document['sku_list']

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        with st.container(border=True):
            st.markdown('#### Delivery Information')
            thin_gradient_line()

            cols = st.columns([1,1])
            with cols[0]:
                st.markdown('##### Delivery Date')
            with cols[1]:
                delivery_date = st.date_input(
                    label='Delivery Date',
                    label_visibility='collapsed',
                    key='delivery_date')
                
            cols = st.columns([1,1])
            with cols[0]:
                st.markdown('##### Delivery Time')
            with cols[1]:
                delivery_date = st.time_input(
                    label='Delivery Time',
                    label_visibility='collapsed',
                    key='delivery_time')
            
            cols = st.columns([1,1])
            with cols[0]:
                st.markdown('##### Supplier')
            with cols[1]:
                supplier_name = st.selectbox(
                    label='Supplier/Vendor',
                    label_visibility='collapsed',
                    key='supplier_name',
                    options=supplier_options,
                    placeholder='Select Supplier',
                    index=None)
                
            colpo1, colpo2 = st.columns(2)
            with colpo1:
                st.markdown('##### Purchase Order No.')
            with colpo2:
                po_number = st.text_input(
                    label='Purchase Order No.',
                    label_visibility='collapsed',
                    key='po_number')
            
            colre1, colre2 = st.columns(2)
            with colre1:
                st.markdown('##### Received by')
            with colre2:
                received_by = st.text_input(
                    label='Received by',
                    label_visibility='collapsed',
                    key='received_by')
                
    
        with st.container(border=True):
            st.markdown('#### Item Details')
            thin_gradient_line()
            cols = st.columns([4,6])
            with cols[0]:
                st.markdown('##### Item Code/SKU')
            with cols[1]:
                item_code = st.selectbox(
                    label='Item Code/SKU',
                    label_visibility='collapsed',
                    options=sorted(sku_options),
                    key='item_code',
                    placeholder='Select Item Code',
                    index=None)
                
            if item_code:
                document = get_collection('items').find_one({'sku':item_code})
                cols = st.columns([4,6])
                with cols[0]:
                    st.markdown('##### Product Details')
                with cols[1]:
                    st.text_area(
                        label='Product Details',
                        value=f"{document['brand']}\n{document['product']} {document['size']['value']}{document['size']['unit']}\n{document['variant']}\n")

                cols = st.columns([4,6])
                with cols[0]:
                    st.markdown('##### Quantity')
                with cols[1]:
                    item_count = st.number_input(
                        label='Items',
                        label_visibility='collapsed',
                        min_value=0)
                    
                    if item_count > 0:
                        if st.button(label='Add', width='stretch'):
                            collection = get_collection('temp')
                            result = collection.find_one({
                                'sku':item_code})
                            
                            if result:
                                exists_popup()
                            else:
                                get_collection('temp').insert_one({
                                    'sku':item_code,
                                    'quantity':item_count})
                                success_popup(item_code, item_count)


    with col2:
        with st.container(border=True):
            st.markdown('#### Delivery Details')
            thin_gradient_line()
            collection = get_collection('temp')
            documents = collection.find({})
            df = pd.DataFrame(documents)
            try:
                st.dataframe(df[['sku', 'quantity']], hide_index=True)
            except:
                pass
            
            if get_collection('temp').count_documents({}) > 0:
                cols = st.columns([1,1,1])
                with cols[0]:
                    if st.button(label='Modify Entry', key='btn_modify',width='stretch'):
                        modify_delivery_popup()
                
                with cols[1]:
                    if st.button(label='Delete Entry',key='btn_delete',width='stretch'):
                        delete_popup()
                
                with cols[2]:
                    if st.button(label='Clear',key='btn_clear',width='stretch'):
                        clear_popup()

                if st.button(label='Submit',key='btn_submit',width='stretch'):
                    delivery_collection = get_collection('deliveries')

                    current_year = date.today().year
                    _count = delivery_collection.count_documents({}) + 1

                    if _count < 10:
                        batch_no = str(f'{current_year}-000{_count}')
                    elif _count >= 10 and _count < 100:
                        batch_no = str(f'{current_year}-00{_count}')
                    elif _count >= 100 and _count < 1000:
                        batch_no = str(f'{current_year}-0{_count}')
                    else:
                        batch_no = str(f'{current_year}-{_count}')
                    
                    delivery_schedule = datetime.combine(st.session_state['delivery_date'], st.session_state['delivery_time'])

                    items = []
                    temp_collection = get_collection('temp')
                    for document in temp_collection.find({}):
                        item_dict = {}
                        item_dict['sku'] = document['sku']
                        item_dict['quantity'] = document['quantity']
                        items.append(item_dict)
                    delivery_collection.insert_one({
                        'delivery_schedule':delivery_schedule,
                        'supplier':st.session_state['supplier_name'],
                        'po_number':st.session_state['po_number'],
                        'receiver':st.session_state['received_by'],
                        'items':items,
                        'status':'for_checking',
                        'batch':batch_no})
                    
                    temp_collection = get_collection('temp')
                    temp_collection.delete_many({})
                    deliveries_popup()
                
                    
                






                


                
            
            