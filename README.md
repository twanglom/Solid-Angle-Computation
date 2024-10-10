# Solid-Angle-Computation

### Overview
The $${\color{blue} Solid \space Angle}$$ is a geometric measure used to quantify how much an object, surface, or area appears to spread out in three dimensions from a specific point of view. It is a crucial concept in various fields such as radiation transfer, lighting, and acoustics, particularly when computing energy distribution or noise levels in environments such as rooms or spaces where external noise is considered.

This project presents an efficient method for computing the **solid angle**, particularly when the **point source** is located near a surface boundary (e.g., in **acoustic simulations considering external noise**). In these scenarios, simple approximations may become inefficient, and precise computations are required.


![image](https://github.com/user-attachments/assets/804c6430-1e7a-4fb9-bd2f-8b9a251dd39a)




---

### Table of Contents
- [Introduction](#introduction)
- [Basic Formulation](#basic-formulation)
  - [Solid Angle](#solid-angle)
  - [Spherical Triangle Method](#spherical-triangle-method)
- [Usage](#usage)
- [Example](#example)
- [License](#license)

---

### Introduction
In acoustic simulations, calculating the solid angle subtended by surfaces near a point source is crucial for determining energy transfer, especially when considering noise reflections or diffraction from room boundaries. This project provides a method that leverages the spherical triangle formulation, which is particularly efficient for surfaces near the source.

![image](https://github.com/user-attachments/assets/f88c5ecd-8c0b-43c6-aa61-37b5a9fedbb6)


---

### Basic Formulation

#### Solid Angle
The **solid angle** $( \Omega )$, subtended by a surface $( S )$ at a point $( P )$, is defined by the integral:

$$
\Omega = \int_S \frac{\mathbf{n} \cdot \mathbf{r}}{r^3} \, dS = \int_{S_i} \frac{\cos \theta}{R^2} dS
$$

where:
- $\mathbf{r}$ is the vector from the point $P$ to a differential area on the surface $dS$,
- $r = |\mathbf{r}|$ is the distance from $P$ to the surface,
- $\mathbf{n}$ is the unit normal vector to the surface,
- $\theta$ is the angle between the surface normal and the line joining the point $P$ to the surface,
- $R$ is the distance between $P$ and the surface element.


In the case where the surface can be approximated as small enough and flat, the solid angle can be computed as:

![image](https://github.com/user-attachments/assets/1e9f94c9-1728-4d0e-83b4-8df0ab3cb1b4)


where:
- $A$ is the area of the surface $S$,
- $\theta$ is the angle between the surface normal and the vector $\mathbf{r}$.

❗ **Important Note:** This approximation is commonly used when the point of observation is far enough from the surface that the curvature of the surface can be ignored.

#### Spherical Triangle Method
For surfaces that can be represented as **triangular patches**, we can use a **spherical triangle** formulation to efficiently compute the solid angle. A **spherical triangle** is formed by the intersection of three great circles on the surface of a sphere, defined by three vertices $v_1$, $v_2$, and $v_3$, which are unit vectors pointing from the origin (the observation point) to the vertices of the surface triangle.

The solid angle subtended by the spherical triangle is given by the **spherical excess** $E$, which is calculated as:

$$
\Omega = E = (\alpha + \beta + \gamma) - \pi
$$

where:
- $\alpha$, $\beta$, and $\gamma$ are the internal angles of the spherical triangle formed by the vectors $v_1$, $v_2$, and $v_3$.
  
The internal angles can be computed using the dot products of the normalized vectors:

$$
\alpha = \arccos(\mathbf{v_2} \cdot \mathbf{v_3}), \quad \beta = \arccos(\mathbf{v_1} \cdot \mathbf{v_3}), \quad \gamma = \arccos(\mathbf{v_1} \cdot \mathbf{v_2})
$$

The **spherical excess** $E$ is proportional to the area of the spherical triangle on the unit sphere, and this provides a simple and efficient way to compute the solid angle without having to rely on more computationally expensive numerical integrations.


---

### Usage
This project implements the spherical triangle method to compute the solid angle subtended by surface patches in acoustic simulations. The methodology includes:
1. **Normalization** of vectors pointing to the vertices of the surface.
2. **Computation of angles** between the surface vectors using dot products.
3. **Spherical excess calculation**, which gives the solid angle for triangular surface elements.
4. Summation of the solid angles for all surface elements to compute the total solid angle subtended by the surface from the point source.

#### Example Code
Here’s an example of how to compute the solid angle for a triangular surface patch given the vertices:

```python
import numpy as np

def spherical_triangle_solid_angle(v1, v2, v3):
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    v3 = v3 / np.linalg.norm(v3)

    a = np.arccos(np.clip(np.dot(v2, v3), -1.0, 1.0))
    b = np.arccos(np.clip(np.dot(v1, v3), -1.0, 1.0))
    c = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))

    # Spherical excess
    s = (a + b + c) / 2
    solid_angle = 4 * np.arctan(np.sqrt(np.tan(s / 2) * np.tan((s - a) / 2) * np.tan((s - b) / 2) * np.tan((s - c) / 2)))

    return solid_angle

# Example vertices (as vectors from the origin)
v1 = np.array([1, 0, 0])
v2 = np.array([0, 1, 0])
v3 = np.array([0, 0, 1])

# Compute the solid angle
angle = spherical_triangle_solid_angle(v1, v2, v3)
print(f"Solid Angle: {angle} steradians")

```
---

#### Requirements
To use this project, you'll need the following:
- **Python 3.x**
- **NumPy**: for numerical operations.
- **PyVista**: for visualization (optional, if 3D visualization is required).

---
### Example

The numerical computation of solid angle will be compared with analytical solution of sphere geometry $R = 1$ m. The numerical demonstrate using difference mesh number.   
![image](https://github.com/user-attachments/assets/b4b13285-cf92-40d5-b274-6ccaf470be9b)


```python
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
    E = 4 * np.arctan(np.sqrt(max(0, np.tan(s / 2) * np.tan((s - a) / 2) * np.tan((s - b) / 2) * np.tan((s - c) / 2))))

    # Return the solid angle
    return E

# Load the VTK file and extract the surface using pyvista
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

```

#### Results
![image](https://github.com/user-attachments/assets/1a2f910d-085c-4990-8eb2-4376a6f208d8)



