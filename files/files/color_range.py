import numpy as np
import cv2

def get_hsv_values_sky(hsv_frame):
    """
    Calculate the minimum and maximum HSV (Hue, Saturation, Value) values in the upper part of an HSV image frame, typically representing the sky.
    
    Parameters:
        hsv_frame (numpy.ndarray): The input HSV image frame.

    Returns:
        tuple: (min_hue, min_saturation, min_value, max_hue, max_saturation, max_value)
               Minimum and maximum HSV values in the top part of the frame.
    """
    # Calculate the top and upper-third heights of the frame
    height = hsv_frame.shape[0]
    line_height = int(3 / 4 * height)
    top_third_height = int(1 / 5 * height)

    # Extract the top part of the frame for analysis
    line = hsv_frame[line_height, :, :]
    top_third = hsv_frame[:top_third_height, :, :]

    # Calculate minimum and maximum HSV values
    max_hue = np.max(top_third[:, :, 0])
    max_saturation = np.max(top_third[:, :, 1])
    max_value = np.max(top_third[:, :, 2])
    min_hue = np.min(top_third[:, :, 0])
    min_saturation = np.min(top_third[:, :, 1])
    min_value = np.min(top_third[:, :, 2])

    return min_hue, min_saturation, min_value, max_hue, max_saturation, max_value

def get_hsv_values_ground(hsv_frame):
    """
    Calculate the minimum and maximum HSV values in the lower part of an HSV image frame, typically representing the ground.
    
    Parameters:
        hsv_frame (numpy.ndarray): The input HSV image frame.

    Returns:
        tuple: (min_hue, min_saturation, min_value, max_hue, max_saturation, max_value)
               Minimum and maximum HSV values in the lower part of the frame.
    """
    height = hsv_frame.shape[0]
    low_third_height = int(4 / 5 * height)

    # Extract the lower third of the frame for analysis
    low_third = hsv_frame[low_third_height:, :, :]

    # Calculate minimum and maximum HSV values
    max_hue = np.max(low_third[:, :, 0])
    max_saturation = np.max(low_third[:, :, 1])
    max_value = np.max(low_third[:, :, 2])
    min_hue = np.min(low_third[:, :, 0])
    min_saturation = np.min(low_third[:, :, 1])
    min_value = np.min(low_third[:, :, 2])

    return min_hue, min_saturation, min_value, max_hue, max_saturation, max_value

def get_max_hsv_values_sky_tilt(frame, tilt_degrees, frame_part, pitch):
    """
    Calculate the maximum HSV values in the upper part of a tilted frame, simulating sky detection with adjustable tilt.
    
    Parameters:
        frame (numpy.ndarray): The input image frame in HSV format.
        tilt_degrees (float): The angle to tilt the frame for analysis.
        frame_part (float): Fraction of the frame height to analyze (e.g., 1/3 for top third).
        pitch (float): Adjustment for pitch, modifying the frame height for calculations.

    Returns:
        tuple: (min_hue, min_saturation, min_value, max_hue, max_saturation, max_value)
               Minimum and maximum HSV values in the analyzed portion of the frame.
    """
    height, width, _ = frame.shape
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), tilt_degrees, 1)
    rotated_frame = cv2.warpAffine(frame, rotation_matrix, (width, height))

    pitch_height = height if pitch is None else (1 - pitch) * height
    top_third_height = int(frame_part * pitch_height)
    top_third = rotated_frame[:top_third_height, :, :]

    max_hue = np.max(top_third[:, :, 0])
    max_saturation = np.max(top_third[:, :, 1])
    max_value = np.max(top_third[:, :, 2])
    min_hue = np.min(top_third[:, :, 0])
    min_saturation = np.min(top_third[:, :, 1])
    min_value = np.min(top_third[:, :, 2])

    return min_hue, min_saturation, min_value, max_hue, max_saturation, max_value

def get_max_hsv_values_ground_tilt(frame, tilt_degrees, frame_part, pitch):
    """
    Calculate the maximum HSV values in the lower part of a tilted frame, simulating ground detection with adjustable tilt.
    
    Parameters:
        frame (numpy.ndarray): The input image frame in HSV format.
        tilt_degrees (float): The angle to tilt the frame for analysis.
        frame_part (float): Fraction of the frame height to analyze (e.g., 1/3 for bottom third).
        pitch (float): Adjustment for pitch, modifying the frame height for calculations.

    Returns:
        tuple: (min_hue, min_saturation, min_value, max_hue, max_saturation, max_value)
               Minimum and maximum HSV values in the analyzed portion of the frame.
    """
    height, width, _ = frame.shape
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), tilt_degrees, 1)
    rotated_frame = cv2.warpAffine(frame, rotation_matrix, (width, height))

    pitch_height = height if pitch is None else pitch * height
    low_third_height = int((1 - frame_part) * pitch_height)
    low_third = rotated_frame[low_third_height:, :, :]

    max_hue = np.max(low_third[:, :, 0])
    max_saturation = np.max(low_third[:, :, 1])
    max_value = np.max(low_third[:, :, 2])
    min_hue = np.min(low_third[:, :, 0])
    min_saturation = np.min(low_third[:, :, 1])
    min_value = np.min(low_third[:, :, 2])

    return min_hue, min_saturation, min_value, max_hue, max_saturation, max_value

