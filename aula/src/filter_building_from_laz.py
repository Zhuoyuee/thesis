import pdal
import geopandas as gpd
import json
from shapely.geometry import Polygon, Point, MultiPoint
from shapely.ops import unary_union
import laspy
from sklearn.cluster import DBSCAN
import numpy as np
import alphashape

'''
Extracting buildings from merged laz file (AHN and the MLS for example)
This method is the easiest and light calculated way - using the building classification from AHN (classification = 6) to 
generate the 2D convex hulls of the building polygons. 
If this one does not work, there are more complex ways to achieve the same goal. One is to find the closest point from 
the merged laz to the AHN file, at least the ground and unclassified (buildings are only with roofs in AHN), 
then further filter it out. 

If there is no prior coarse classification, use point cloud classification method for separating ground, buildings and
the other components. 
'''

def generate_building_polygon_from_laz (laz_path, buffer_distance=1.0, alpha=1.5, clustering_eps=2.0, min_samples=30):
    with laspy.open(laz_path) as file:
        las = file.read()
        x = las.x
        y = las.y

    coords = np.column_stack((x, y))

    # 🧠 Looser DBSCAN to keep fragments together
    db = DBSCAN(eps=clustering_eps, min_samples=min_samples).fit(coords)
    labels = db.labels_

    polygons = []
    for label in np.unique(labels):
        if label == -1:
            continue
        cluster_points = coords[labels == label]
        if len(cluster_points) < 100:  # Only filter extreme noise
            continue

        shape = alphashape.alphashape(cluster_points, alpha)
        if shape and not shape.is_empty:
            if shape.geom_type == "Polygon":
                shape = Polygon(shape.exterior)
            elif shape.geom_type == "MultiPolygon":
                shape = unary_union([Polygon(p.exterior) for p in shape.geoms])
            polygons.append(shape)

    # GeoDataFrame for spatial merging
    gdf = gpd.GeoDataFrame(geometry=polygons, crs="EPSG:28992")

    # Merge fragments that are close (<4m apart) into unified buildings
    gdf["geometry"] = gdf.buffer(2)  # Pre-buffer to allow slits/gaps
    merged = unary_union(gdf.geometry)
    gdf_merged = gpd.GeoDataFrame(geometry=[merged] if merged.geom_type == "Polygon" else list(merged.geoms),
                                  crs="EPSG:28992")
    gdf_merged["geometry"] = gdf_merged.buffer(buffer_distance)  # Final outward buffer

    return list(gdf_merged.geometry)

def split_top_two_polygons(polygons):
    sorted_polygons = sorted(polygons, key=lambda p: p.area, reverse=True)
    if len(sorted_polygons) < 2:
        raise ValueError("Expected at least 2 main buildings, found less.")
    return sorted_polygons[0].wkt, sorted_polygons[1].wkt



def clip_laz_by_polygon(input_laz, polygon_wkt, output_laz):
    # PDAL pipeline using filters.crop with the buffered polygon
    pipeline = {
        "pipeline": [
            input_laz,
            {
                "type": "filters.crop",
                "polygon": polygon_wkt
            },
            {
                "type": "writers.las",
                "filename": output_laz
            }
        ]
    }

    pdal.Pipeline(json.dumps(pipeline)).execute()




building_polygons = generate_building_polygon_from_laz(
    laz_path=r"C:\Users\wangz\thesis\AULA_merge\AULA_building_AHN.laz",
    buffer_distance=1.0,
    alpha=1.5,
    clustering_eps=2.0,
    min_samples=30
)

# Step 2: Separate top two buildings
building1_wkt, building2_wkt = split_top_two_polygons(building_polygons)

# Step 3: Clip each building separately
clip_laz_by_polygon(
    input_laz=r"C:\Users\wangz\thesis\AULA_merge\AULA_merged.laz",
    polygon_wkt=building1_wkt,
    output_laz=r"C:\Users\wangz\thesis\AULA_merge\AULA_building3.laz"
)

# clip_laz_by_polygon(
#     input_laz=r"C:\Users\wangz\thesis\AULA_merge\AULA_merged.laz",
#     polygon_wkt=building2_wkt,
#     output_laz=r"C:\Users\wangz\thesis\AULA_merge\AULA_building2.laz"
# )