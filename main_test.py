from UglyCamera import UglyCamera
import cv2
import numpy as np
import json

class ProcessingUtils():
    @staticmethod
    def crop_img(img):
        img = img[220:390, 220:400]
        img = cv2.rotate(img, cv2.ROTATE_180)
        return img

    @staticmethod
    def draw_mesh(img):
        h,w = img.shape[:2]
        cell_h = h // 8
        cell_w = w // 8
        for i in range(1,8):
            cv2.line(img, (0, i * cell_h), (w, i*cell_h), (255,255,255), 1)
            cv2.line(img, (i*cell_w, 0), (i*cell_w, h), (255,255,255), 1)
        return img 

if __name__ == "__main__":
    cam = UglyCamera()
    cam.start()

    for img in cam:
        cv2.imshow("IMG" , img)
        print(img.shape)
        img = ProcessingUtils.crop_img(img)
        mesh_img = ProcessingUtils.draw_mesh(img)
        
        w,h,c = mesh_img.shape
        cell_h = h // 8
        cell_w = w // 8
        pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
        pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

        M = cv2.getPerspectiveTransform(pts1, pts2)
        warped_image = cv2.warpPerspective(mesh_img, M, (w, h))
        array_camera_res = []
        for i in range(8):
            row = []
            for j in range(8):
                cell = mesh_img[i * cell_h:(i+1)*cell_h, j*cell_w : (j+1) * cell_w]
                cell = cell.flatten()
                cell = cell[cell != 255]
                if cell.size > 0:
                    max_val = np.max(cell)
                else:
                    max_val = 255
                row.append(max_val)
            array_camera_res.append(row)
        
        array_camera_res = np.array(array_camera_res)
        
        with open('optical.json', 'w') as json_file:
            json.dump(array_camera_res.tolist(), json_file)
        np.save('optical.npy',array_camera_res)
        print(array_camera_res)
        cv2.imshow("MESH GRID",mesh_img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cam.stop()
            cv2.destroyAllWindows()
        
