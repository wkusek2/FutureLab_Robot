###################################
# Install necessary dependencies  #
# for futurelab project           #
###################################

sudo apt install python3-pil python3-pil.imagetk
python3 -m pip install -r utils/packages/requirements.txt

# check if cv2 is installed


# opencv2 is not installed with gstreamer
is_gstreamer="$(python3 -c "import cv2;print(cv2.getBuildInformation())" | grep "GStreamer:" | cut -f2 -d":" | tr -d " ")"
is_cuda="$(python3 -c "import cv2;print(cv2.getBuildInformation())" | grep "CUDA:" | cut -f2 -d":" | tr -d " ")"

echo " "
echo "GSTREAMER ENABLED WITH OPENCV: ${is_gstreamer}"
echo "CUDA ENABLED WITH OPENCV: ${is_cuda}"
