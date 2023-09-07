import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
from tempfile import NamedTemporaryFile

# Function to convert RGB to HEX
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

# Streamlit app
st.title("Color Detector")

# Upload an image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Create a temporary file to store the uploaded image
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        image_path = temp_file.name

    # Load the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize the image for better performance
    scale_percent = 30  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    img = cv2.resize(img, (width, height))

    # Display the image
    st.image(img, use_column_width=True, channels="RGB")

    # Flatten the image
    pixels = img.reshape((-1, 3))

    # Use K-means clustering to find dominant colors
    num_colors = st.slider("Select the number of colors to detect", 1, 10, 5)
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get the dominant colors
    dominant_colors = kmeans.cluster_centers_.astype(int)

    st.header("Dominant Colors:")
    
    # Display dominant colors and hex codes in a horizontal line
    for color in dominant_colors:
        hex_color = rgb_to_hex(color)
        st.markdown(f'<div style="display: inline-block; margin-right: 20px;"><div style="background-color: {hex_color}; width: 50px; height: 50px;"></div><div>{hex_color}</div></div>', unsafe_allow_html=True)
