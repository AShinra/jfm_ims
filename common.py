import streamlit as st
from pymongo import MongoClient
from PIL import Image
import requests
from io import BytesIO
import time

@st.cache_resource
def get_client():
    client = MongoClient(st.secrets["mongo"]["uri"])
    return client

@st.cache_resource
def connect_mongodb():
    client = get_client()
    return client['jfm_ims']

@st.cache_resource
def get_collection(collection_name):
    db = connect_mongodb()
    return db[collection_name]

@st.cache_resource
def get_logo():
    url = "https://i.ibb.co/RpzG1R1d/JFM-Logo.jpg"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return Image.open(BytesIO(response.content))

@st.cache_resource
def get_bgimage():
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
    background-image: url("https://i.ibb.co/8D4hLbSX/natural-light-white-background.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;
    background-repeat: no-repeat;}</style>"""
    st.markdown(background_image, unsafe_allow_html=True)


def has_upper_and_number(text: str) -> bool:
    has_upper = any(c.isupper() for c in text)
    has_digit = any(c.isdigit() for c in text)
    if len(text)>=8:
        text_length = True
    else:
        text_length = False
    return has_upper, has_digit, text_length

def page_title(title):
    st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem; /* Adjust this value as needed (e.g., 0rem for minimal padding) */
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }    
    </style>
    """,
    unsafe_allow_html=True
    )
    
    # st.markdown(
    #     """<style>h1{color: blue !important;}</style>""", unsafe_allow_html=True)
    
    st.title(f":blue[{title}]")

def gradient_line():
    st.markdown("<hr style='border: 0; height: 10px; padding: 0; margin: 0; background: linear-gradient(to right, #444, #bbb);'/>", unsafe_allow_html=True)

def thin_gradient_line():
    st.markdown("<hr style='border: 0; height: 5px; padding: 0; margin: 0; background: linear-gradient(to right, #444, #bbb);'/>", unsafe_allow_html=True)

# -----------DIALOGS-------------

@st.dialog("Item Exists")
def exists_popup():
    st.error('❌Item already exist!')
    time.sleep(2)
    st.rerun()

@st.dialog("⚠️Clear all records!")
def clear_popup():
    collection = get_collection('temp')
    if collection.count_documents({}) > 0:
        if st.button(label='Clear all records', width='stretch'):
            collection = get_collection('temp')
            collection.delete_many({})

            st.caption('✅All Records Deleted')
            with st.spinner('Updating Records...', show_time=True):
                time.sleep(2)
                st.rerun()
    else:
        st.error('No Record to delete')


@st.dialog("❗Delete Entry")
def delete_popup():

    _options = []
    for document in get_collection('temp').find({}):
        _options.append(document['sku'])
    
    cols = st.columns([1,3])
    with cols[0]:
        st.markdown('#### Item Code')
    with cols[1]:
        _item_code = st.selectbox(
            label='Item Code',
            label_visibility='collapsed',
            options=_options,
            placeholder='Select Item Code to delete',
            index=None)
        
    if _item_code:
        if st.button(label='Delete Record', width='stretch'):
            collection = get_collection('temp')
            collection.delete_one(
                {'sku':_item_code})
            
            st.caption('✅Record Deleted Successfully')
            with st.spinner('Updating Records...', show_time=True):
                time.sleep(2)
                st.rerun()


@st.dialog("🚨Notification")
def success_popup(item_code, item_count):
    st.success("✅Successfully added")
    st.caption(f"{item_code} × {item_count}")
    with st.spinner('Updating Records...', show_time=True):
        time.sleep(2)
        st.rerun()

@st.dialog("🚨Notification")
def deliveries_popup():
    st.success("✅Items added")
    with st.spinner('Updating Records...', show_time=True):
        time.sleep(2)
        st.rerun()


@st.dialog("Modify Delivery")
def modify_delivery_popup():
    _options = []
    for document in get_collection('temp').find({}):
        _options.append(document['sku'])
    
    cols = st.columns([1,3])
    with cols[0]:
        st.markdown('#### Item Code')
    with cols[1]:
        _item_code = st.selectbox(
            label='Item Code',
            label_visibility='collapsed',
            options=_options,
            placeholder='Select Item Code to modify',
            index=None)

    if _item_code:
        collection = get_collection('temp')
        document = collection.find_one({'sku':_item_code})

        cols = st.columns([1,3])
        with cols[0]:
            st.markdown('#### New Quantity')
        with cols[1]:
            _item_count = st.number_input(
                label='Quantity',
                label_visibility='collapsed',
                min_value=0)
            
        if _item_count > 0:
            if st.button(label='Modify', width='stretch'):
                collecion = get_collection('temp')
                collection.update_one(
                    {'sku':_item_code},
                    {'$set':{'quantity':_item_count}})
                
                st.caption('✅Record Updated Successfully')
                with st.spinner('Updating Records...', show_time=True):
                    time.sleep(2)
                    st.rerun()