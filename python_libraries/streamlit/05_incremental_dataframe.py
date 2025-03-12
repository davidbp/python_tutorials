# This exapmles shows how to increment a dataframe every time a button is pressed

import streamlit as st
import io
import pandas as pd

df = pd.DataFrame()
st.title("Add Movies and related words to a table")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
    st.session_state.df_csv = None 

related_words = None
movie = None

def update_df(st, movie, related_words):
    df_current = pd.DataFrame({'movie': movie, 'asin_examples': [related_words] })
    st.session_state.df = pd.concat((st.session_state.df, df_current))
    st.write(f'Added {len(related_words)} related terms')
    st.session_state.df_csv = st.session_state.df.to_csv(index=True).encode("utf-8")

def clear_df():
    st.session_state.df = pd.DataFrame()
    st.session_state.df_csv = None

new_movie_container = st.container()
new_movie = new_movie_container.text_input('Write here Movie to add')

related_words_container = st.container()
related_words = related_words_container.text_input('related words')

if related_words:
    related_words = related_words.split(',')

st.write('Number of movies added so far:', len(st.session_state.df))
added_data = st.button('Add related words', 
                       on_click=update_df,  
                       kwargs=dict(st=st, movie=new_movie, related_words=related_words) )
st.button('Clear data', on_click=clear_df())

if added_data:
    download_button = st.download_button("Download button", 
                            data=st.session_state.df.to_csv(index=True).encode("utf-8"), 
                            key='download_button_flag',
                            file_name='df.csv')

