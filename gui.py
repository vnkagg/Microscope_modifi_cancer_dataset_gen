from cgitb import text
import tkinter as tk
from tkinter import colorchooser, messagebox
import serial

ser = serial.Serial('/dev/tty.usbmodem11401', 115200, timeout=1)

def handle_const_col():
    colour_code = colour_value.get()
    ser.write(b'W')
    ser.write((colour_code + '\n').encode())

def blink_RGB():
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
    # brightness_value = brightness_scale.get()
    # ser.write(('L' + str(value) + '\n').encode())
    ser.write(b'L')
    ser.write((str(value) + '\n').encode())
    print("Brightness:", value)

def capture_image():
    pass

app = tk.Tk()
app.title("Microscope Controls")

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
