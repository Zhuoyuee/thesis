import numpy as np
import pyproj
from scipy.optimize import least_squares

# Define source and target CRS
crs_wgs84 = pyproj.CRS("EPSG:4326")
crs_rdnew = pyproj.CRS("EPSG:28992")

# Define transformer
transformer = pyproj.Transformer.from_crs(crs_wgs84, crs_rdnew, always_xy=True)

# Local coordinates (X, Y) and corresponding WGS84 coordinates (Longitude, Latitude)
local_coords = np.array([
    [-6.31, 10.5],
    [31.59, 96.46],
    [-81.79, 88.58],
    [-128.04, 42.15],
    [-230.05, 109.95],
    [-132.34, 51.30],
    [-226.48, 54.35],
    [-109.07, 98.24],
    [-121.35, 106.87],
    [-125.00, 111.77]
])

wgs84_coords = np.array([
    [4.376224, 52.002366],
    [4.376071, 52.003205],
    [4.374704, 52.002633],
    [4.374464, 52.002064],
    [4.372684, 52.002127],
    [4.374342, 52.002111],
    [4.373135, 52.001712],
    [4.374293, 52.002584],
    [4.374077, 52.002589],
    [4.373990, 52.002615]
])

# Convert WGS84 coordinates to RD New coordinates
rd_new_coords = np.array([transformer.transform(lon, lat) for lon, lat in wgs84_coords])

# Define function to minimize
def objective_function(x):
    # Transformation matrix parameters
    a, b, tx, c, d, ty = x
    # Compute estimated RD New coordinates using the transformation matrix
    estimated_rd_new_coords = np.dot(local_coords, np.array([[a, b], [c, d]])) + np.array([tx, ty])
    # Compute residuals between estimated and actual RD New coordinates
    return (estimated_rd_new_coords - rd_new_coords).ravel()

# Initial guess for the parameters: Identity matrix and zero translation
x0 = [1, 0, 0, 0, 1, 0]

# Perform least squares optimization
res = least_squares(objective_function, x0)

# Extract transformation matrix components
a, b, tx, c, d, ty = res.x

print(f"Affine Transformation Matrix:")
print(f"[[{a:.6f}, {b:.6f}, {tx:.2f}],")
print(f" [{c:.6f}, {d:.6f}, {ty:.2f}]]")

# Height transformation
z_offset = -0.625  # As previously calculated
print(f"Height Offset (Z): {z_offset:.3f} meters")

'''
result-
Affine Transformation Matrix:
[[0.870089, 0.490798, 85589.92],
 [-0.489936, 0.868996, 446476.01]]
Height Offset (Z): -0.625 meters'''