# Panorama-Algorithm

# Synopsis

In this project, I implemented a system that combines a series of horizontally overlapping photographs into a single panoramic image. First, ORB is used to detect discriminating features in the images and find the best matching features in the other images. Then, using RANSAC, the photos are aligned the photographs and then blended into a single seamless panorama. 

The following are the steps used to achieve the panorama stitching

1. Take pictures on a tripod (or handheld)

2. Warp to spherical coordinates

3. Extract features

4. Match features

5. Align neighboring pairs using RANSAC

6. Write out list of neighboring translations

7. Correct for drift

8. Read in warped images and blend them

9. Crop the result and import into a viewer
