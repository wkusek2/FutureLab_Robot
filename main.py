import os
import time
import threading

from src.app.gui import App
from src.camera.camera_read import start_capture


###################################################################

DO_CHANGE_ENV = True
ENV_DISPLAY_CAMERA = ":0"
ENV_DISPLAY_APP = ":1"

ENV_DISTANCE_BETWEEN_CAMERAS = 60 # [cm]

#########################
# Camera modes for IMX708
# [WIDTH, HEIGHT, FPS]
CAMERA_MODES = [
    [4608, 2592, 14],  # Pełna rozdzielczość, około 14 FPS
    [2304, 1296, 30],  # Połowa rozdzielczości, wyższa ilość klatek
    [1920, 1080, 40]
]

# Variables for camera
ENV_CAMERA = {
    "MODE": 0, 
    "DISPLAY_W": 768,
    "DISPLAY_H": 432,
    "FLIP": 1, # 0 or 1 or2
    "EXPOSURE": 1, # <-2; 2>
    "TNR_STRENGTH" : 1,
    "WB_MODE": 5, # wyłączenie automatycznego balansu bieli
    "SATURATION": 1.0,
    "AUTO_EXPOSURE": True # Domyślnie brak blokadu autoekspozycji
}

###################################################################


def start_camera():
    if DO_CHANGE_ENV:
        os.environ["DISPLAY"] = ENV_DISPLAY_CAMERA
        print("[ ] Variable DISPLAY on camera process is", os.environ["DISPLAY"])
        print("[+] Started camera capture process. Saving frames to redis database")

    start_capture(
        display_w =     ENV_CAMERA["DISPLAY_W"], 
        display_h =     ENV_CAMERA["DISPLAY_H"], 
        capture_w =     CAMERA_MODES[ENV_CAMERA["MODE"]][0], 
        capture_h =     CAMERA_MODES[ENV_CAMERA["MODE"]][1], 
        capture_fps =   CAMERA_MODES[ENV_CAMERA["MODE"]][2], 
        flip =          ENV_CAMERA["FLIP"],
        exposure =      ENV_CAMERA["EXPOSURE"],
        tnr_strength =  ENV_CAMERA["TNR_STRENGTH"],
        wb_mode =       ENV_CAMERA["WB_MODE"],
        auto_exposure = ENV_CAMERA["AUTO_EXPOSURE"])


def start_app():
    if DO_CHANGE_ENV:
        os.environ["DISPLAY"] = ENV_DISPLAY_APP
        print("[ ] Variable DISPLAY on app process is", os.environ["DISPLAY"])
        print("[+] Started GUI app.")
    
    app = App(
        ENV_DISTANCE_BETWEEN_CAMERAS, 
        CAMERA_MODES[ENV_CAMERA["MODE"]][0], 
        CAMERA_MODES[ENV_CAMERA["MODE"]][1])
    
    app.run()



if __name__ =="__main__":

    # start camera capture thread
    thread_camera = threading.Thread(target=start_camera, daemon=True, args=())
    thread_camera.start()

    # wait for camera thread to start
    time.sleep(1)

    # start GUI application
    start_app()
    

    #gst-launch-1.0 nvarguscamerasrc sensor-id=0 ! 'video/x-raw(memory:NVMM), width=4608, height=2592, format=(string)NV12, framerate=(fraction)14/1' ! nvvidconv flip-method=0 ! 'video/x-raw, width=768, height=432, format=(string)BGRx' ! videoconvert ! xvimagesink