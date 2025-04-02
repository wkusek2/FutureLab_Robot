#!/usr/bin/env python3

import cv2
import struct
import redis
import numpy as np

from src.camera.jetcam.csi_camera import CSICamera

def toRedis(r,a,n):
   """Store given Numpy array 'a' in Redis under key 'n'"""
   h, w = a.shape[:2]
   shape = struct.pack('>II',h,w)
   encoded = shape + a.tobytes()

   # Store encoded data in Redis
   r.set(n, encoded)
   return


def start_capture(display_w, display_h, capture_w, capture_h, capture_fps, flip=2, exposure=0, tnr_strength=1, wb_mode=1, saturation=1.0, auto_exposure=False):

    # Redis connection
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    camera_idx = [0, 1]

    cam0 = CSICamera(
        capture_device=camera_idx[0], 
        width=display_w, 
        height=display_h, 
        capture_width=capture_w, 
        capture_height=capture_h, 
        capture_fps=capture_fps, 
        flip=flip, 
        exposure=exposure,
        tnr_strength=tnr_strength,
        wb_mode=wb_mode,
        saturation=saturation,
        ae_lock=auto_exposure)
    
    cam1 = CSICamera(
        capture_device=camera_idx[1], 
        width=display_w, 
        height=display_h, 
        capture_width=capture_w, 
        capture_height=capture_h, 
        capture_fps=capture_fps, 
        flip=3, 
        exposure=exposure,
        tnr_strength=tnr_strength,
        wb_mode=wb_mode,
        saturation=saturation,
        ae_lock=auto_exposure)

    while True:
        img0 = cam0.read()
        img1 = cam1.read()

        toRedis(r, img0, 'image0')
        toRedis(r, img1, 'image1')