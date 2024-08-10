from UglyCamera import UglyCamera
import cv2

class ProcessingUtils():
    @classmethod
    def crop_img(img):
        return img[100:270, 240:410]

    @classmethod
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
        img = ProcessingUtils.crop_img(img)
        mesh_img = ProcessingUtils.draw_mesh(img)

        cv2.imwrite("mesh_img.png", mesh_img)

        # array_camera_res = []
        # for i in range(8):
        #     row = []
        #     for j in range(8):
        #         cell = roate_img[i * cell_h:(i+1)*cell_h, j*cell_w : (j+1) * cell_w]
        #         cell = cell.flatten()
        #         cell = cell[cell != 255]
        #         if cell.size > 0:
        #             # print(cell)
        #             max_val = np.max(cell)
        #         else:
        #             max_val = 255
        #         row.append(max_val)
        #     array_camera_res.append(row)
        
        # array_camera_res = np.array(array_camera_res)
        # print(array_camera_res)

        # if cv2.waitKey(1) & 0xFF == ord("q") or True:
        cam.stop()
        cv2.destroyAllWindows()
