
import streamlit as st

st.title("Making and using a button")


st.header("Button code")

st.text('The button that will appear below is created using the following code')

code_snippet = """
result = st.button("Click here")
"""

st.code(code_snippet)


st.header("Button render")

st.text('Here you have the button')
result = st.button("Click here")
st.text('Note that the button will return a boolean "True" once it is clicked.')
st.markdown(f'The result of result variable is **{result}**')


st.header("Button to display an image")

st.text('The following code will allow displaying an image once cliked. ')

code_button_flag = """
result_display_image = st.button("Display image")

if result_display_image:
    from PIL import Image
    image = Image.open('./media/europe.png')
    st.image(image, caption='European Union Flag')
"""
st.code(code_button_flag)

### code_button_flag BEGIN ###
result_display_image = st.button("Display image") 

if result_display_image:
    from PIL import Image
    image = Image.open('./media/europe.png')
    st.image(image, caption='European Union Flag')
### code_button_flag END ###

st.text('Note that the image will remain visible even if the button is clicked again,')
st.text('this happens because the variable "result_display_image" that stores if the user has')
st.text('clicked the button does not change.')








st.header("Button to update session state variable")

st.text('The following code will allow changing the session_state variable "button_flag"')
st.text('after a button is called.')


code_ex2 = """
if 'button_flag' not in st.session_state:
    st.session_state.button_flag = False

button_pressed = st.button("Button session state button_flag")

if button_pressed:
    st.session_state.button_flag = not st.session_state.button_flag
    st.text(f"after pressing button st.session_state is:")
    st.write(st.session_state)
"""
st.code(code_ex2)

### Example2 BEGIN ###
if 'button_flag' not in st.session_state:
    st.session_state.button_flag = False

button_pressed = st.button("Button session state button_flag")

if button_pressed:
    st.session_state.button_flag = not st.session_state.button_flag
    st.text(f"after pressing button st.session_state is:")
    st.write(st.session_state)
### Example2 END ###




