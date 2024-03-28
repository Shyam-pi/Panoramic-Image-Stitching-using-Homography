## Import necessary libraries here (You can add libraries you want to use here)
import cv2
import numpy as np
import matplotlib.pyplot as plt
from match_utils import *
from homography_utils import *
import warnings

warnings.filterwarnings("ignore")

def getStitchedImage(im_list):

  # Creating the canvas for the stitched image
  c_height = max([im.shape[0] for im in im_list])
  c_width = sum([im.shape[1] for im in im_list])
  canvas = np.uint8(np.zeros((3*c_height,c_width,3)))
  canvas[c_height:c_height*2, im_list[0].shape[1]:im_list[0].shape[1]*2, :] = im_list[1]

  H0 = ransacH(im_list[0], canvas)
  H2 = ransacH(im_list[2], canvas)
  H3 = H2 @ ransacH(im_list[3],im_list[2])

  warped1 = cv2.warpPerspective(im_list[0], H0,(c_width, 3*c_height))
  warped2 = cv2.warpPerspective(im_list[2], H2,(c_width, 3*c_height))
  warped3 = cv2.warpPerspective(im_list[3], H3,(c_width, 3*c_height))

  for warped in [warped1,warped2,warped3]:
    canvas[canvas == 0] = warped[canvas == 0]

  cv2.imshow('Before trimming',cv2.resize(canvas, (int(canvas.shape[1]*0.1), int(canvas.shape[0]*0.1))))

  args = np.where(canvas!=0)
  trim = canvas[np.min(args[0]):np.max(args[0]), np.min(args[1]):np.max(args[1]), :]
  
  cv2.imshow('After trimming',cv2.resize(trim, (int(trim.shape[1]*0.15), int(trim.shape[0]*0.15))))

  cv2.waitKey(0)

  cv2.destroyAllWindows()

  cv2.imwrite("results/stitched.png", trim)

def blur(img):
    img = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)
    return img

def main():
    # Reading and resizing images

  im_list = []
  for i in range(1,5,1):
      im_list.append(cv2.imread("image_" + str(i) +".jpg"))

  scale = 0.5

  w = int(im_list[0].shape[1] * scale)
  h = int(im_list[0].shape[0] * scale)

  for i in range(len(im_list)):
      im_list[i] = blur(im_list[i])
      im_list[i] = cv2.resize(im_list[i], (w,h))
    
    # Stitching the images
    
  getStitchedImage(im_list=im_list)

if __name__ == "__main__":
  main()