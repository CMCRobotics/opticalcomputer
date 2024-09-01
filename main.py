from Camera import Camera
import cv2
import numpy as np

class ProcessingUtils():
    @staticmethod
    def crop_img(img):
        img = img[210:400, 240:430]
        return img

    def project_img(img, collect_coordinates=False, img_src_coordinate=[[19,20], [16,175], [174,177], [169,19]]):

        def collect_callback(event, x, y, flags, paste_coordinate_list):
            cv2.imshow('Collect coordinates', img_src_copy)
            if event == cv2.EVENT_LBUTTONUP:
                paste_coordinate_list.append([x,y])
                cv2.circle(img_src_copy, (x,y), 2, (255,255,255), -1)

        h,w = img.shape[:2]
        img_src_coordinate = []
        img_dest_coordinate = np.array([[0,0], [0,h], [w,h], [w,0]]) # Anticlockwise from top left

        if collect_coordinates:
            img_src_copy = img.copy()
            cv2.namedWindow('Collect coordinates')
            cv2.setMouseCallback('Collect coordinates', collect_callback, img_src_coordinate)

            while True:
                cv2.waitKey(1)
                if len(img_src_coordinate) == 4: break
        img_src_coordinate = np.array(img_src_coordinate)

        matrix, _ = cv2.findHomography(img_src_coordinate, img_dest_coordinate, 0)
        projected_img = cv2.warpPerspective(img, matrix, (w,h))
        return projected_img

    @staticmethod
    def draw_mesh(img, grid_size:int = 8, line_color:tuple[int,int,int] = (255,255,255)):
        h,w = img.shape[:2]
        cell_h = h // grid_size
        cell_w = w // grid_size
        for i in range(1,8):
            cv2.line(img, (0, i * cell_h), (w, i*cell_h), line_color, 1)
            cv2.line(img, (i*cell_w, 0), (i*cell_w, h), line_color, 1)
        return img 

if __name__ == "__main__":
    cam = Camera()
    cam.start()

    for img in cam:
        cv2.imshow("IMG" , img)
        print(img.shape)
        img = ProcessingUtils.crop_img(img)
        mesh_img = ProcessingUtils.draw_mesh(img)
        
        w,h,c = mesh_img.shape
        cell_h = h // 8
        cell_w = w // 8

        array_camera_res = []
        for i in range(8):
            row = []
            for j in range(8):
                cell = mesh_img[i * cell_h:(i+1)*cell_h, j*cell_w : (j+1) * cell_w]
                cell = cell.flatten()
                # Filter the 255 values
                cell = cell[cell != 255]
                if cell.size > 0:
                    max_val = np.max(cell)
                else:
                    # If the are all 255, then the max value should to 255
                    max_val = 255
                row.append(max_val)
            array_camera_res.append(row)
        
        array_camera_res = np.array(array_camera_res)
        
        print(array_camera_res)
        cv2.imshow("MESH GRID",mesh_img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cam.stop()
            cv2.destroyAllWindows()
