
import streamlit as st
from PIL import Image
import numpy as np
import requests


## Streamlit app
#st.title("Shark-ID")
#st.text("Upload an image to predict the shark species.")

#now lokal, later we will put it to google cloud

url = 'https://shark-api-o7bru5oetq-ew.a.run.app'


# Shark-ID front

buffer_image = st.file_uploader('Upload an Image')
if buffer_image is not None:
    image = Image.open(buffer_image)
    image_array= np.array(image) # if you want to pass it to OpenCV
    st.image(image_array, caption="The caption", use_column_width=True)


# Make the prediction
if st.button('Predict'):
    #prediction = predict_image(image)
    st.text("This is the prediction:")
    #st.write(prediction)
    img_bytes = buffer_image.getvalue()
    res = requests.post(url + "/predict_file", files={'file': img_bytes})
    print(res)
    if res.status_code == 200:
        ### Display the image returned by the API
        st.text(res.json())
    else:
        st.markdown("**Oops**, something went wrong 😓 Please try again.")
        print(res.status_code, res.content)
