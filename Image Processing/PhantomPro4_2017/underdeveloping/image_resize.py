import cv2
import numpy as np
img=cv2.imread('MacShot 8.png')
cv2.namedWindow('frame',cv2.WINDOW_KEEPRATIO)
cv2.resizeWindow('frame',900,600)
img1=img[900:950,880:890]
img1=0
img[550:600,260:320]=0
img[390:450,1560:1660]=0
img1=img[150:930,230:1690]
cv2.imshow('frame',img1)
cv2.waitKey(0)
cv2.destroyAllWindows()