'''

(-6.31, 10.5) (52.002366, 4.376224)
(31.59, 96.46) (52.003205, 4.376071)
(-81.79,88.58) (52.002633, 4.374704)
(-128.04, 42.15)(52.002064, 4.374464)
(-230.05, 109.95)(52.002127, 4.372684)
(-132.34, 51.30) (52.002111, 4.374342)
(-226.48, 54.35)(52.001712, 4.373135)
(-109.07,98.24)(52.002584, 4.374293)
(-121.35,106.87)(52.002589, 4.374077)
(-125.00,111.77)(52.002615, 4.373990)

z: local 0.17 -0.455 NAP
'''


import pdal
import json

def transform_laz_with_pdal(input_file, output_file):
    pipeline_json = {
        "pipeline": [
            {
                "type": "readers.las",
                "filename": input_file
            },
            {
                "type": "filters.transformation",
                "matrix": "0.870089 0.490798 0 85589.92 -0.489936 0.868996 0 446476.01 0 0 1 -0.625 0 0 0 1"
            },
            {
                "type": "writers.las",
                "filename": output_file,
                "a_srs": "EPSG:28992"  # Assigning the correct projection
            }
        ]
    }

    pipeline = pdal.Pipeline(json.dumps(pipeline_json))
    pipeline.execute()
    print("Transformation applied and saved to:", output_file)

# Run transformation
transform_laz_with_pdal("C:/Users/wangz/thesis/MLS_AULA.laz", "C:/Users/wangz/thesis/MLS_AULA_georeference.laz")
