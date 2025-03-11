import sys
import subprocess
import cv2
from math import radians
import numpy as np
sys.path.insert(1, '/home/rocketryclub/EEproject/files')
from crop_and_scale import get_cropping_and_scaling_parameters, crop_and_scale
from image_process import HorizonDetector
#from calculate_angle import calculate_rocket_orientation
from plain_finder import fit_plane_from_lines
from draw_display import draw_horizon




######### tweak to make VideoCapture work

def __gstreamer_pipeline(
        camera_id=0,
        capture_width=1920,
        capture_height=1080,
        display_width=1920,
        display_height=1080,
        framerate=30,
        flip_method=0,
):
    return (
        f"nvarguscamerasrc sensor-id={camera_id} ! "
        f"video/x-raw(memory:NVMM), width=(int){capture_width}, height=(int){capture_height}, "
        f"format=(string)NV12, framerate=(fraction){framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! "
        f"videoconvert ! video/x-raw, format=(string)BGR ! appsink"
    )

######### System commands to kill and restart nvargus-daemon (camera proccesses) #########

def restart_nvargus_daemon():
    try:
        # Kill processes using /dev/video* (this shows active processes)
        subprocess.run(['sudo', 'fuser', '-v', '/dev/video0'], check=True)

        # Kill nvargus-daemon
        subprocess.run(['sudo', 'killall', 'nvargus-daemon'], check=True)

        # Restart nvargus-daemon
        subprocess.run(['sudo', 'systemctl', 'restart', 'nvargus-daemon'], check=True)

        print("Successfully restarted nvargus-daemon.")

    except subprocess.CalledProcessError as e:
        print(f"Error restarting nvargus-daemon: {e}")

#########


def init_cam():

    # Restart nvargus-daemon before starting the camera capture
    restart_nvargus_daemon()

    # Initialize camera capture for the combined feed (index 0)
    cap = cv2.VideoCapture(__gstreamer_pipeline(camera_id=0, flip_method=2), cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Define variables related to cropping and scaling
    INFERENCE_RESOLUTION = (100, 100)
    EXCLUSION_THRESH = 5  # degrees of pitch above and below the horizon
    FOV = 48.8
    ACCEPTABLE_VARIANCE = 1.3


    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from camera.")
        cap.release()
        #cv2.destroyAllWindows()
        sys.exit("Exiting the program")


    # Assuming the combined feed is 1920x1080, each camera feed is 960x540
    height, width = frame.shape[:2]
    cam_width = width // 2
    cam_height = height // 2

    cam_params = [cam_width, cam_height, INFERENCE_RESOLUTION, EXCLUSION_THRESH, FOV, ACCEPTABLE_VARIANCE]

    return cap, cam_params



def find_angle_from_cameras(cap, cam_params, DISPLAY_CAM):
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from camera.")
        exit()

    cam_width, cam_height, INFERENCE_RESOLUTION, EXCLUSION_THRESH, FOV, ACCEPTABLE_VARIANCE = cam_params

    # Split the frame into 4 regions corresponding to the 4 cameras
    camera_1 = frame[0:cam_height, 0:cam_width]      # Top-left
    camera_2 = frame[0:cam_height, cam_width:]       # Top-right
    camera_3 = frame[cam_height:, 0:cam_width]       # Bottom-left
    camera_4 = frame[cam_height:, cam_width:]        # Bottom-right

    cameras = [camera_1, camera_2, camera_3, camera_4]
    lines = []
    result = []
    plain = []
    pitch_data = []  # To store pitch and yaw data for each camera
    yaw_data = []  # To store pitch and yaw data for each camera

    for i, cam_frame in enumerate(cameras):
        RESOLUTION = cam_frame.shape[1::-1]  # extract the resolution from the frame
        CROP_AND_SCALE_PARAM = get_cropping_and_scaling_parameters(RESOLUTION, INFERENCE_RESOLUTION)

    # Scale the captured frame down
        cam_frame_small = crop_and_scale(cam_frame, **CROP_AND_SCALE_PARAM)
        horizon_detector = HorizonDetector(EXCLUSION_THRESH, FOV, ACCEPTABLE_VARIANCE, INFERENCE_RESOLUTION)

        # Process frame to find the horizon
        output = horizon_detector.find_horizon(cam_frame_small, cam_frame, diagnostic_mode=True)
        yaw, pitch, variance, is_good_horizon, mask = output


        if DISPLAY_CAM:
            # Draw the horizon and center circle
            color = (255, 0, 0)
            draw_horizon(cam_frame, yaw, pitch, FOV, color, True)
            center = (cam_frame.shape[1] // 2, cam_frame.shape[0] // 2)
            radius = cam_frame.shape[0] // 100
            cv2.circle(cam_frame, center, radius, (255, 0, 0), 2)
            # Display each camera's output in a separate window
            cv2.imshow(f"Camera {i+1} - Frame", cam_frame)
            #cv2.imshow(f"Camera {i+1} - Mask", mask)
	

       # print("camera num: ", i, " pitch: ", pitch, " yaw: ", yaw)
        # Append pitch and yaw (roll) data to the list
        pitch_data.append(pitch)  # Pitch data
        yaw_data.append(yaw)   # Yaw data (roll represents horizontal angle)


#   print("pitch: ", pitch, "yaw: ", yaw)

#   print(pitch_yaw_data)

# find the horizion plain and norma
    


    # Loop to populate lines, skipping or handling None values
    for i in range(4):  # 4 cameras
        if pitch_data[i] is None or yaw_data[i] is None or pitch_data[i] is 0 or yaw_data[i] is 0:
            continue  # Skip this line if data is None

        # Construct the line
        line = (
            (1 if i % 2 == 0 else -1 if i == 2 else 0,  # x component
             0 if i % 2 == 0 else -1 if i == 3 else 1,  # y component
             pitch_data[i]),                            # z component
            (np.cos(radians(yaw_data[i])) if i % 2 != 0 else 0,  # cos(yaw) or 0
             0 if i % 2 == 0 else np.cos(radians(yaw_data[i])),  # 0 or cos(yaw)
             np.sin(radians(yaw_data[i])) if i != 2 else np.sin(-radians(yaw_data[i])))  # sin(yaw) or -sin(yaw)
        )
        lines.append(line)

    # Pass the valid lines to the function
    if lines:
        plain = fit_plane_from_lines(lines)
   # else:
     #   result = None
    

    """
    lines = [
        ((1, 0, pitch_data[0]), (0,np.cos(yaw_data[0]),np.sin(yaw_data[0]))),  # Line 0
        ((0, 1, pitch_data[1]), (np.cos(yaw_data[1]),0,np.sin(yaw_data[1]))),  # Line 1
        ((-1, 0, pitch_data[2]), (0,np.cos(yaw_data[2]),np.sin(-yaw_data[2]))),  # Line 2
        ((0 ,-1, pitch_data[3]), (np.cos(yaw_data[3]),0,np.sin(-yaw_data[3])))   # Line 3
    ]
    result = fit_plane_from_lines(lines)
    """
#    result = calculate_rocket_orientation(pitch_yaw_data[0],pitch_yaw_data[1], pitch_yaw_data[4],pitch_yaw_data[5], pitch_yaw_data[2],pitch_yaw_data[3], pitch_yaw_data[6],pitch_yaw_data[7])


    return plain, pitch_data, yaw_data, cap

