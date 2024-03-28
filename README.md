# Panoramic Image Stitching using Homography

**Note**: This project was done as a part of the course ENPM673 - Perception for Autonomous Robots in Spring 2023 at the University of Maryland, College Park.

## Overview
This project focuses on stitching multiple images together to create a panoramic view using homography techniques. The pipeline includes feature matching, homography estimation, image warping, and trimming.

## Pipeline
1. **Feature Matching:** Use Scale-Invariant Feature Transform (SIFT) features to find matching points between consecutive images.
2. **Homography Estimation:** Compute the homography matrix between pairs of images using RANSAC.
3. **Image Warping:** Warp and stitch images together using the estimated homographies.
4. **Trimming:** Remove excess black pixels to obtain the final stitched image.

## Running the Code
To run the code:
1. Clone this repository to your local machine.
2. Navigate to the `image_stitching` folder.
3. Execute the `stitch.py` script.
4. Wait for the execution to complete. It may take around 15 seconds.
5. View the stitched image in an OpenCV window.
6. Find the final trimmed output saved as `stitched.png` in the `results` folder.

## Note
- For detailed descriptions of the algorithms and implementation, refer to the project report.
- Adjust parameters as needed for optimization and visualization purposes.
