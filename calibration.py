import cv2
import subprocess
import numpy as np
from main import ProcessingUtils

height=480
width=640
shutter_ms=100
awbgains=(1,1)
output_file = 'tmp.png'

gain_max = 100
gain_min = 10
gain_step = -10

LED_value = 254

for index, gain in enumerate(np.arange(gain_max, gain_min, gain_step)):

    # Picture shot
    cmd_str = f"rpicam-still -o {output_file} --height {height} --width {width} --shutter {shutter_ms * 1000} --gain {gain} --awbgains {','.join([str(val) for val in awbgains])} --immediate --nopreview --vflip"
    cmd_arr = cmd_str.split(" ")
    subprocess.run(cmd_arr, stdout=subprocess.DEVNULL)

    # Picture computation
    img = cv2.imread("tmp.png")
    img = ProcessingUtils.crop_img(img)

    w,h,c = img.shape
    cell_h = h // 8
    cell_w = w //8

    array_camera_res = []
    for i in range(8):
        row = []
        for j in range(8):
            cell = img[i * cell_h:(i+1)*cell_h, j*cell_w : (j+1) * cell_w]
            cell = cell.flatten()
            max_val = np.max(cell)
            row.append(max_val)

        array_camera_res.append(row)

    array_camera_res = np.array(array_camera_res)

    if np.argwhere(array_camera_res > LED_value).size == 0:
        continue

    print(array_camera_res)

    # if max of picture < 255: save and break
