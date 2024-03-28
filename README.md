# Panoramic Image Stitching using Homography

**Note**: This project was done as a part of the course ENPM673 - Perception for Autonomous Robots in Spring 2023 at the University of Maryland, College Park.

## Overview
This project focuses on stitching multiple images together to create a panoramic view using homography techniques. The pipeline includes feature matching, homography estimation, image warping, and trimming.

## Pipeline
1. **Feature Matching:** Use Scale-Invariant Feature Transform (SIFT) features to find matching points between consecutive images.
2. **Homography Estimation:** Compute the homography matrix between pairs of images using RANSAC.
3. **Image Warping:** Warp and stitch images together using the estimated homographies.

![image](https://github.com/Shyam-pi/Panoramic-Image-Stitching-using-Homography/assets/57116285/0deb742e-e47d-48fc-9ac6-5c9ccaf2cfba)![image](https://github.com/Shyam-pi/Panoramic-Image-Stitching-using-Homography/assets/57116285/152bd882-68c5-42c2-9170-4620ee314771)

4. **Trimming:** Remove excess black pixels to obtain the final stitched image.

![image](https://github.com/Shyam-pi/Panoramic-Image-Stitching-using-Homography/assets/57116285/9b383759-2612-45ff-bbba-aac7c80ea753)

## Running the Code
To run the code:
1. Clone this repository to your local machine.
2. Execute the `stitch.py` script.
3. Wait for the execution to complete. It may take around 15 seconds.
4. View the stitched image in an OpenCV window.
5. Find the final trimmed output saved as `stitched.png` in the `results` folder.

## Note
- For detailed descriptions of the algorithms and implementation, refer to the project report.
- Adjust parameters as needed for optimization and visualization purposes.
