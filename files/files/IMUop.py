from time import time, strftime, gmtime, sleep
import smbus2

# Function to initialize the sensors
def init_sensors(bus, MPU6050_ADDR):
    # Initialize MPU6050
    bus.write_byte_data(MPU6050_ADDR, 0x6B, 0x00)  # Wake up MPU6050

def read_raw_data(addr, bus, MPU6050_ADDR):
    """Read 16-bit raw data from the specified address."""
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = (high << 8) | low
    if value > 32767:  # Convert to signed 16-bit
        value -= 65536
    return value

def calibrate_sensor(bus, MPU6050_ADDR, samples=100):
    print("Calibrating... Please keep the sensor still.")
    sleep(2)
    gyro_offset = [0.0, 0.0, 0.0]

    for _ in range(samples):

        # Read gyroscope data
        gyro_offset[0] += read_raw_data(0x43, bus, MPU6050_ADDR)
        gyro_offset[1] += read_raw_data(0x45, bus, MPU6050_ADDR)
        gyro_offset[2] += read_raw_data(0x47, bus, MPU6050_ADDR)

        sleep(0.01)

    # Calculate the average offsets
    gyro_offset = [x / samples for x in gyro_offset]

    print(f"Calibration complete. Gyro Offset: {gyro_offset}")
    return gyro_offset


# Read calibrated data from the MPU6050.
def calculate_angle_change(gyro_offset, dt, MPU6050_ADDR, bus):

    # Read gyroscope data from MPU6050
    gyro_x = read_raw_data(0x43, bus, MPU6050_ADDR) - gyro_offset[0]
    gyro_y = read_raw_data(0x45, bus, MPU6050_ADDR) - gyro_offset[1]
    gyro_z = read_raw_data(0x47, bus, MPU6050_ADDR) - gyro_offset[2]

    # Convert raw gyro values to degrees/sec (sensitivity = 131 LSB/deg/sec for ±250°/sec range)
    gyro_x = gyro_x / 131.0
    gyro_y = gyro_y / 131.0
    gyro_z = gyro_z / 131.0

    # Calculate angle change (degrees)
    delta_angle_x = gyro_x * dt
    delta_angle_y = gyro_y * dt
    delta_angle_z = gyro_z * dt

    return (delta_angle_x, delta_angle_y, delta_angle_z)


# Read temperature and pressure from the BMP280.
def read_bmp280(bus, BMP280_ADDR):
    # Read temperature registers
    temp_msb = bus.read_byte_data(BMP280_ADDR, 0xFA)
    temp_lsb = bus.read_byte_data(BMP280_ADDR, 0xFB)
    temp_xlsb = bus.read_byte_data(BMP280_ADDR, 0xFC)
    raw_temp = (temp_msb << 12) | (temp_lsb << 4) | (temp_xlsb >> 4)

    # Read pressure registers
    press_msb = bus.read_byte_data(BMP280_ADDR, 0xF7)
    press_lsb = bus.read_byte_data(BMP280_ADDR, 0xF8)
    press_xlsb = bus.read_byte_data(BMP280_ADDR, 0xF9)
    raw_press = (press_msb << 12) | (press_lsb << 4) | (press_xlsb >> 4)

    # Convert raw temperature and pressure to meaningful values (adjust conversion based on BMP280 configuration)
    temperature = raw_temp / 100.0  # Example conversion, adjust according to BMP280 settings
    pressure = raw_press / 256.0    # Example conversion

    return temperature, pressure




def init_IMU():

    # Use I2C Bus 0
    i2c_bus_number = 0  # Use I2C Bus 0

    # Initialize I2C bus
    bus = smbus2.SMBus(i2c_bus_number)

    # MPU6050 and BMP280 addresses
    MPU6050_ADDR = 0x68  # Typically 0x68 or 0x69 depending on the AD0 pin
    BMP280_ADDR = 0x76   # Typically 0x76 or 0x77

    # calibrate data for IMU 
    gyro_offset = calibrate_sensor(bus, MPU6050_ADDR, 100)
    angles = [0.0, 0.0, 0.0]  # [x, y, z]

    # Initialize sensors
    init_sensors(bus, MPU6050_ADDR)

    return gyro_offset, angles, bus, MPU6050_ADDR, BMP280_ADDR


def get_data_from_IMU(gyro_offset, angles, bus, MPU6050_ADDR, BMP280_ADDR):

    global previous_time  # Declare previous_time as global

    # Time calculations
    current_time = time()
    dt = current_time - previous_time  # Time difference in seconds
    previous_time = current_time

    # Read BMP280 data
    temperature, pressure = read_bmp280(bus, BMP280_ADDR)

    # Read IMU and calc angle
    delta_angle = calculate_angle_change(gyro_offset, dt, MPU6050_ADDR, bus)

    # Update total angles
    angles[0] += delta_angle[0]
    angles[1] += delta_angle[1]
    angles[2] += delta_angle[2]

    return angles, temperature, pressure


previous_time = time() # gmtime(time())
