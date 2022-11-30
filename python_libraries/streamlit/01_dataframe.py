import pandas as pd
import streamlit as st

st.title("Data Frame visualization")


st.header("Dataframe collection")

# st.subheader() makes bold "subheader like text"
st.subheader("1) Small dataframe")

# st.write() prints standard text
st.write("The ABC DataFrame containing 3 columns and 4 observations")

st.write(
pd.DataFrame({
    'A': [1, 5, 9, 10],
    'B': [3, 2, 4, 8],
    'C': [2, 2, 1, 1]
  })
)
st.caption('3x4 dataframe', unsafe_allow_html=False)
st.subheader("2) Medium dataframe")


st.write("The ABC DataFrame containing 3 columns and 7 observations")
st.write(
pd.DataFrame({
    'A': [1, 5, 9, 10, 4, 5, 7],
    'B': [3, 2, 4, 8, 33, 4, 5], 
    'C': [2, 2, 1, 1, 11, 2, 4] 
  })
)   
st.caption('3x8 dataframe', unsafe_allow_html=False)


 

