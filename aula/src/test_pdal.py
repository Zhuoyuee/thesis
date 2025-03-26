import pdal
import json
import pandas as pd

def print_first_10_points(laz_file):
    # Define the PDAL pipeline
    pipeline_config = {
        "pipeline": [
            laz_file,
            {
                "type": "filters.head",
                "count": 10
            }
        ]
    }

    # Convert pipeline configuration to JSON
    pipeline_json = json.dumps(pipeline_config)

    # Create and execute PDAL pipeline
    pipeline = pdal.Pipeline(pipeline_json)
    pipeline.execute()

    # Fetch the output data as an array
    point_data = pipeline.arrays[0]  # This is a numpy structured array

    # Convert the structured array to a Pandas DataFrame for better readability
    df = pd.DataFrame(point_data)

    # Print the first 10 lines with attributes
    print(df.head(10))

# # Example usage
# print_first_10_points(r"C:\Users\wangz\thesis\good_result_clean_colour.laz")

def get_laz_metadata(laz_file):
    pipeline = pdal.Pipeline(json.dumps({"pipeline": [laz_file]}))
    pipeline.execute()
    metadata = pipeline.metadata  # Already a dict, no need for json.loads()

    # Pretty print metadata
    print(json.dumps(metadata, indent=4))


# Example usage
get_laz_metadata("C:/Users/wangz/thesis/MLS_AULA_geo.laz")

'''{
    "metadata": {
        "filters.merge": {},
        "readers.las": {
            "comp_spatialreference": "",
            "compressed": true,
            "copc": false,
            "count": 153421025,
            "creation_doy": 39,
            "creation_year": 2025,
            "dataformat_id": 3,
            "dataoffset": 333,
            "filesource_id": 0,
            "global_encoding": 0,
            "global_encoding_base64": "AAA=",
            "header_size": 227,
            "major_version": 1,
            "maxx": 115.4739,
            "maxy": 227.4153,
            "maxz": 64.5501,
            "minor_version": 2,
            "minx": -346.5222,
            "miny": -97.4359,
            "minz": -7.5563,
            "offset_x": 0,
            "offset_y": 0,
            "offset_z": 0,
            "point_length": 34,
            "project_id": "00000000-0000-0000-0000-000000000000",
            "scale_x": 0.0001,
            "scale_y": 0.0001,
            "scale_z": 0.0001,
            "software_id": "GeoSLAM",
            "spatialreference": "",
            "srs": {
                "compoundwkt": "",
                "horizontal": "",
                "isgeocentric": false,
                "isgeographic": false,
                "json": {},
                "prettycompoundwkt": "",
                "prettywkt": "",
                "proj4": "",
                "units": {
                    "horizontal": "unknown",
                    "vertical": ""
                },
                "vertical": "",
                "wkt": ""
            },
            "system_id": "libLAS",
            "vlr_0": {
                "data": "AgAAAAICAAAAAAAAUMMAAP////////////////////8DAAYAFAACAAcACAACAAgABgACAA==",
                "description": "LASzip.net DLL 2.2 r0 (140907)",
                "record_id": 22204,
                "user_id": "laszip encoded"
            }
        }
    }
}'''