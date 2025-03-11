import sys
#import cv2
import numpy as np
import csv
sys.path.insert(1, '/home/rocketryclub/EEproject/files')
#from time import time, strftime, gmtime
from timeit import default_timer as timer
from IMUop import get_data_from_IMU, init_IMU, time, gmtime, strftime
from CAMop import init_cam, find_angle_from_cameras, cv2


DISPLAY_CAM = True

if __name__ == "__main__":


    # Open a CSV file to log the data
    csv_file = 'camera_log.csv'
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the headers for each camera
        writer.writerow([
            'Timestamp',
	    'X_angle', 'y_angle', 'z_angle',
            'Camera 1 Pitch', 'Camera 2 Pitch',
            'Camera 3 Pitch', 'Camera 4 Pitch',
            'Camera 1 Yaw', 'Camera 2 Yaw',
            'Camera 3 Yaw', 'Camera 4 Yaw',
            'gyro_x', 'gyro_y', 'gyro_z', 'temperature', 'pressure'
        ])

    print('Starting perf test...')
    t1 = timer()


    gyro_offset, angles, bus, MPU6050_ADDR, BMP280_ADDR = init_IMU()
    cap, cam_params = init_cam()


    try:
        while True:

	    ######################## IMU ########################

            angles, temperature, pressure = get_data_from_IMU(gyro_offset, angles, bus, MPU6050_ADDR, BMP280_ADDR)

	    ######################## CAM ########################
            #read from camera a quad frame input
            # ret, frame = cap.read()
            # if not ret:
            #      print("Error: Could not read frame from camera.")
            #      break

#            cap = find_angle_from_cameras(cap, cam_params, DISPLAY_CAM)
            plain, pitch_data, yaw_data, cap = find_angle_from_cameras(cap, cam_params, DISPLAY_CAM)

	    ######################## SAVE DATA ########################
            # Log the data to the CSV file
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime(time()))
#                writer.writerow([timestamp] + [angles[0], angles[1], angles[2], temperature, pressure])
                writer.writerow([timestamp] + plain + pitch_data + yaw_data + [angles[0], angles[1], angles[2], temperature, pressure])

            # Break the loop when the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Process interrupted by user.")

    finally:
        # Ensure the camera is released and all windows are closed
        cap.release()
        cv2.destroyAllWindows()
        print(f"Cleaned up and closed all windows. Data saved to {csv_file}.")


