from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Dict, List
import numpy as np
from ai2thor.controller import Controller

def closest_position(object_position: Dict[str, float], reachable_positions: List[Dict[str, float]]) -> Dict[str, float]:
    out = reachable_positions[0]
    min_distance = float('inf')
    for pos in reachable_positions:
        # NOTE: y is the vertical direction, so only care about the x/z ground positions
        dist = sum([(pos[key] - object_position[key]) ** 2 for key in ["x", "z"]])
        if dist < min_distance:
            min_distance = dist
            out = pos
    return out

def teleport_face_2_pos(controller: Controller, pos_x: float, pos_z: float, forward=0.1, ifMoveForward=False,
                        look_down=30, ifLookDown=False):
    # compute the rotation that turns the agent face to the object
    agent_x, agent_z = controller.last_event.metadata["agent"]["position"]['x'], \
                       controller.last_event.metadata["agent"]["position"]['z']
    yaw = -np.arctan2(-agent_x + pos_x, -agent_z + pos_z) / np.pi * 180
    # rotate the agent
    controller.step(action="RotateLeft", degrees=yaw)

    # move backward to have wider view
    if ifMoveForward:
        controller.step(
            action="MoveAhead",
            moveMagnitude=forward
        )

    # look down by 30 degree
    if ifLookDown:
        controller.step(
            action="LookDown",
            degrees=look_down
        )

def teleport_face_2_obj(controller: Controller, obj_type: str, forward_dst=0.1, look_down_angle=30, ifMoveBack=False):
    obj = None
    for item in controller.last_event.metadata["objects"]:
        if item["objectType"] == obj_type:
            obj = item

    if obj is None:
        return False

    # teleport the closest reachable position of obj1
    # get all reachable positions for the agent
    reachable_positions = controller.step(action="GetReachablePositions").metadata["actionReturn"]
    # compute the closest reachable to obj1
    closest_pos = closest_position(obj["position"], reachable_positions)
    # teleport the agent to closest position
    closest_pos["rotation"] = {}
    closest_pos["rotation"]['x'] = 0
    closest_pos["rotation"]['y'] = 0
    closest_pos["rotation"]['z'] = 0
    controller.step(action="Teleport", **closest_pos)

    # compute the rotation that turns the agent face to the object
    agent_x, agent_z = controller.last_event.metadata["agent"]["position"]['x'], \
                       controller.last_event.metadata["agent"]["position"]['z']
    yaw = -np.arctan2(-agent_x + obj["position"]['x'], -agent_z + obj["position"]['z'])/np.pi*180
    # rotate the agent
    controller.step(action="RotateLeft", degrees=yaw)

    # move forward by 0.1 meters to get closer
    controller.step(
        action="MoveAhead",
        moveMagnitude=forward_dst
    )

    # move backward to have wider view
    if ifMoveBack:
        controller.step(
            action="MoveBack",
            moveMagnitude=forward_dst
        )

    # look down by 30 degree
    if look_down_angle != 0:
        controller.step(
            action="LookDown",
            degrees=look_down_angle
        )

    # in case the scene isn't updated
    controller.step(action='Pass')

    return True
