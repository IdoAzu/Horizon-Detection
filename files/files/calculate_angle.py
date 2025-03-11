def calculate_rocket_orientation(cam1_pitch, cam1_yaw, cam2_pitch, cam2_yaw,
                                 cam3_pitch, cam3_yaw, cam4_pitch, cam4_yaw):
    """
    Calculate the rocket's overall pitch and yaw based on camera data.

    Args:
        cam1_pitch, cam1_yaw: Pitch and yaw for Camera 1 (forward-facing).
        cam2_pitch, cam2_yaw: Pitch and yaw for Camera 2 (backward-facing).
        cam3_pitch, cam3_yaw: Pitch and yaw for Camera 3 (left-facing).
        cam4_pitch, cam4_yaw: Pitch and yaw for Camera 4 (right-facing).

    Returns:
        dict: A dictionary containing the overall pitch and yaw of the rocket.
    """

    # Combine pitch data from forward and backward cameras (Camera 1 and Camera 2)

    if cam1_pitch is None and cam2_pitch is None:
        overall_pitch = 0
    elif cam1_pitch is None:
        overall_pitch = cam2_pitch
    elif cam2_pitch is None:
        overall_pitch = cam1_pitch
    else:
        overall_pitch = (cam1_pitch + cam2_pitch) / 2


    # Combine yaw data from left and right cameras (Camera 3 and Camera 4)

    if cam3_yaw is None and cam4_yaw is None:
        overall_yaw = 0
    elif cam3_yaw is None:
        overall_yaw = cam4_yaw
    elif cam4_yaw is None:
        overall_yaw = cam3_yaw
    else:
        overall_yaw = (cam3_yaw + cam4_yaw) / 2

    return [
        overall_pitch,  # Forward/backward tilt
        overall_yaw       # Left/right rotation
    ]

