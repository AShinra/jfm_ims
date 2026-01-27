import streamlit as st
from common import get_logo, get_collection
from argon2 import PasswordHasher
from home import main



if __name__ == '__main__':

    hide_streamlit_style = """<style>
    ._profileContainer_gzau3_63{display: none;}
    </style>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem;}

        h1, h2, h3, h4, h5, h6 {
            margin-top: 0px !important;
            margin-bottom: 0px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            line-height: 1.1;}
        
        /* ---------- TEXTAREA ---------- */    
        div[data-baseweb="textarea"] textarea {
                color: #F5F5F5;
                background-color: #1A1A1A;}

        /* ---------- INPUTBOX ---------- */    
        /* Input text */
        div[data-baseweb="input"] input {
                color: #F5F5F5;
                background-color: #1A1A1A;}

        /* Placeholder text */
        div[data-baseweb="input"] input::placeholder {color: #7A7A7A;}
        
        /* ---------- SELECTBOX ---------- */
        div[data-baseweb="select"] > div {
                background-color: #1A1A1A;
                color: #F5F5F5;}
        
        /* ---------- BUTTON ---------- */
        div.stButton > button {
                background-color: #FFC400;
                color: #111111;
                border: none;
                border-radius: 8px;
                padding: 0.6em 1.2em;
                font-weight: 600;}
        
        /* Hover */
        div.stButton > button:hover {
                background-color: #111111;
                color: #FFC400;}

        </style>
        """, unsafe_allow_html=True)

    st.set_page_config(
        layout="wide",
        page_title='Joseph Feeding Mission - Inventory Management System')
    
    # hide streamlit toolbar
    st.markdown("""<style>[data-testid="stToolbar"] {display: none;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>[data-testid="manage-app-button"] {display: none !important;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>[data-testid="stSidebarCollapseButton"] {display: none !important;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>[data-testid="stSidebarHeader"] {height: 1rem;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>.stSidebar.st-emotion-cache-1legitb {background-color: black;}</style>""", unsafe_allow_html=True)
    
    try:
        st.sidebar.image(get_logo())
    except Exception as e:
        st.sidebar.warning("Logo cannot be loaded.")
        st.exception(e)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if 'username' not in st.session_state:
        st.session_state.username = ''
    
    if 'rights' not in st.session_state:
        st.session_state.rights = ''
    
    ph = PasswordHasher()
    user_collection = get_collection('users')
        
    if st.session_state.logged_in:
        main(st.session_state.username, st.session_state.rights)
        with st.sidebar:
            if st.button('**Log Out**', use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()

    else:
        with st.sidebar:
            username = st.text_input(
                label="**USERNAME**",
                key='login_username')
            password = st.text_input(
                label="**PASSWORD**",
                type="password",
                key='login_password')
            submit_btn = st.button(
                label='**LOGIN**',
                use_container_width=True,
                key='login_submit_btn'
            )

        if submit_btn:
            doc = user_collection.find_one({"username": username})
            if not doc:
                st.sidebar.error("No such user")
            else:
                try:
                    ph.verify(doc["password_hash"], password)
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.rights = doc['rights']
                    st.rerun()
                except Exception:
                    st.sidebar.error("Wrong password")
    
        
