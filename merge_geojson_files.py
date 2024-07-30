import streamlit as st
import geopandas as gpd
import zipfile
import io
import pandas as pd

def extract_geojson_from_zip(zip_file):
    geojson_files = []
    with zipfile.ZipFile(zip_file, 'r') as z:
        for file_info in z.infolist():
            if file_info.filename.endswith('.geojson'):
                with z.open(file_info.filename) as f:
                    geojson_files.append((file_info.filename, f.read()))
    return geojson_files

def merge_geojson_files(geojson_files):
    gdfs = []
    for filename, content in geojson_files:
        gdf = gpd.read_file(io.BytesIO(content))
        gdf['sourcegeojson'] = filename
        gdfs.append(gdf)
    merged_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)
    return merged_gdf

def main():
    st.title("Merge GeoJSON Files")

    st.write("Upload a ZIP folder containing multiple GeoJSON files to merge them into a single GeoJSON file.")

    uploaded_zip = st.file_uploader("Choose a ZIP file", type="zip")

    if uploaded_zip is not None:
        with st.spinner("Processing..."):
            geojson_files = extract_geojson_from_zip(uploaded_zip)
            if not geojson_files:
                st.error("No GeoJSON files found in the ZIP.")
                return

            merged_gdf = merge_geojson_files(geojson_files)

            # Convert GeoDataFrame to DataFrame for display (excluding geometry column)
            df = merged_gdf.drop(columns='geometry')

            # Display the attribute table
            st.write("Attribute Table:")
            st.dataframe(df)

            # Save the merged GeoDataFrame to a GeoJSON file
            geojson_output = io.BytesIO()
            merged_gdf.to_file(geojson_output, driver='GeoJSON')
            geojson_output.seek(0)

            # Provide download button
            st.download_button(
                label="Download Merged GeoJSON",
                data=geojson_output.getvalue(),
                file_name="merged.geojson",
                mime="application/geo+json"
            )

if __name__ == "__main__":
    main()


