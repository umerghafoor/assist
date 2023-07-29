import os
import win32gui
import win32con
import time

def get_active_folder_path():
    hwnd = win32gui.GetForegroundWindow()
    file_path = win32gui.GetWindowText(hwnd)
    print(file_path,",",hwnd)

    if file_path and "File Explorer" in file_path:
        try:
            parts = file_path.split(" - ")
            folder_path = parts[-1]
            if os.path.exists(folder_path):
                return folder_path
        except Exception as e:
            print("Error:", e)
    return None

def track_active_folder():
    prev_folder = None

    while True:
        active_folder = get_active_folder_path()

        if active_folder and active_folder != prev_folder:
            print("Active folder path:", active_folder)
            prev_folder = active_folder

        time.sleep(1)
        print("working")

if __name__ == "__main__":
    track_active_folder()
