import cv2
import numpy as np
from math import cos, sin, pi, radians

# Constants
FULL_ROTATION = 360
FULL_ROTATION_RADIANS = 2 * pi

def _restrict(val, upper_bound=1, lower_bound=-1):
    """
    Keeps a value within a specific range. If it's above the upper limit or below the lower limit, it adjusts it.

    Args:
        val (float): The value to check.
        upper_bound (float): The maximum allowed value (default is 1).
        lower_bound (float): The minimum allowed value (default is -1).

    Returns:
        float: The adjusted value if out of bounds.
    """
    return max(min(val, upper_bound), lower_bound)

def _find_points(m, b, frame_shape: tuple):
    """
    Given the slope (m) and y-intercept (b), figure out where the line intersects the edges of the frame.

    Args:
        m (float): Slope of the line.
        b (float): Y-intercept of the line.
        frame_shape (tuple): Shape of the frame as (height, width).

    Returns:
        list: Two points [(x1, y1), (x2, y2)] where the line meets the frame boundary.
    """
    # Special case for a horizontal line
    if m == 0:
        return [(0, int(b)), (frame_shape[1], int(b))]

    points = []
    height, width = frame_shape[0], frame_shape[1]

    # Check intersections with the left, top, right, and bottom borders
    if 0 < b <= height:  # Left side
        points.append((0, int(b)))
    if 0 < -b / m <= width:  # Top side
        points.append((int(-b / m), 0))
    if 0 < m * width + b <= height:  # Right side
        points.append((width, int(m * width + b)))
    if 0 < (height - b) / m <= width:  # Bottom side
        points.append((int((height - b) / m), height))

    return points

def draw_roi(frame, crop_and_scale_params):
    """
    Draws the region of interest (ROI) lines on the frame.

    Args:
        frame (np.ndarray): The image frame to draw on.
        crop_and_scale_params (dict): Cropping start/end points from `crop_and_scale.get_cropping_and_scaling_parameters`.
    """
    # Get the crop boundaries
    cropping_start = crop_and_scale_params['cropping_start']
    cropping_end = crop_and_scale_params['cropping_end']
    height = frame.shape[0]

    # Define the color and draw the lines
    off_white = (215, 215, 215)
    cv2.line(frame, (cropping_start, 0), (cropping_start, height), off_white, 1)
    cv2.line(frame, (cropping_end, 0), (cropping_end, height), off_white, 1)

def draw_hud(frame, roll, pitch, fps, is_good_horizon, recording=False):
    """
    Adds HUD (Heads-Up Display) data like roll, pitch, and FPS to the frame.

    Args:
        frame (np.ndarray): Frame to draw on.
        roll (float): Roll angle.
        pitch (float): Pitch angle.
        fps (float): Frames per second.
        is_good_horizon (bool): Flag for good horizon alignment.
        recording (bool): Flag for recording status.
    """
    # Set color based on horizon quality
    color = (255, 0, 0) if is_good_horizon else (0, 0, 255)
    roll_text = f"Roll: {int(round(roll))}" if is_good_horizon else "Roll: "
    pitch_text = f"Pitch: {int(round(pitch))}" if is_good_horizon else "Pitch: "

    # Display roll, pitch, and FPS
    cv2.putText(frame, roll_text, (20, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 1, cv2.LINE_AA)
    cv2.putText(frame, pitch_text, (20, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 1, cv2.LINE_AA)
    cv2.putText(frame, f"FPS: {fps:.2f}", (20, 120), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 1, cv2.LINE_AA)

    # Display "Recording" if recording
    if recording:
        cv2.putText(frame, "Recording", (frame.shape[1] - 140, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1, cv2.LINE_AA)

def draw_horizon(frame, roll, pitch, fov, color, draw_groundline):
    """
    Draws the horizon line on the frame based on roll and pitch angles.

    Args:
        frame (np.ndarray): Frame to draw on.
        roll (float): Roll angle in degrees.
        pitch (float): Pitch angle.
        fov (float): Field of view of the camera.
        color (tuple): Color of the horizon line.
        draw_groundline (bool): Whether to draw a groundline as well.
    """
    if roll is None:
        return

    # Convert roll to radians and calculate the horizon's center
    roll_rad = radians(roll)
    distance = pitch / fov * frame.shape[0]
    x_center = frame.shape[1] / 2 + distance * cos(roll_rad + pi / 2)
    y_center = frame.shape[0] / 2 + distance * sin(roll_rad + pi / 2)

    # Determine line points and draw
    run, rise = cos(roll_rad), sin(roll_rad)
    slope = rise / run if run != 0 else None
    points = _find_points(slope, y_center - slope * x_center if slope is not None else None, frame.shape)
    if points:
        cv2.line(frame, points[0], points[1], color, 2)

def draw_surfaces(frame, left, right, top, bottom, ail_val, elev_val, surface_color):
    """
    Draws surfaces on the frame to represent control surfaces like ailerons and elevators.

    Args:
        frame (np.ndarray): Frame to draw on.
        left, right, top, bottom (float): Frame relative positions.
        ail_val (float): Aileron value.
        elev_val (float): Elevator value.
        surface_color (tuple): Color for the control surfaces.
    """
    width = int((right - left) * frame.shape[1])
    elev_deflection = int(round(elev_val * 0.2 * (bottom - top) * frame.shape[0]))

    # Draw ailerons
    if ail_val is not None:
        ail_deflection = int(round(ail_val * 0.2 * (bottom - top) * frame.shape[0]))
        cv2.rectangle(frame, (int(left * frame.shape[1]), int(bottom * frame.shape[0])), (int(left * frame.shape[1] + 30), int(bottom * frame.shape[0] - ail_deflection)), surface_color, -1)

def draw_stick(frame, left, top, width, val1, val2, trim1, trim2, color):
    """
    Draws a joystick representation on the frame, indicating control stick positions.

    Args:
        frame (np.ndarray): Frame to draw on.
        left, top, width (float): Position and size relative to frame.
        val1, val2 (float): Stick deflections.
        trim1, trim2 (float): Trim positions.
        color (tuple): Color of the stick.
    """
    # Convert relative values to pixel positions
    cx, cy = int((left + width / 2) * frame.shape[1]), int((top + width / 2) * frame.shape[0])
    radius = int(width * frame.shape[1] / 2)
    stick_x = cx + int(radius * val1)
    stick_y = cy + int(radius * val2)

    # Draw the stick in its current position
    cv2.circle(frame, (stick_x, stick_y), 5, color, -1)

