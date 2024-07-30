import streamlit as st
import geopandas as gpd
from zipfile import ZipFile
import tempfile
import os
from lxml import etree
from pykml.factory import KML_ElementMaker as KML

def shapefile_to_kml(shapefile_path, kml_output_path):
    gdf = gpd.read_file(shapefile_path)

    # Create KML root
    kml = KML.kml(
        KML.Document()
    )

    for _, row in gdf.iterrows():
        geometry = row['geometry']
        if geometry.geom_type == 'Point':
            point = KML.Point(KML.coordinates(f"{geometry.x},{geometry.y}"))
            placemark = KML.Placemark(KML.name(str(row.get('name', ''))), point)
        elif geometry.geom_type == 'LineString':
            coords = " ".join([f"{x},{y}" for x, y in geometry.coords])
            line = KML.LineString(KML.coordinates(coords))
            placemark = KML.Placemark(KML.name(str(row.get('name', ''))), line)
        elif geometry.geom_type == 'Polygon':
            coords = " ".join([f"{x},{y}" for x, y in geometry.exterior.coords])
            polygon = KML.Polygon(KML.outerBoundaryIs(KML.LinearRing(KML.coordinates(coords))))
            placemark = KML.Placemark(KML.name(str(row.get('name', ''))), polygon)
        else:
            continue
        kml.Document.append(placemark)

    with open(kml_output_path, 'wb') as f:
        f.write(etree.tostring(kml, pretty_print=True))

st.title("Shapefile to KML Converter")

st.write("Upload a zipped Shapefile to convert it to a KML file.")

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
        # Convert Shapefile to KML
        base_name = os.path.splitext(uploaded_file.name)[0]
        kml_output_path = os.path.join(temp_dir, f"{base_name}.kml")
        shapefile_to_kml(shapefile_path, kml_output_path)

        # Read the KML file and return bytes
        with open(kml_output_path, 'rb') as f:
            kml_bytes = f.read()

        # Create download button for the KML file
        st.download_button(
            label="Download KML file",
            data=kml_bytes,
            file_name=f"{base_name}.kml",
            mime="application/vnd.google-earth.kml+xml"
        )
