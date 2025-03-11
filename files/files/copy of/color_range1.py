import numpy as np
import cv2


def get_hsv_values_sky(hsv_frame):

    # Calculate the height at 2/3 of the frame
    height = hsv_frame.shape[0]
    line_height = int(3/4 * height)
    top_third_height = int(1/5 * height)

    # Extract the line from the frame
    line = hsv_frame[line_height, :, :]
    top_third = hsv_frame[:top_third_height, :, :]

    # Calculate the maximum H, S, and V values in the line
    max_hue = np.max(top_third[:, :, 0])
    max_saturation = np.max(top_third[:, :, 1])
    max_value = np.max(top_third[:, :, 2])
    min_hue = np.min(top_third[:, :, 0])
    min_saturation = np.min(top_third[:, :, 1])
    min_value = np.min(top_third[:, :, 2])

    return min_hue,min_saturation,min_value, max_hue, max_saturation, max_value

def get_hsv_values_ground(hsv_frame):

    # Calculate the height at 2/3 of the frame
    height = hsv_frame.shape[0]
    line_height = int(3/4 * height)
    low_third_height = int(4/5 * height)

    # Extract the line from the frame
    low_third = hsv_frame[low_third_height:, :, :]

    # Calculate the maximum H, S, and V values in the line
    max_hue = np.max(low_third[:, :, 0])
    max_saturation = np.max(low_third[:, :, 1])
    max_value = np.max(low_third[:, :, 2])
    min_hue = np.min(low_third[:, :, 0])
    min_saturation = np.min(low_third[:, :, 1])
    min_value = np.min(low_third[:, :, 2])

    return min_hue,min_saturation,min_value, max_hue, max_saturation, max_value





def get_max_hsv_values_sky_tilt(frame, tilt_degrees,frame_part,pitch):
    # Get the frame dimensions
    height, width, _ = frame.shape

    # Define the transformation matrix for the tilt
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), tilt_degrees, 1)

    # Apply the rotation to the frame
    rotated_frame = cv2.warpAffine(frame, rotation_matrix, (width, height))

    if (pitch == None):
    #if (True):
        pitch_height = height
    else:
        # Calculate the height of the part above the pitch
        pitch_height = (1-pitch) * height

    # Calculate the height of the top 1/3 of the tilted frame
    top_third_height = int(frame_part * pitch_height)

    # Extract the top 1/3 of the tilted frame
    top_third = rotated_frame[:top_third_height, :, :]

    # Calculate the maximum H, S, and V values in the top 1/3
    max_hue = np.max(top_third[:, :, 0])
    max_saturation = np.max(top_third[:, :, 1])
    max_value = np.max(top_third[:, :, 2])
    min_hue = np.min(top_third[:, :, 0])
    min_saturation = np.min(top_third[:, :, 1])
    min_value = np.min(top_third[:, :, 2])

    return min_hue,min_saturation,min_value, max_hue, max_saturation, max_value

def get_max_hsv_values_ground_tilt(frame, tilt_degrees,frame_part,pitch):
    # Get the frame dimensions
    height, width, _ = frame.shape

    # Define the transformation matrix for the tilt
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), tilt_degrees, 1)

    # Apply the rotation to the frame
    rotated_frame = cv2.warpAffine(frame, rotation_matrix, (width, height))
    if (pitch == None):
        # if (True):
        pitch_height = height
    else:
        # Calculate the height of the part above the pitch
        pitch_height = (pitch) * height

    # Calculate the height of the top 1/3 of the tilted frame
    low_third_hight = int((1-frame_part) * pitch_height)

    # Extract the top 1/3 of the tilted frame
    low_third = rotated_frame[low_third_hight:, :, :]

    # Calculate the maximum H, S, and V values in the line
    max_hue = np.max(low_third[:, :, 0])
    max_saturation = np.max(low_third[:, :, 1])
    max_value = np.max(low_third[:, :, 2])
    min_hue = np.min(low_third[:, :, 0])
    min_saturation = np.min(low_third[:, :, 1])
    min_value = np.min(low_third[:, :, 2])

    return min_hue,min_saturation,min_value, max_hue, max_saturation, max_value
