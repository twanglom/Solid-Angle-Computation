##### approximation method

import numpy as np
import pyvista as pv

# Function to calculate the configuration factor (approximation for solid angle)
def aproximation_solid_angle(patch_position, patch_normal, point_S, area):
    """Calculate configuration factor from a source to a patch."""
    vector_to_S = point_S - patch_position
    distance = np.linalg.norm(vector_to_S)
    if distance == 0:
        return 0
    cos_theta_i = np.dot(patch_normal, vector_to_S) / distance
    return (max(cos_theta_i, 0) / (distance**2)) * area

# Load the VTK file and extract the surface
shape = pv.read('sphere.vtk')
shape = shape.extract_surface()

# Compute normals and other properties
shape.compute_normals(cell_normals=True, inplace=True, flip_normals=True)
normals = shape.cell_normals

# Calculate patch areas
cell_sizes = shape.compute_cell_sizes()
patch_areas = cell_sizes.cell_data['Area']

# Define the observation point at the center of the sphere
observation_point = np.array([0, 0, 0])

# Approximate solid angle using configuration factor approach
approx_solid_angle = 0

for i in range(shape.n_cells):
    patch_position = shape.cell_centers().points[i]  # Center of the patch
    patch_normal = normals[i]  # Normal vector of the patch
    area = patch_areas[i]  # Area of the patch
    config_factor = aproximation_solid_angle(patch_position, patch_normal, observation_point, area)
    approx_solid_angle += aproximation_solid_angle   # Multiply by the patch area

# Exact solution for solid angle of the entire sphere
exact_solid_angle = 4 * np.pi

# Print the results
print(f"Approximate Solid Angle using Configuration Factor: {approx_solid_angle}")
print(f"Exact Solid Angle: {exact_solid_angle}")
