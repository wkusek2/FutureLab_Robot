import cv2
import numpy as np
from PIL import Image, ImageTk

import struct
import redis

from src.camera.utils import Utils

# [WIDTH, HEIGHT, FPS]
CAMERA_MODES = [
    [1536, 864, 10],
    [1536, 864, 90],
    [1920, 1090, 30],
    [1640, 1232, 30],
    [1280, 720, 60],
    [1280, 720, 120]
]

def fromRedis(r,n):
   """Retrieve Numpy array from Redis key 'n'"""
   encoded = r.get(n)
   h, w = struct.unpack('>II',encoded[:8])
   a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
   return a

def convert_rg10_to_rgb(image):
    # Zakładam, że obraz RG10 jest zapisany w 16-bitowej tablicy (np. uint16)
    # RG10 oznacza: 10-bitowy R, 10-bitowy G, 10-bitowy B w 16-bitowym kontenerze
    
    # Przeskalowanie wartości z 10-bitowego zakresu (0-1023) do 8-bitowego (0-255)
    image = (image >> 2).astype(np.uint8)  # 10-bitowe wartości przesunięte do 8-bitowego zakresu
    
    # OpenCV działa w BGR, więc konwertujemy do RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BAYER_RG2RGB)
    
    return Image.fromarray(image_rgb)

