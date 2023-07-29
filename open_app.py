import subprocess
import pygetwindow as gw
import win32gui
import win32gui
import win32con

def get_active():
    active_window = win32gui.GetForegroundWindow()
    
    if active_window:
        window_title = win32gui.GetWindowText(active_window)
        print("Title of the window: ", window_title)
        
        # Get the class name of the active window
        class_name = win32gui.GetClassName(active_window)
        print("Class name of the window: ", class_name)
        
        # Check if the window class name indicates a folder window (assuming it contains the word "CabinetWClass")
        if "CabinetWClass" in class_name:
            # Get the folder path associated with the window
            folder_path = win32gui.SendMessage(active_window, win32con.WM_COPYDATA, 0, "00000000CloverGet")
            print("Folder path of the window: ", folder_path)
            return folder_path
        else:
            print("The active window is not a folder window.")
    
    return None

def run_commands_in_cmd(selected_path, commands):
    print(selected_path)
    try:
        # Open CMD in the selected path and wait for it to finish
        subprocess.Popen('cmd', cwd=selected_path, creationflags=0)

        # Run the specified commands
        for command in commands:
            subprocess.run(command, cwd=selected_path, shell=True)
            print("code ran")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    selected_path = r'D:\GitHub\Qt-Stylesheet-Library'
    active_window_title = get_active()
    print("Active Window Title (Windows):", active_window_title)

    #run_commands_in_cmd(selected_path, ['code .',])
