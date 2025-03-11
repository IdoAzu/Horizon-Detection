import numpy as np

def fit_plane_from_lines(lines):
    """
    Fit a plane to 3D lines represented by points (r0) and direction vectors (d0).

    Parameters:
        lines (list of tuples): A list of inputs where each input is a tuple (r0, d0),
                                where r0 is a point on the line (x, y, z), and d0 is the direction vector (dx, dy, dz).

    Returns:
        dict: A dictionary containing the plane coefficients, the plane's normal vector, and angles to the axes.
    """
    # Generate points on the lines by sampling multiple points along each line
    points = []
    for r0, d0 in lines:
        t_values = np.linspace(-1, 1, 5)  # Generate 5 points along the line
        for t in t_values:
            point = r0 + t * np.array(d0)
            points.append(point)
        # Add the origin point (0, 0, 0)
    points.append(np.array([0, 0, 0]))
    points = np.array(points)  # Convert to numpy array

    # Separate x, y, z coordinates
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    # Construct the A matrix and b vector for Ax + b = z
    A = np.c_[x, y, np.ones(len(z))]
    b = -z

    # Solve for plane coefficients (a, b, d)
    coeffs, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    a, b, d = coeffs
    c = 1  # By definition for the plane equation

    # Normal vector of the plane
    normal_vector = np.array([a, b, c])

    # Normalize the normal vector
    normal_vector_norm = np.linalg.norm(normal_vector)
    normalized_normal = normal_vector / normal_vector_norm

    # Calculate angles between the normal vector and the axes
    angles = []
    axes = {"x": np.array([1, 0, 0]), "y": np.array([0, 1, 0]), "z": np.array([0, 0, 1])}
    for axis_name, axis_vector in axes.items():
        cos_theta = np.dot(normalized_normal, axis_vector) / np.linalg.norm(axis_vector)
        angle = np.arccos(cos_theta) * (180 / np.pi)  # Convert to degrees
        #angles[f"angle_to_{axis_name}_axis"] = angle
        angles.append(angle)

    return angles

