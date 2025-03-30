import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os

adb_path = r"C:\Users\berkx\Downloads\platform-tools-latest-windows\platform-tools\adb.exe"

def get_connected_devices():
    try:
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        output = result.stdout.strip().split('\n')[1:]
        devices = [line.split()[0] for line in output if line.strip()]
        return devices
    except Exception as e:
        messagebox.showerror("Error", f"Error getting devices: {e}")
        return []

def update_device_list():
    devices = get_connected_devices()
    device_dropdown['values'] = devices
    if devices:
        device_dropdown.set(devices[0])
    else:
        device_dropdown.set("No devices connected")

def install_apk():
    device = device_dropdown.get()
    if device == "No devices connected":
        messagebox.showerror("Error", "No device selected or connected.")
        return
    
    apk_path = filedialog.askopenfilename(title="Select APK", filetypes=[("APK files", "*.apk")])
    if not apk_path:
        return
    
    try:
        subprocess.run([adb_path, "-s", device, "install", apk_path], check=True)
        messagebox.showinfo("Success", f"APK installed successfully on {device}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error installing APK: {e}")

def take_screenshot():
    device = device_dropdown.get()
    if device == "No devices connected":
        messagebox.showerror("Error", "No device selected or connected.")
        return
    
    try:
        subprocess.run([adb_path, "-s", device, "shell", "screencap", "-p", "/sdcard/screen.png"], check=True)
        screenshot_path = os.path.join(os.getcwd(), "screen.png")
        subprocess.run([adb_path, "-s", device, "pull", "/sdcard/screen.png", screenshot_path], check=True)
        messagebox.showinfo("Success", f"Screenshot saved as {screenshot_path}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error taking screenshot: {e}")

def execute_command():
    device = device_dropdown.get()
    if device == "No devices connected":
        messagebox.showerror("Error", "No device selected or connected.")
        return
    
    command = command_entry.get()
    if not command:
        messagebox.showerror("Error", "Please enter a command.")
        return
    
    try:
        result = subprocess.run([adb_path, "-s", device, "shell", command], capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Success", f"Command executed successfully:\n{result.stdout}")
        else:
            messagebox.showerror("Error", f"Error executing command:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error executing command: {e}")

root = tk.Tk()
root.title("Droid one by grant.xyz")

device_label = tk.Label(root, text="Select Device:")
device_label.pack(pady=5)

device_dropdown = ttk.Combobox(root)
device_dropdown.pack(pady=5)

refresh_button = tk.Button(root, text="Refresh Devices", command=update_device_list)
refresh_button.pack(pady=5)

install_button = tk.Button(root, text="Install APK", command=install_apk)
install_button.pack(pady=10)

screenshot_button = tk.Button(root, text="Take Screenshot", command=take_screenshot)
screenshot_button.pack(pady=10)

command_label = tk.Label(root, text="Enter ADB Command:")
command_label.pack(pady=5)

command_entry = tk.Entry(root, width=30)
command_entry.pack(pady=5)

execute_button = tk.Button(root, text="Execute Command", command=execute_command)
execute_button.pack(pady=10)

root.geometry("350x350")
root.mainloop()
