from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import random
from typing import Tuple, List

def random_offset(dst: float) -> Tuple[float, float]:
    '''
     given the total length, randomly generate length in x and y-axis
     :param dst: float
     :return:
     offset_x, offset_z: length in x and y axis
     '''
    theta = random.uniform(-np.pi, np.pi)

    offset_x = np.cos(theta) * dst
    offset_z = np.sin(theta) * dst

    return offset_x, offset_z

def random_offset_dst_angle(dst: List[int], angles: List[List[int]]) -> Tuple[float, float]:
    dst = random.uniform(dst[0], dst[1])

    angle = random.choice(angles)
    theta = random.uniform(angle[0], angle[1])

    offset_x = np.cos(theta / 180 * np.pi) * dst
    offset_z = np.sin(theta / 180 * np.pi) * dst

    return offset_x, offset_z

def project_2d_3d(pixel, depth_image, cameraMatrix):
    '''
    project 2d pixel on the image to 3d by depth info
    :param pixel: x, y
    :param cameraMatrix: camera intrinsic matrix
    :param depth_image: depth image
    :param depth_scale: depth scale that trans raw data to mm
    :return:
    q_C: 3d coordinate of pixel with respect to camera frame
    '''
    depth = depth_image[pixel[1], pixel[0]]

    pxl = np.linalg.inv(cameraMatrix).dot(
        np.array([pixel[0] * depth, pixel[1] * depth, depth]))
    q_C = np.array([pxl[0], pxl[1], pxl[2], 1])

    return q_C

def project_3d_2d(q_C, cameraMatrix):
    '''
    project 3d pixel in camera frame to 2d pixel in the image plane
    :param point: 3d coordinate of pixel with respect to camera frame
    :return:
    pxl: x, y in the image plane
    '''
    pxl = cameraMatrix.dot(q_C[:-1])
    pxl = [int(pxl[0]/pxl[-1]), int(pxl[1]/pxl[-1]), int(pxl[-1]/pxl[-1])]

    return pxl[:2]
