import streamlit as st
import PIL
from PIL import Image
import io

st.title("Introduction to Widgets")

st.header("Types of widgets")


'Streamlit contains a wide variety of widgets, such as `st.button`, `st.slider`, `st.radio`, `st.download_button` etc...' 
'The API reference can be found in: https://docs.streamlit.io/library/api-reference/widgets'

st.header("Widget examples with code")



st.subheader("Button: `st.button`")

'The following code will allow you to create a button and generate a session_state variable "button_flag".'\
'Besides, '

code_ex1 = """
aux = st.button("Button session state button_flag_2", key='button_flag')
st.write(st.session_state)
"""
st.code(code_ex1)

### Example 1 BEGIN ###
aux = st.button("Button", key='button_flag')
st.write(st.session_state)
### Example 1 END ###




st.subheader("Download button: `st.download_button`")


'The following code will allow you to create a button and generate a session_state variable "download_button_flag"'

code_ex2 = """
some_string = 'Downloaded string when clicking in Download button generated with `st.download_button`'       
aux = st.download_button("Download button", 
                         data=some_string, 
                         key='download_button_flag',
                         file_name='download_button_str.md')
st.write(st.session_state)
"""
st.code(code_ex2)

### Example 2 BEGIN ###
some_string = 'Downloaded string when clicking in Download button generated with `st.download_button`'       
aux = st.download_button("Download button", 
                         data=some_string, 
                         key='download_button_flag',
                         file_name='download_button_str.md')
st.write(st.session_state)
### Example 2 END ###



st.subheader("Slider: `st.slider`")

'The following code will allow you to create a slider and generate a session_state variable "slider_flag"'

code_ex_3 = """
var_slider = st.slider("Button session state button_flag_2", key='slider_flag')
st.write(st.session_state)
"""
st.code(code_ex_3)


### Example 3 BEGIN ###
var_slider = st.slider("Button session state button_flag_2", key='slider_flag')
st.write(st.session_state)
### Example 3 END ###




st.subheader("File Uploader: `st.file_uploader`")


'The following code will allow you to create a file uploader widget and generate a session_state variable "slider_flag"'

code_ex_4 = """
uploaded_file = None
uploaded_file = st.file_uploader("Upload Image (.png or .jpg only)", type=['png','jpg'], key='uploader_flag')

if uploaded_file:
    bytes_uploaded_file = uploaded_file.read()
    image = Image.open(io.BytesIO(bytes_uploaded_file))
    image = image.resize((256,256))
    st.image(image)
"""
st.code(code_ex_4)

uploaded_file = None
uploaded_file = st.file_uploader("Upload Image (.png or .jpg only)", type=['png','jpg'], key='uploader_flag')

if uploaded_file:
    bytes_uploaded_file = uploaded_file.read()
    image = Image.open(io.BytesIO(bytes_uploaded_file))
    image = image.resize((256,256))
    st.image(image)





