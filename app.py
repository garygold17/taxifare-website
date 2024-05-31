import streamlit as st
import requests
from datetime import datetime
import folium
from folium import plugins
from geopy.distance import geodesic

# Set up parameters for the app
title = st.title("Calculating taxi fare in New York City!")

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

def calculate_distance(pickup, dropoff):
    return geodesic(pickup, dropoff).kilometers

# Let's call our API using the `requests` package...
if st.button('Get Fare Prediction'):
    # Let's build a dictionary containing the parameters for our API...
    api_params = {
        'pickup_datetime': pickup_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'pickup_longitude': pickup_longitude,
        'pickup_latitude': pickup_latitude,
        'dropoff_longitude': dropoff_longitude,
        'dropoff_latitude': dropoff_latitude,
        'passenger_count': passenger_count
    }

    response = requests.get(url, params=api_params)
    # Let's retrieve the prediction from the **JSON** returned by the API...
    if response.status_code == 200:
        prediction = response.json().get('fare', 'Error: No fare returned')
        st.write(f'Estimated Fare: ${prediction}')

        # Convert pickup and dropoff coordinates to tuple
        pickup_coords = (pickup_latitude, pickup_longitude)
        dropoff_coords = (dropoff_latitude, dropoff_longitude)

        # Calculate distance
        distance = calculate_distance(pickup_coords, dropoff_coords)
        st.write(f"Distance between pickup and dropoff points: {distance:.2f} kilometers")
    else:
        st.write('Error: Failed to retrieve prediction')
