import streamlit as st
import geopandas as gpd
import pandas as pd
import os
import zipfile
import tempfile

st.title("Shapefile to CSV Converter")

st.write("Upload a zipped Shapefile to extract its attribute table and convert it to a CSV file.")

uploaded_file = st.file_uploader("Choose a zipped Shapefile", type="zip")

if uploaded_file is not None:
    # Create a temporary directory to extract the uploaded zip file
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "uploaded_shapefile.zip")
    
    # Save the uploaded zip file to the temporary directory
    with open(zip_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Find the shapefile in the extracted files
    shapefile_path = None
    for file_name in os.listdir(temp_dir):
        if file_name.endswith(".shp"):
            shapefile_path = os.path.join(temp_dir, file_name)
            break
    
    if shapefile_path is None:
        st.error("No shapefile (.shp) found in the uploaded zip file.")
    else:
        # Read the shapefile into a GeoDataFrame
        gdf = gpd.read_file(shapefile_path)
        
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
