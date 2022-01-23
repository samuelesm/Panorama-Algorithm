import os
import cv2
import numpy as np

def warpLocal(src, uv):
    '''
    Input:
        src --    source image in a numpy array with values in [0, 255].
                  The dimensions are (rows, cols, color bands BGR).
        uv --     warped image in terms of addresses of each pixel in the source
                  image in a numpy array.
                  The dimensions are (rows, cols, addresses of pixels [:,:,0]
                  are x (i.e., cols) and [:,:,1] are y (i.e., rows)).
    Output:
        warped -- resampled image from the source image according to provided
                  addresses in a numpy array with values in [0, 255]. The
                  dimensions are (rows, cols, color bands BGR).
    '''
    width = src.shape[1]
    height  = src.shape[0]
    mask = cv2.inRange(uv[:,:,1],0,height-1.0)&cv2.inRange(uv[:,:,0],0,width-1.0)
    warped = cv2.remap(src, uv[:, :, 0].astype(np.float32),\
             uv[:, :, 1].astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    img2_fg = cv2.bitwise_and(warped,warped,mask = mask)
    return img2_fg


def computeSphericalWarpMappings(dstShape, f, k1, k2):
    '''
    Compute the spherical warp. Compute the addresses of each pixel of the
    output image in the source image.

    Input:
        dstShape -- shape of input / output image in a numpy array.
                    [number or rows, number of cols, number of bands]
        f --        focal length in pixel as int
                    See assignment description on how to find the focal length
        k1 --       horizontal distortion as a float
        k2 --       vertical distortion as a float
    Output:
        uvImg --    warped image in terms of addresses of each pixel in the
                    source image in a numpy array.
                    The dimensions are (rows, cols, addresses of pixels
                    [:,:,0] are x (i.e., cols) and [:,:,1] are y (i.e., rows)).
    '''

    # calculate minimum y value
    vec = np.zeros(3)
    vec[0] = np.sin(0.0) * np.cos(0.0)
    vec[1] = np.sin(0.0)
    vec[2] = np.cos(0.0) * np.cos(0.0)
    min_y = vec[1]

    # calculate spherical coordinates
    # (x,y) is the spherical image coordinates.
    # (xf,yf) is the spherical coordinates, e.g., xf is the angle theta
    # and yf is the angle phi
    one = np.ones((dstShape[0],dstShape[1]))
    xf = one * np.arange(dstShape[1])
    yf = one.T * np.arange(dstShape[0])
    yf = yf.T

    xf = ((xf - 0.5 * dstShape[1]) / f)
    yf = ((yf - 0.5 * dstShape[0]) / f - min_y)
    xn = np.divide(np.multiply(np.sin(xf), np.cos(yf)),
                   np.multiply(np.cos(xf), np.cos(yf)))
    yn = np.divide(np.sin(yf), np.multiply(np.cos(xf), np.cos(yf)))
    xn2 = np.multiply(xn, xn)
    yn2 = np.multiply(yn, yn)
    r2 = xn2 + yn2
    r4 = np.multiply(r2, r2)
    k = 1 + k1 * r2 + k2 * r4
    xt = np.multiply(xn, k)
    yt = np.multiply(yn, k)
    
    # Convert back to regular pixel coordinates
    xn = 0.5 * dstShape[1] + xt * f
    yn = 0.5 * dstShape[0] + yt * f
    uvImg = np.dstack((xn,yn))
    return uvImg


def warpSpherical(image, focalLength, k1=-0.21, k2=0.26):
    '''
    Input:
        image --       filename of input image as string
        focalLength -- focal length in pixel as int
                       see assignment description on how to find the focal
                       length
        k1, k2 --      Radial distortion parameters
    Output:
        dstImage --    output image in a numpy array with
                       values in [0, 255]. The dimensions are (rows, cols,
                       color bands BGR).
    '''

    # compute spherical warp
    # compute the addresses of each pixel of the output image in the
    # source image
    uv = computeSphericalWarpMappings(np.array(image.shape), focalLength, k1, \
        k2)

    # warp image based on backwards coordinates
    return warpLocal(image, uv)

