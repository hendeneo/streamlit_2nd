import streamlit as st
import geopandas as gpd
from zipfile import ZipFile
import tempfile
import os

def shapefile_to_geojson(shapefile_path, geojson_output_path):
    gdf = gpd.read_file(shapefile_path)
    gdf.to_file(geojson_output_path, driver="GeoJSON")

st.title("Shapefile to GeoJSON Converter")

st.write("Upload a zipped Shapefile to convert it to a GeoJSON file.")

uploaded_file = st.file_uploader("Choose a zipped Shapefile", type="zip")

if uploaded_file is not None:
    # Ensure temporary directory exists
    temp_dir = tempfile.mkdtemp()

    with ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    shapefile_path = None
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(".shp"):
                shapefile_path = os.path.join(root, file)
                break
    
    if shapefile_path is None:
        st.error("No shapefile found in the uploaded zip file.")
    else:
        # Convert Shapefile to GeoJSON
        base_name = os.path.splitext(uploaded_file.name)[0]
        geojson_output_path = os.path.join(temp_dir, f"{base_name}.geojson")
        shapefile_to_geojson(shapefile_path, geojson_output_path)

        # Read the GeoJSON file and return bytes
        with open(geojson_output_path, 'rb') as f:
            geojson_bytes = f.read()

        # Create download button for the GeoJSON file
        st.download_button(
            label="Download GeoJSON file",
            data=geojson_bytes,
            file_name=f"{base_name}.geojson",
            mime="application/geo+json"
        )
