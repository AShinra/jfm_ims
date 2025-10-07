import streamlit as st
from pymongo import MongoClient
from PIL import Image
import requests
from io import BytesIO

def connect_to_mongodb():
    try:
        
        # client = MongoClient('mongodb+srv://jeaniemoradillo1_db_user:SHozRooFXX9VRQyr@cluster0.inrodym.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        client = MongoClient('mongodb+srv://jonpuray:vYk9PVyQ7mQCn0Rj@cluster1.v4m9pq1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1')
    except Exception as e:
        st.write(e)

    return client


@st.cache_resource
def get_logo():

    url = "https://i.ibb.co/RpzG1R1d/JFM-Logo.jpg"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    image = Image.open(BytesIO(response.content))

    return image

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

    return


