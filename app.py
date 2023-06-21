#User -> input picture
#Picture→ preprocessed
#	→ run through model

import streamlit as st
from PIL import Image
import numpy as np
import requests
import pandas as pd

# Prepare variables etc.
buffer_image = None
API_URL = 'https://shark-api-o7bru5oetq-ew.a.run.app'

classes = {'basking': 0, 'blue': 1, 'hammerhead': 2, 'mako': 3, 'sand tiger': 4, 'tiger': 5, 'white' : 6,
            'blacktip': 7 , 'bull': 8, 'lemon':9 , 'nurse': 10, 'thresher': 11, 'whale': 12, 'whitetip': 13}
nice_names = [f'{_.capitalize()} Shark' for _ in classes.keys()]
classes = dict(zip(nice_names, list(classes.values())))

## Streamlit app
st.set_page_config(layout='wide',
                   page_title='Sharks prediction',
                   page_icon='https://i.ibb.co/5GGxjMt/1f988.jpg')

# gh link
'''
[![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/nikkernoodle/shark-id)
'''

# add a title to the page and the shark emoji
st.title("Shark-ID")
st.markdown("**Upload an image to predict the shark species.**")

# model
# load_model takes model_path as an argument
# we need to be able to give the model path as an argument
# to predict the image we need to then create something else using predict_image

# Shark-ID front
buffer_image = st.file_uploader('', label_visibility='hidden')

if buffer_image is not None:
    col1, col2 = st.columns(2)

    with col1:
        image = Image.open(buffer_image)
        image_array= np.array(image) # if you want to pass it to OpenCV
        st.image(image_array, width=int(0.4*1920))

    with col2:
        with st.spinner('Sharking...'):
            img_bytes = buffer_image.getvalue()
            res = requests.post(API_URL + "/predict_file", files={'file': img_bytes})

            if res.status_code == 200:
                st.markdown("**This shark could be:**")

                # Display the prediction returned by the API
                prediction = pd.DataFrame(res.json(), columns=['Probability'], index=classes)
                prediction.sort_values(by='Probability', ascending=False, inplace=True)
                output = [f'{round(_*100, 2)}%' for _ in prediction.Probability.values]
                prediction['Probability'] = output
                st.dataframe(prediction[0:3])
            else:
                st.markdown("**Oops**, something went wrong 😓 Please try again.")
                print(res.status_code, res.content)

# background image
page_bg_img = '''
<style>
.stApp {
  background-image: url("https://upload.wikimedia.org/wikipedia/commons/c/c5/Biscayne_underwater_NPS1.jpg");
  background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)
