import cv2
import numpy as np

def get_cropping_and_scaling_parameters(original_resolution: tuple, new_resolution: tuple) -> dict:
    """
    Calculate parameters for cropping and scaling an image to a new resolution.

    Args:
        original_resolution (tuple): The original resolution of the frame as (width, height).
        new_resolution (tuple): The target resolution for scaling, generally much smaller than the original resolution.

    Returns:
        dict: A dictionary containing the cropping start, cropping end, and scale factor.
    """
    # Calculate aspect ratios of the original and target resolutions
    new_aspect_ratio = new_resolution[0] / new_resolution[1]
    original_aspect_ratio = original_resolution[0] / original_resolution[1]

    # Check if the target aspect ratio is feasible with the original image
    if new_aspect_ratio > original_aspect_ratio:
        print(f"Requested aspect ratio of {new_aspect_ratio} is wider than original aspect ratio of {original_aspect_ratio}. "\
              "This is not allowed.")
        new_aspect_ratio = original_aspect_ratio  # Adjust to the original aspect ratio
        print(f'Aspect ratio of {new_aspect_ratio} will be used instead.')

    # Define variables for cropping based on aspect ratio adjustments
    height = original_resolution[1]
    width = original_resolution[0]
    new_width = height * new_aspect_ratio
    margin = (width - new_width) // 2
    cropping_start = int(margin)
    cropping_end = int(width - margin)

    # Define scaling factor based on the target resolution height
    scale_factor = new_resolution[1] / original_resolution[1]

    # Package parameters into a dictionary
    crop_and_scale_parameters = {
        'cropping_start': cropping_start,
        'cropping_end': cropping_end,
        'scale_factor': scale_factor
    }

    return crop_and_scale_parameters

def crop_and_scale(frame, cropping_start, cropping_end, scale_factor):
    """
    Crop and scale an image frame based on provided parameters.

    Args:
        frame (numpy.ndarray): The input image frame.
        cropping_start (int): Starting x-coordinate for cropping.
        cropping_end (int): Ending x-coordinate for cropping.
        scale_factor (float): Factor by which to scale the frame.

    Returns:
        numpy.ndarray: The cropped and scaled frame.
    """
    # Crop the image horizontally
    frame = frame[:, cropping_start:cropping_end]
    # Resize (scale) the image
    frame = cv2.resize(frame, (0, 0), fx=scale_factor, fy=scale_factor)
    return frame

if __name__ == "__main__":
    # Load an example image
    path = 'training_data/sample_images/image2.png'
    input_frame = cv2.imread(path)
    input_frame_resolution = input_frame.shape[1::-1]  # Get (width, height) of the input frame
    print(input_frame_resolution)

    # Define the desired resolution
    desired_resolution = (100, 100)

    # Calculate cropping and scaling parameters
    crop_and_scale_parameters = get_cropping_and_scaling_parameters(input_frame_resolution, desired_resolution)

    # Apply cropping and scaling
    output_frame = crop_and_scale(input_frame, **crop_and_scale_parameters)

    # Display the input and output frames
    cv2.imshow("input_frame", input_frame)
    cv2.imshow("output_frame", output_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

