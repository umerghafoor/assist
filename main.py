from pynput import keyboard
from window import MyWindow
from PyQt6.QtWidgets import QApplication
import sys
import threading


def runApp():
    app = QApplication(sys.argv)
    window = MyWindow()
    print("One is running")
    window.load_buttons()
    window.show_window()
    app.exec()


def on_press(key):
    try:
        print('Key {} pressed.'.format(key.char))
        try:
            if key.char == "/":
                print('"/" key is pressed.')

                runApp()

        except AttributeError:
            pass
    except AttributeError:
        print('Special key {} pressed.'.format(key))


def on_release(key):
    if key == keyboard.Key.esc:
        return False


print("App start working")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
