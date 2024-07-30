import streamlit as st
import pandas as pd
import geopandas as gpd
from pykml import parser
from io import BytesIO

def parse_kml_attributes(kml_file):
    # Parse the KML file
    doc = parser.parse(kml_file)
    root = doc.getroot()
    
    # Extract placemarks
    placemarks = []
    for element in root.iter():
        if element.tag.endswith('Placemark'):
            placemarks.append(element)
    
    if not placemarks:
        raise ValueError("No Placemark elements found in the KML file.")
    
    # Create a list to store attributes
    attributes = []
    
    # Loop through placemarks and extract data
    for placemark in placemarks:
        data = {}
        for elem in placemark.iter():
            if elem.tag.endswith('name'):
                data['name'] = elem.text
            elif elem.tag.endswith('description'):
                data['description'] = elem.text
        
        attributes.append(data)
    
    # Convert attributes to a DataFrame
    df = pd.DataFrame(attributes)
    return df

st.title("KML to CSV Converter")

st.write("Upload a KML file to extract its attribute table and convert it to a CSV file.")

uploaded_file = st.file_uploader("Choose a KML file", type="kml")

if uploaded_file is not None:
    try:
        # Extract the attribute table from the KML file
        attribute_table = parse_kml_attributes(uploaded_file)
        
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
    except Exception as e:
        st.error(f"Error processing KML file: {e}")
