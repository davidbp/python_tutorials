# This exapmles shows how to increment a dataframe every time a button is pressed

import streamlit as st
import SessionState

st.title("Add words to a list when clicking a button")

words = []

ss = SessionState.get(words=words)

container1 = st.container()
new_word = container1.text_input('Write here word to add')
container2 = st.container()
add_button = container2.button('add')

if add_button:
    ss.words.append(new_word)

st.write(ss.words)