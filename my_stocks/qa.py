import streamlit as st
from common import get_collection, thin_gradient_line


def qa_checking():
    collection = get_collection('deliveries')
    documents = collection.find({'status':'for checking'})

    batch_options = []
    for document in documents:
        batch_options.append(document['batch'])
    
    with st.container(border=True):
        cols = st.columns([1,1,1])
        with cols[0]:
            st.markdown('#### Batch Information')
            thin_gradient_line()
            col =st.columns([2,8])
            with col[0]:
                st.markdown('##### Batch')
            with col[1]:
                st.selectbox(
                    label='Batch',
                    label_visibility='collapsed',
                    options=batch_options,
                    key='batch_no',
                    placeholder='Select Batch',
                    index=None)
            
            st.markdown('##### Batch Details')
            thin_gradient_line()
        
        document = get_collection('deliveries').find_one({
            'batch':st.session_state['batch_no']})
    
    

    


