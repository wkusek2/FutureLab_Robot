from .camera import Camera
import atexit
import cv2
import traitlets


class CSICamera(Camera):
    capture_device = traitlets.Integer(default_value=0)
    capture_fps = traitlets.Integer(default_value=14)
    capture_width = traitlets.Integer(default_value=768)
    capture_height = traitlets.Integer(default_value=432)
    flip = traitlets.Integer(default_value=0)
    exposure = traitlets.Float(default_value=0.0)
    exposure_time_min = 50000
    exposure_time_max = 30000000
    gainrange = "1 1"
    tnr_strength = traitlets.Integer(default_value=1)
    wb_mode = traitlets.Integer(default_value=5)
    saturation = traitlets.Float(default_value=1.0)
    ae_lock=False


    def __init__(self, *args, **kwargs):
        super(CSICamera, self).__init__(*args, **kwargs)
        try:
            self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)

            re, image = self.cap.read()

            if not re:
                raise RuntimeError('Could not read image from camera.')
        except:
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.cap.release)

    def _gst_str(self):

        exposure_time_range = f"{self.exposure_time_min} {self.exposure_time_max}"

        return (
            'nvarguscamerasrc sensor-id=%d exposuretimerange=\"%s\" gainrange=\"%s\" tnr-strength=%d wbmode=%d exposurecompensation=%d saturation=%f aelock=%s ! ' \
            'video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! ' \
            'nvvidconv flip-method=%d  ! ' \
            'video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx !' \
            'videoconvert ! ' \
            'appsink' 
        % (
            self.capture_device, 
            exposure_time_range,
            self.gainrange,
            self.tnr_strength,
            self.wb_mode,
            self.exposure, 
            self.saturation,
            "true" if self.ae_lock else "false",
            self.capture_width, 
            self.capture_height,
            self.capture_fps, 
            self.flip, 
            self.width, 
            self.height)
        )

    def _read(self):
        re, image = self.cap.read()
        if re:
            return image
        else:
            raise RuntimeError('Could not read image from camera')
