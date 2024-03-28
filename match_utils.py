import cv2
import numpy as np
import matplotlib.pyplot as plt

"""Helper functions to get matching points"""

def detectKeypoints(img):
  sift = cv2.xfeatures2d.SIFT_create(2000)
  keypoints, descriptors = sift.detectAndCompute(img,None)
  return keypoints, descriptors

def getCoordinates(kp):
  coord = np.ones((len(kp),3))
  for i in range(len(kp)):
    coord[i,0] = kp[i].pt[0]
    coord[i,1] = kp[i].pt[1]
  return coord

def getMatches(img1, img2):
  kp1, dp1 = detectKeypoints(img1)
  kp2, dp2 = detectKeypoints(img2)

  coord1 = getCoordinates(kp1)
  coord2 = getCoordinates(kp2)

  matches = []

  # DR_thresh = 0.2
  DR_thresh = 0.4

  mode = "DR"

  for i in range(dp1.shape[0]):
    temp = dp1[i,:]
    norm = dp2.copy()

    norm = norm - temp

    norm = np.linalg.norm(norm, axis=1)

    if mode == "DR":
      sorted_norm = np.sort(norm)
      DR = sorted_norm[0]/sorted_norm[1]
      if DR<DR_thresh:
        arg = np.argmin(norm)
        matches.append([int(i),int(arg)])

  matches = np.array(matches)

  coord_matches1 = coord1[matches[:,0]]
  coord_matches2 = coord2[matches[:,1]]

  return coord_matches1, coord_matches2