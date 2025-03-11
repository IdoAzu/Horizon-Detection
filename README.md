Horizon-Based Rocket Orientation System
This project implements a multi-camera horizon detection and optical flow system for real-time rocket orientation estimation. Designed for the HUJI Rocketry Club’s RAM-II project, the system utilizes four synchronized cameras to estimate pitch, yaw, and roll by combining horizon detection and optical flow algorithms. Unlike traditional IMU-based approaches, this method mitigates drift bias and enhances measurement accuracy in dynamic flight conditions.

The hardware setup includes an NVIDIA Jetson Nano paired with ArduCam IMX519 cameras, capturing a 360° field of view for robust horizon detection.

However, initial tests revealed performance limitations, achieving only 40 FPS instead of the targeted 400 Hz data rate, highlighting the need for further optimization. Future developments will focus on improving processing speed and enhancing real-time capabilities for high-speed rocket flights.

📌 Key Features:
✅ Multi-camera horizon detection (closed-loop 3D horizon estimation)\n
✅ Optical flow for roll estimation (unlike horizon-only methods)
✅ Drift-free alternative to IMU-based systems
✅ Hardware setup optimized for real-time rocket flight
✅ High-precision testing and validation

🚀 Next Steps:
🔹 Optimize processing pipeline to achieve real-time performance
🔹 Improve robustness under challenging lighting conditions
🔹 Expand system integration with onboard flight computers