class Camera:
    def __init__(self, width, height):
        # system arguments default values
        self.cam_disp = 1 # cam_disp
        self.contour = 0 # return contour (canny, threshold) image
        self.detect = 1 # show detected all squares
        self.info = 0 # info about width, height of detected square, distance

        # display window size
        self.display_w = width
        self.display_h = height

        # OBJECT TO DETECT # DEPRECATED
        self.OBJECT_W = 10 #object_w  # [cm]
        self.OBJECT_L = 10 #object_l  # [cm]

        # FRAME FOR BOTH CAMERAS
        self.image0 = None
        self.image0_contour = None
        self.detected_object0 = [0, 0, 0, 0, 0, 0]
        
        self.image1 = None
        self.image1_contour = None
        self.detected_object1 = [0, 0, 0, 0, 0, 0]

        self.distance = 0
        self.center_scale = 3 # [%] how big or small should center of screen be to set camera

        # UTILS
        self.utils = Utils()
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def change_param(self, id, param):
        id = int(id)
        param = int(param)

        if id == 1:
            self.utils.threshold1 = param
        elif id == 2:
            self.utils.threshold2 = param
        elif id == 3:
            self.utils.epsilon = param
        elif id == 4:
            self.utils.max_area = param
        elif id == 5:
            self.utils.min_area = param
        elif id == 6:
            self.utils.brightness_v = param
        elif id == 7:
            self.utils.contrast_v = param
        else:
            pass

    def processing(self, frame):
        # 1
        # image operations to get black and white contours
        frame = self.utils.masking(frame, self.utils.lower_color, self.utils.upper_color)
        frame, image_contour = self.utils.get_contours(frame, 
                                                       [self.utils.threshold1, self.utils.threshold2],
                                                       self.utils.contrast_v, 
                                                       self.utils.brightness_v,
                                                       draw=self.contour)

        # 2
        # detecting squares from image and returning it with square contours
        # finals_contours = [index, x, y, w, h [straight rectangle around object], box corner points [box],
        # width [cm], height [cm], color]
        frame, final_contours = self.utils.detect_square(image_contour, 
                                                         frame, 
                                                         self.utils.min_area, 
                                                         self.utils.max_area, 
                                                         self.OBJECT_W, self.OBJECT_L)

        # 3
        # display detected rectangles and
        # display info about length, width and color
        self.utils.display_info(frame, 
                                final_contours, 
                                self.distance,
                                draw_detect=self.detect, 
                                draw_info=self.info)

        image_contour = cv2.resize(image_contour, (int(self.display_w / 2), int(self.display_h / 2)))

        # 4
        # todo returning picked image coordinates and color
        detected_object = self.utils.pick_object(frame, final_contours, self.distance)

        return frame, image_contour, detected_object


    def start(self):
        frame_camera0 = fromRedis(self.redis, 'image0')
        frame_camera1 = fromRedis(self.redis, 'image1')

        self.image0, self.image0_contour, self.detected_object0 = self.processing(frame_camera0)
        self.image1, self.image1_contour, self.detected_object1 = self.processing(frame_camera1)


    def object_in_center(self, object_id, frame_size):
        center_width_ratio = 1 / self.center_scale  # Proportion of the width
        center_height_ratio = 1 / self.center_scale  # Proportion of the height
        
        detected = self.get_object_info(object_id)

        # detected[0] is top-left point in rectangle, we calculate according to center of it
        pos_x = detected[0] + (detected[3] // 2)
        center_x_start = frame_size[0] * (0.5 - center_width_ratio / 2)
        center_x_end = frame_size[0] * (0.5 + center_width_ratio / 2)

        # only assuming X axis, so pos_y not relevant
        pos_y = detected[1]
        center_y_start = frame_size[1] * (0.5 - center_height_ratio / 2)
        center_y_end = frame_size[1] * (0.5 + center_height_ratio / 2) 

        return center_x_start <= pos_x <= center_x_end
    
        # check also for y pos
        # return center_x_start <= pos_x <= center_x_end and center_y_start <= pos_y <= center_y_end

    def object_is_detected(self, object_id):
        detected = self.get_object_info(object_id)

        if detected == [0, 0, 0, 0, 0, [0]]:
            return False
        
        return True
    
    def get_image(self):
        img0 = Image.fromarray(cv2.cvtColor(self.image0, cv2.COLOR_BGR2RGB))
        img1 = Image.fromarray(cv2.cvtColor(self.image1, cv2.COLOR_BGR2RGB))
        return img0, img1

    def get_contour(self):
        img0_cnt = Image.fromarray(cv2.cvtColor(self.image0_contour, cv2.COLOR_BGR2RGB))
        img1_cnt = Image.fromarray(cv2.cvtColor(self.image1_contour, cv2.COLOR_BGR2RGB))
        return img0_cnt, img1_cnt
    
    def get_object_info(self, idx: int):
        if idx == 0:
            return self.detected_object0
        elif idx == 1:
            return self.detected_object1
        else:
            return "Invalid index for detected object. (Possible values: 0 or 1)"
    
    def get_param(self):
        return [self.utils.threshold1, self.utils.threshold2, 
                self.utils.max_area, self.utils.min_area, 
                self.utils.brightness_v, self.utils.contrast_v]

    ##########################    
    # DEPRECATED
    
    # def get_info(self):
    #     info = [bool(self.cam_disp),
    #             self.WIDTH, self.HEIGHT, self.FPS,
    #             bool(self.contour),
    #             bool(self.detect),
    #             bool(self.info),
    #             self.current_img]
    #     return info

    # def __str__(self):
    #     return (
    #         f"========================\n"
    #         f"Running image processing program\n"
    #         f"Use camera: {bool(self.cam_disp)}\n"
    #         f"Camera stream resolution:\n"
    #         f"W = {self.WIDTH} | H = {self.HEIGHT} | FPS = {self.FPS}\n"
    #         f"Draw contour: {bool(self.contour)}\n"
    #         f"Draw rectangles: {bool(self.detect)}\n"
    #         f"Display info: {bool(self.info)}\n"
    #         f"Current image: cam{self.current_img}.jpg\n"
    #         f"========================\n")

    # def update_image_param(self, param):
    #     self.utils.threshold1 = param[0]
    #     self.utils.threshold2 = param[1]
    #     self.utils.max_area = param[2]
    #     self.utils.min_area = param[3]
    #     self.utils.brightness_v = param[4]
    #     self.utils.contrast_v = param[5]
    #     self.utils.lower_color = np.array([param[7], param[8], param[9]])
    #     self.utils.upper_color = np.array([param[10], param[11], param[12]])