# Panorama-Algorithm

# Synopsis

In this project, you will implement a system to combine a series of horizontally overlapping photographs into a single panoramic image. We give the ORB feature detector and descriptor. You will use ORB to first detect discriminating features in the images and find the best matching features in the other images. Then, using RANSAC, you will automatically align the photographs (determine their overlap and relative positions) and then blend the resulting images into a single seamless panorama. We have provided you with a graphical interface that lets you view the results of the various intermediate steps of the process. We have also provided you with some test images and skeleton code to get you started with the project.

The project will consist of a pipeline of tabs visualized through AutostitchUI that will operate on images or intermediate results to produce the final panorama output.  

The steps required to create a panorama are listed below. You will be creating two ways to stitch a panorama: using translations (where you'll need to pre-spherically-warp the input images) and homographies, where you align the input images directly. The steps in square brackets are only used with the spherical warping route:

 

Step

1. Take pictures on a tripod (or handheld)

2. [Warp to spherical coordinates]

3. Extract features

4. Match features

5. Align neighboring pairs using RANSAC

6. Write out list of neighboring translations

7. Correct for drift

8. Read in [warped] images and blend them

9. Crop the result and import into a viewer
