# import readline
# import struct
# import io
# import time
from cgitb import text
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import serial
import serial.tools.list_ports
from PIL import Image

def list_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

def refresh_ports():
    ports = list_serial_ports()
    serial_combo['values'] = ports
    if ports:
        serial_combo.current(0)
    else:
        messagebox.showwarning("Warning", "No serial ports found.")
    
# def on_serial_selection(event):
#     # Assuming 'serial_var' is your StringVar associated with the Combobox
#     selected_port = serial_var.get()
#     print(f"Selected port: {selected_port}")
#     # Here, you can also open the serial connection or update a global variable

def get_serial_connection():
    selected_port = serial_var.get()
    try:
        return serial.Serial(selected_port, 115200, timeout=1)
    except serial.SerialException as e:
        messagebox.showerror("Serial Connection Error", str(e))
        return None

def handle_const_col():
    ser = get_serial_connection()
    print(ser)
    if ser:
        colour_code = colour_value.get()
        ser.write(b'W')
        ser.write((colour_code + '\n').encode())
        ser.close()

def blink_RGB():
    ser = get_serial_connection()
    if ser:
        interval_value = blink_entry.get()
        try:
            interval = int(interval_value)
            ser.write(b'B')
            ser.write(str(interval).encode())
        except ValueError:
            messagebox.showerror("Error", "Blink interval must be an integer")


def static_colour():
    color_code = colorchooser.askcolor(title ="Choose color")
    color_entry.delete(0, tk.END)
    color_entry.insert(0, color_code[1])

def handle_colour_input(*args):
    colour_code = colour_value.get()
    if not (colour_code[0] == "#"):
        messagebox.showerror("Error", "INVALID COLOUR CODE")
        colour_value.set(colour_code[:-1])
    if(len(colour_code) > 1):
        if not ((colour_code[-1] >= 'A' and colour_code[-1] <= 'F') or (colour_code[-1] <= '9' and colour_code[-1] >= '0') or (colour_code[-1] >= 'a' and colour_code[-1] <= 'f')):
            messagebox.showerror("Error", "Invalid Colour Code")
            colour_value.set(colour_code[:-1])
    print(colour_code)

def handle_brightness(value):
    ser = get_serial_connection()
    if ser:
        # brightness_value = brightness_scale.get()
        # ser.write(('L' + str(value) + '\n').encode())
        ser.write(b'L')
        ser.write((str(value) + '\n').encode())
        print("Brightness:", value)

def capture_image():
    ser = get_serial_connection()
    if ser:
        ser.write(b'C')
        # s = ser.readline().decode('utf-8')
        # print(s)
        # if s.startswith("Saved"):
        #     messagebox.showinfo("Success", "Image captured and saved as captured_image.jpg")
        # elif s.startswith("before"):
        #     messagebox.showinfo("before loop")
        # elif s.startswith("nothing"):
        #     messagebox.showinfo("uart wrote")
        # elif s.startswith("C"):
        #     messagebox.showinfo("C")
        # elif s.startswith("before loop"):
        #     messagebox.showinfo("before loop")

        

            
        # try:
        
            # size_str = serial_camera.readline()  # Read the size as a string
            # img_size = int(size_str)  # Convert the size to an integer
            # img_data = serial_camera.read(img_size)  # Now read the image data
            
            # # Convert the bytes data to an image
            # img = Image.open(io.BytesIO(img_data))
            # img.save("captured_image.jpg")  # Save the image
            
        
        # except Exception as e:
        #     messagebox.showerror("Error", f"An error occurred: {str(e)}")

app = tk.Tk()
app.title("Microscope Controls")

serial_var = tk.StringVar()

serial_frame = tk.Frame(app)
serial_frame.pack(pady=10)

serial_label = tk.Label(serial_frame, text="Select Serial Port:")
serial_label.pack(side=tk.LEFT)

serial_combo = ttk.Combobox(serial_frame, textvariable=serial_var, state="readonly", width=50)
serial_combo.pack(side=tk.LEFT)
# serial_combo.bind('<<ComboboxSelected>>', on_serial_selection)

refresh_button = tk.Button(serial_frame, text="Refresh Ports", command=refresh_ports)
refresh_button.pack(side=tk.LEFT)

colour_value = tk.StringVar()
colour_value.trace("w", handle_colour_input)

# Brightness Control Frame
brightness_frame = tk.Frame(app)
brightness_frame.pack(pady=10)
brightness_label = tk.Label(brightness_frame, text="Brightness:")
brightness_label.pack(side=tk.LEFT)
brightness_scale = tk.Scale(brightness_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=handle_brightness)
brightness_scale.pack(side=tk.LEFT)

# Color Control Frame
color_frame = tk.Frame(app)
color_frame.pack(pady=10)
color_label = tk.Label(color_frame, text="Color (hex):")
color_label.pack(side=tk.LEFT)
color_entry = tk.Entry(color_frame, textvariable=colour_value)
color_entry.pack(side=tk.LEFT)
color_button = tk.Button(color_frame, text="Choose Color", command=static_colour)
color_button.pack(side=tk.LEFT)

# Blink Control Frame
blink_frame = tk.Frame(app)
blink_frame.pack(pady=10)
blink_label = tk.Label(blink_frame, text="Blink Interval (ms):")
blink_label.pack(side=tk.LEFT)
blink_entry = tk.Entry(blink_frame)
blink_entry.pack(side=tk.LEFT)
blink_button = tk.Button(blink_frame, text="Blink RGB", command=blink_RGB)
blink_button.pack(side=tk.LEFT)

# Action Buttons Frame
action_frame = tk.Frame(app)
action_frame.pack(pady=10)
capture_button = tk.Button(action_frame, text="Capture Image", command=capture_image)
capture_button.pack(side=tk.LEFT)
static_button = tk.Button(action_frame, text="Glow Chosen Colour Static", command=handle_const_col)
static_button.pack(side=tk.LEFT)

app.mainloop()