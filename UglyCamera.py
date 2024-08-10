import cv2
import subprocess
import numpy as np

class UglyCamera():
    def __init__(self, height=480, width=640, shutter_ms=100, gain=1, awbgains=(1,1)):
        self.height = height
        self.width = width
        self.shutter_ms = shutter_ms
        self.gain = gain
        self.awbgains = awbgains
        self.off = True
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.off:
            raise StopIteration

        cmd_str = f"rpicam-still -o tmp.png --height {self.height} --width {self.width} --shutter {self.shutter_ms * 1000} --gain {self.gain} --awbgains {','.join([str(val) for val in self.awbgains])} --immediate --nopreview --vflip"
        cmd_arr = cmd_str.split(" ")
        subprocess.run(cmd_arr, stdout=subprocess.DEVNULL)
        img = cv2.imread("tmp.png")
        return img

    def start(self):
        self.off = False

    def stop(self):
        self.off = True
    
if __name__ == "__main__":
    cam = UglyCamera()

    cam.start()
    print("Press Q to exit")
    for img in cam:
        cv2.imshow(
            "USB Camera Test", img
        )
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cam.stop()
            cv2.destroyAllWindows()

    
