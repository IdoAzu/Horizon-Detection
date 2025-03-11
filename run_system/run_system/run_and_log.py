import subprocess
import sys
sys.path.insert(1, '/home/rocketryclub/EEproject/files')

import merge_log_files
import run



# run both algo and IMU sync 
subprocess.call("run.py", shell=True)

# join log files into last table
subprocess.call("merge_log_files.py", shell=True)
print("yey all good")

#if __name__ == '__main__':
