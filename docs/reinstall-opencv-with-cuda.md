# Update OpenCV ze wsparciem CUDA oraz GSTREAMER

Skrypt jest zmodyfikowaną wersją z innego [repo](https://github.com/mdegans/nano_build_opencv).

Update zajmuje ~3h, kawa do umilenia czasu obowiązkowa ☕

W pliku `installer.sh` należy zmienić
  - `-D CUDNN_VERSION='8.9'`

Uruchamiamy skrypt z poziomu Orina w folderze `podwodny`. Możliwa jest zmiana zainstalowanej wersji OpenCV.

Poprawione zostały wersje instalowanych bilbiotek oraz nowsza wersja CUDNN do OpenCV.

```bash
export OPENCV_VERSION=4.8.0 # opcjonalnie, jeżeli konieczna konkretna wersja
sudo jetson-utilities/installer.sh $OPENCV_VERSION
```

Jeżeli wystąpią problemy, należy kierować się outputem z errorów i spróbować to naprawić, w razie czego służę pomocą. :)

### Częste problemy podczas instalacji

- `Ambiguous overload for 'operator!='` - `CUDA: 12.2`

```bash
/home/di0n/Desktop/opencv-4.8.0/modules/dnn/src/layers/../cuda4dnn/primitives/normalize_bbox.hpp:114:24: error: ambiguous overload for ‘operator!=’ (operand types are ‘__half’ and ‘double’)
  114 |             if (weight != 1.0)
      |                 ~~~~~~~^~~~~~
(...)
gmake[2]: *** [modules/dnn/CMakeFiles/opencv_dnn.dir/build.make:1148: modules/dnn/CMakeFiles/opencv_dnn.dir/src/layers/normalize_bbox_layer.cpp.o] Error 1
gmake[1]: *** [CMakeFiles/Makefile2:5170: modules/dnn/CMakeFiles/opencv_dnn.dir/all] Error 2
gmake: *** [Makefile:166: all] Error 2
```

Problem występuje przez złą wersję CUDA, w której został znaleziony bug. Konieczne jest podbicie wersji CUDA albo pobranie niższej.
W tym celu kroki zmiany wersji CUDA zostały opisane [tutaj](./change-cuda-version.md)
