from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

def coordinate_l2r(ql, flip_axis: str):
    szs = {'x': np.array([[-1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., 1.]]),
           'y': np.array([[1., 0., 0.],
                          [0., -1., 0.],
                          [0., 0., 1.]]),
           'z': np.array([[1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., -1.]])}
    sz = szs[flip_axis]

    if ql.size == 4:
        sz_homo = np.zeros((4, 4))
        sz_homo[:3, :3] = sz
        sz_homo[3, 3] = 1
        return sz_homo.dot(ql)
    elif ql.size == 3:
        return sz.dot(ql)

def rot_x_l(roll: float):
    return np.array([[1.,           0.,           0.],
                     [0., np.cos(roll), -np.sin(roll)],
                     [0, np.sin(roll), np.cos(roll)]])

def rot_y_l(pitch: float):
    return np.array([[np.cos(pitch), 0., np.sin(pitch)],
                     [0.,            1.,             0.],
                     [-np.sin(pitch), 0., np.cos(pitch)]])

def rot_z_l(yaw: float):
    return np.array([[np.cos(yaw),  -np.sin(yaw), 0.],
                     [np.sin(yaw), np.cos(yaw), 0.],
                     [0.,                    0., 1.]])

def rot_x_l2r(roll: float, flip_axis: str):
    szs = {'x': np.array([[-1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., 1.]]),
           'y': np.array([[1., 0., 0.],
                          [0., -1., 0.],
                          [0., 0., 1.]]),
           'z': np.array([[1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., -1.]])}
    sz = szs[flip_axis]

    return np.matmul(np.matmul(sz, rot_x_l(roll)), sz)

def rot_y_l2r(pitch: float, flip_axis: str):
    szs = {'x': np.array([[-1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., 1.]]),
           'y': np.array([[1., 0., 0.],
                          [0., -1., 0.],
                          [0., 0., 1.]]),
           'z': np.array([[1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., -1.]])}
    sz = szs[flip_axis]

    return np.matmul(np.matmul(sz, rot_y_l(pitch)), sz)

def rot_z_l2r(yaw: float, flip_axis: str):
    szs = {'x': np.array([[-1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., 1.]]),
           'y': np.array([[1., 0., 0.],
                          [0., -1., 0.],
                          [0., 0., 1.]]),
           'z': np.array([[1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., -1.]])}
    sz = szs[flip_axis]

    return np.matmul(np.matmul(sz, rot_z_l(yaw)), sz)

def rot_matrix_l(roll: float, pitch: float, yaw: float, order='yxz'):
    out = None

    dict_axis_angle = {'x': roll,
                       'y': pitch,
                       'z': yaw}

    for axis in order:
        if out is None:
            out = eval('rot_{}_l({})'.format(axis, str(dict_axis_angle[axis])))
        else:
            out = np.matmul(out, eval('rot_{}_l({})'.format(axis, str(dict_axis_angle[axis]))))

    return out

def homogenous_transformation_matrix_l(roll: float, pitch: float, yaw: float, x: float, y: float, z: float, order='yxz'):
    rot_max = rot_matrix_l(roll, pitch, yaw, order)
    out = np.zeros((4, 4))

    # assign rotation matrix
    out[:3, :3] = rot_max

    # assign translation
    out[0, 3] = x
    out[1, 3] = y
    out[2, 3] = z

    out[3, 3] = 1

    return out

def homogenous_transformation_matrix_l2r(roll: float, pitch: float, yaw: float, x: float, y: float, z: float, flip_axis: str, order='yxz'):
    szs = {'x': np.array([[-1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., 1.]]),
           'y': np.array([[1., 0., 0.],
                          [0., -1., 0.],
                          [0., 0., 1.]]),
           'z': np.array([[1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., -1.]])}
    sz = szs[flip_axis]

    rot_max_r = rot_matrix_l2r(roll, pitch, yaw, flip_axis, order)
    trans_l = np.array([x, y, z])
    trans_r = sz.dot(trans_l)

    out = np.zeros((4, 4))

    # assign rotation matrix
    out[:3, :3] = rot_max_r

    # assign translation
    out[0, 3] = trans_r[0]
    out[1, 3] = trans_r[1]
    out[2, 3] = trans_r[2]

    out[3, 3] = 1

    return out

def rot_matrix_l2r(roll: int, pitch: float, yaw: float, flip_axis: str, order='yxz'):
    szs = {'x': np.array([[-1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., 1.]]),
           'y': np.array([[1., 0., 0.],
                          [0., -1., 0.],
                          [0., 0., 1.]]),
           'z': np.array([[1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., -1.]])}
    sz = szs[flip_axis]

    return np.matmul(np.matmul(sz, rot_matrix_l(roll, pitch, yaw, order)), sz)

def convert_vFoV_2_hFoV(vFoVdeg: float, aspect_ratio: float):
    vFoVrad = vFoVdeg / 180 * np.pi
    hFoVrad = 2. * np.arctan(np.tan(vFoVrad / 2) * aspect_ratio)
    hFoVdeg = hFoVrad / np.pi * 180

    return hFoVdeg

def compute_intrinsic_matrix(hFoV: int, vFoV: int, width: int, height: int):
    x = width / 2
    y = height / 2
    fx = x / np.tan((hFoV / 2) / 180 * np.pi)
    fy = y / np.tan((vFoV / 2) / 180 * np.pi)

    return np.array([[fx, 0, x],
                     [0, fy, y],
                     [0,  0, 1]])