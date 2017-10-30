import vision
import cv2
import matplotlib.pyplot as plt
import numpy as np

IM_NAME = 'test.png'


new_webcam = vision.Webcam()

img = new_webcam.get_frame()
new_webcam.close()
edges = vision.detect_edge(img)

cv2.imshow("img",img)
cv2.imshow("edges",edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("input.png",img)
cv2.imwrite("edges.png",edges)

# new_connection = vision.Vision()
# color = new_connection.get_depth()
# img = color.asarray(np.float32)
# cv2.imwrite(IM_NAME,img)
# new_connection.close()

#img = cv2.imread(IM_NAME)
#gray_img = vision.convert_greyscale(img)
#rotated_img = vision.rotate_image(img,90)
#cv2.imshow("gray_img",gray_img)
#cv2.imshow("rotated_img",rotated_img)
# cv2.imshow("img",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# plt.figure(1)
# plt.imshow(img[:,:,0])
# plt.figure(2)
# plt.imshow(img[:,:,1])
# plt.figure(3)
# plt.imshow(img[:,:,2])
# plt.figure(4)
# plt.imshow(img[:,:,3])
# plt.show()




