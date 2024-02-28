import sensor, image, time, pyb, os

# Initialize the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

# Create a UART object
uart = pyb.UART(3, 115200, timeout_char = 1000)  # Use the correct UART port

# Attempt to mount the SD card
try:
    os.mount(pyb.SDCard(), '/sd')  # Corrected to not call SDCard as a function
    print("SD card mounted successfully.")
except OSError:
    print("SD card mount failed or already mounted.")

# Specify the directory to save images
image_dir = "/sd/microscope_images"

try:
    os.mkdir(image_dir)
    print("Image directory created.")
except OSError as e:
    # If the directory already exists, an OSError is thrown
    if e.args[0] == 17:  # EEXIST
        print("Image directory already exists.")
    else:
        raise

image_count = 0  # Initialize image counter

#if uart.any():
#    print("uart exists")
uart.write("before loopb")
while True:
    print("in loop")
    if uart.any():
        cmd = uart.read(1)  # Read a command from the PC
        print(cmd)
        if cmd == b'C':  # If the command is 'C' for capture
            img = sensor.snapshot()
            # Generate a file name based on the image count
            file_name = "image_{}.jpg".format(image_count)
            file_path = "{}/{}".format(image_dir, file_name)
            img.save(file_path, quality = 90)  # Save the image to the SD card
            image_count += 1  # Increment the image counter

            # Optionally, send back a confirmation or the file name
            uart.write("Saved: {}\n".format(file_path))
    else:
        uart.write("nothing")
