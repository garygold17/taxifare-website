import streamlit as st
import requests
from datetime import datetime


# Set up parameters for the app
title = st.title("Calculating taxi fare in new york city!")

st.image('image.png')

title2 = st.title("Enter parameters: ")

pickup_date = st.date_input('Pickup Date',datetime.now())
pickup_time = st.time_input('Pickup Time',datetime.now().time())
pickup_datetime = datetime.combine(pickup_date, pickup_time)

pickup_longitude = st.slider('Pickup Longitude', min_value=-180.0, max_value=180.0, value=0.0, step=0.01)
pickup_latitude = st.slider('Pickup Latitude', min_value=-90.0, max_value=90.0, value=0.0, step=0.01)
dropoff_longitude = st.slider('Dropoff Longitude', min_value=-180.0, max_value=180.0, value=0.0, step=0.01)
dropoff_latitude = st.slider('Dropoff Latitude', min_value=-90.0, max_value=90.0, value=0.0, step=0.01)

passenger_count = st.number_input('Passenger Count',value=0)



url = 'https://taxifare.lewagon.ai/predict'

#if url == 'https://taxifare.lewagon.ai/predict'

    #st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# Let's build a dictionary containing the parameters for our API...

api_params = {
    'pickup_datetime': pickup_datetime.strftime('%Y-%m-%d %H:%M:%S'),
    'pickup_longitude': pickup_longitude,
    'pickup_latitude': pickup_latitude,
    'dropoff_longitude': dropoff_longitude,
    'dropoff_latitude': dropoff_latitude,
    'passenger_count': passenger_count
}
# Let's call our API using the `requests` package...
if st.button('Get Fare Prediction'):
    response = requests.get(url, params=api_params)
    # Let's retrieve the prediction from the **JSON** returned by the API...
    if response.status_code == 200:
        prediction = response.json().get('fare', 'Error: No fare returned')
        st.write(f'Estimated Fare: ${prediction}')
    else:
        st.write('Error: Failed to retrieve prediction')
