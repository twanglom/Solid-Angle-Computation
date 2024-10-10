###### Sphere triangle method 

import numpy as np
import pyvista as pv

# Function to calculate the solid angle subtended by a spherical triangle
def spherical_triangle_solid_angle(v1, v2, v3):
    # Normalize the vectors
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    v3 = v3 / np.linalg.norm(v3)

    # Calculate angles between vectors
    a = np.arccos(np.clip(np.dot(v2, v3), -1.0, 1.0))
    b = np.arccos(np.clip(np.dot(v1, v3), -1.0, 1.0))
    c = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))

    # Calculate the solid angle using spherical excess formula
    s = (a + b + c) / 2
    tan_half_s = np.tan(s / 2)
    tan_half_a = np.tan(a / 2)
    tan_half_b = np.tan(b / 2)
    tan_half_c = np.tan(c / 2)

    # Spherical excess
    E = 4 * np.arctan(np.sqrt(np.tan(s / 2) * np.tan((s - a) / 2) * np.tan((s - b) / 2) * np.tan((s - c) / 2)))

    # Return the solid angle
    return E

# Load the VTK file and extract the surface
shape = pv.read('sphere.vtk')
shape = shape.extract_surface()

# Define the observation point at the center of the sphere
observation_point = np.array([0, 0, 0])

# Loop through cells to get their vertices and compute the solid angle
numerical_solid_angle = 0

for i in range(shape.n_cells):
    cell = shape.extract_cells(i)
    vertices = cell.points - observation_point  # Translate vertices relative to the observation point
    
    if len(vertices) >= 3:  # Ensure we have at least a triangle
        for j in range(1, len(vertices) - 1):
            v1 = vertices[0]
            v2 = vertices[j]
            v3 = vertices[j + 1]
            numerical_solid_angle += spherical_triangle_solid_angle(v1, v2, v3)

# Exact solution for solid angle of the entire sphere
exact_solid_angle = 4 * np.pi

# Print the results
print(f"Numerical Solid Angle using Spherical Triangle Method: {numerical_solid_angle}")
print(f"Exact Solid Angle: {exact_solid_angle}")
