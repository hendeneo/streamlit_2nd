import streamlit as st
import geopandas as gpd
import pandas as pd
import os

st.title("GeoJSON to CSV Converter")

st.write("Upload a GeoJSON file to extract its attribute table and convert it to a CSV file.")

uploaded_file = st.file_uploader("Choose a GeoJSON file", type="geojson")

if uploaded_file is not None:
    # Read the GeoJSON file into a GeoDataFrame
    gdf = gpd.read_file(uploaded_file)
    
    # Extract the attribute table
    attribute_table = gdf.drop(columns='geometry')
    
    # Display the attribute table
    st.write("Attribute Table:")
    st.dataframe(attribute_table)
    
    # Convert the attribute table to a CSV file
    csv_file = attribute_table.to_csv(index=False).encode('utf-8')
    
    # Get the name of the uploaded file without extension
    base_name = os.path.splitext(uploaded_file.name)[0]
    
    # Create the file name for the CSV
    csv_file_name = f"{base_name}.csv"
    
    # Create download button for the CSV file
    st.download_button(
        label="Download CSV file",
        data=csv_file,
        file_name=csv_file_name,
        mime="text/csv"
    )
