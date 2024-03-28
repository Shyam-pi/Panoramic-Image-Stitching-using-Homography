import cv2
import numpy as np
import matplotlib.pyplot as plt
from match_utils import *

"""Helper functions to get Homography using RANSAC"""

def errorH(coord1, coord2, H):
  # Function: Computing the Homography transformation error
  error = 0
  for i in range(coord1.shape[0]):
    transformed = H @ coord1[i,:].T
    transformed = transformed/transformed[2]
    error = error + np.linalg.norm(coord2[i,:].T - transformed , axis = 0)
  return error/coord1.shape[0]

def computeH(x1, y1, x2, y2):
  #  Function: compute Homographic matrix from corresponding points
  # YOUR CODE HERE: 

  A = np.zeros((x1.shape[0]*2,9))

  for i in range(x1.shape[0]):
    x = x1[i]
    x_ = x2[i]
    y = y1[i]
    y_ = y2[i]
    A[i*2:i*2 + 2,:] = np.array([[-x, -y, -1, 0, 0, 0, x*x_, y*x_, x_],
                                [0, 0, 0, -x, -y, -1, x*y_, y*y_, y_]])
    
  # SVD solution
  _ , _ , V = np.linalg.svd(A)
  h = V.T[:,8]
  H = np.reshape(h, (3,3))

  return H

def normalizeH(coordinates, matrix = False):
  # Function: find the transformation to make it zero mean and the variance as sqrt(2)
  # YOUR CODE HERE:
  og_coord = coordinates
  x = coordinates[:,1]
  y = coordinates[:,0]

  mean = (np.mean(x),np.mean(y))
  translate = np.array([[1,0,-mean[0]],
                        [0,1,-mean[1]],
                        [0,0,1]])
  
  # coord = np.transpose(np.dot(translate, np.transpose(og_coord)))
  coord = (translate @ og_coord.T).T

  k_x = np.sqrt((x.shape[0])/(np.sum(coord[:,0]**2)))
  k_y = np.sqrt((y.shape[0])/(np.sum(coord[:,1]**2)))

  scaling = np.array([[k_x,0,0],
                      [0,k_y,0],
                      [0,0,1]])
  
  # coord = np.transpose(np.dot(scaling, np.transpose(coord)))
  coord = (scaling @ coord.T).T

  x_new = coord[:,0]
  y_new = coord[:,1]

  if matrix:
    T = np.dot(scaling, translate)
    return T
  
  else:
    return x_new, y_new

def denormalizeH(coord1, coord2, H):
  # Function: to reverse the normalization process and get the resultant homography
  T = normalizeH(coord1, matrix = True)
  T_ = normalizeH(coord2, matrix = True)
  H_denormalized = np.linalg.inv(T_) @ H @ T

  return H_denormalized

def getInliersH(pt1, pt2, H, thresh):
  # Function: implement the criteria checking inliers. 
  # YOUR CODE HERE:

  inliers = 0

  for i in range(pt1.shape[0]):
    transformed = H @ pt1[i,:].T
    transformed = transformed/transformed[2]
    score = np.linalg.norm(pt2[i,:].T - transformed)

    if score < thresh:
      inliers = inliers + 1

  return inliers
  
def ransacH(img1, img2, thresh = 0.01):
  # Find normalization matrix
  # Transform point set 1 and 2
  # RANSAC based 8-point algorithm
  # YOUR CODE HERE: 

  coord1, coord2 = getMatches(img1, img2)
  
  x1N, y1N = normalizeH(coord1)
  x2N, y2N = normalizeH(coord2)

  pt1 = np.ones((coord1.shape[0],3))
  pt2 = np.ones((coord2.shape[0],3))

  pt1[:,0] = x1N
  pt1[:,1] = y1N

  pt2[:,0] = x2N
  pt2[:,1] = y2N

  inliers = []
  H_bank = []

  for i in range(1000):
    rand = np.random.choice(coord1.shape[0], 4, replace=False)
    x1R = x1N[rand]
    y1R = y1N[rand]
    x2R = x2N[rand]
    y2R = y2N[rand]

    H = computeH(x1R, y1R, x2R, y2R)

    inliers.append(getInliersH(pt1, pt2, H, thresh))
    H_bank.append(H)

  best = np.argmax(np.array(inliers))
  H_best = H_bank[best]
  
  H_best = denormalizeH(coord1, coord2, H_best)

  return H_best