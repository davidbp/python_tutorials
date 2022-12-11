
import streamlit as st
from streamlit_option_menu import option_menu # need pip install streamlit_option_menu


def streamlit_menu():
    with st.sidebar:
        menu_flag = option_menu(
                menu_title="Menu",  
                options=["A", "B", "C"], 
            )
    return menu_flag

menu_flag = streamlit_menu()

if menu_flag == "A":
    st.title(f"You have selected {menu_flag}")
    "Information about A"
if menu_flag == "B":
    st.title(f"You have selected {menu_flag}")
    "Information about B"
if menu_flag == "C":
    st.title(f"You have selected {menu_flag}")
    "Information about C"
