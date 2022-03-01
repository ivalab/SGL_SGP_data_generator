from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from utils.utils import random_offset, random_offset_dst_angle

from ai2thor.controller import Controller

from typing import Dict, List
import numpy as np
import random

def spawn_object_near_sink(controller, workRange, obj1_type, obj2_type, obj_ref_type, y_offset, removed_objects: List[str],
                           placeStationary=False):
    obj1 = None
    obj2 = None
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj1_type:
            obj1 = obj
        elif obj["objectType"] == obj2_type:
            obj2 = obj

    dst = float('inf')
    height_y = 0
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj_ref_type:
            if (obj['position']['x'] - obj1['position']['x']) ** 2 + (obj['position']['z'] - obj1['position']['z']) ** 2 < dst:
                dst = (obj['position']['x'] - obj1['position']['x']) ** 2 + (obj['position']['z'] - obj1['position']['z']) ** 2
                height_y = obj['position']['y']

    obj2_info = {}
    obj2_info["objectName"] = obj2["name"]

    offset_x, offset_z = random_offset_dst_angle(workRange[0], workRange[1])
    obj2_info["rotation"] = obj2["rotation"].copy()
    obj2_info["position"] = obj1["position"].copy()
    obj2_info["position"]['x'] += offset_x
    obj2_info["position"]['z'] += offset_z
    obj2_info["position"]['y'] = height_y + y_offset

    object_poses = []
    obj1_iy = None
    obj2_iy = None
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj2["objectType"]:
            object_poses.append(obj2_info)
            obj2_iy = obj["position"]['y']
        elif obj["objectType"] == obj1["objectType"]:
            object_poses.append({"objectName": obj["name"],
                                 "rotation": obj["rotation"],
                                 "position": obj["position"]})
            obj1_iy = obj["position"]['y']
        elif obj["objectType"] in removed_objects:
            continue
        else:
            object_poses.append({"objectName": obj["name"],
                                 "rotation": obj["rotation"],
                                 "position": obj["position"]})
    controller.step(
        action='SetObjectPoses',
        objectPoses=object_poses,
        placeStationary=placeStationary,
    )

    # run an amount of Pass action unitl all objects are not moving
    # if exceed the limit, manually set all objects to be static
    scene_static = False
    max_pass = 20
    cnt = 1
    obj1_fy = None
    obj2_fy = None
    while not scene_static:
        if cnt > max_pass:
            setAllObjectStatic(controller)

        controller.step(action='Pass')
        cnt += 1

        allstatic = True
        for obj in controller.last_event.metadata["objects"]:
            if obj["objectType"] == obj1["objectType"]:
                obj1_fy = obj['position']['y']

            if obj["objectType"] == obj2["objectType"]:
                obj2_fy = obj['position']['y']

            if obj['visible']:
                allstatic &= not obj['isMoving']

        scene_static = allstatic

    if abs(obj1_iy - obj1_fy) < 0.5 and abs(obj2_iy - obj2_fy) < 0.5:
        res = True
    else:
        res = False

    res &= check_scene_isvalid(controller, obj1_type, obj2_type)

    return res

def spawn_obj_over_obj(controller, obj1_type, obj2_type, removed_objects: List[str], placeStationary=False, lift_height=0.0):
    '''
    Spawn object 2 over the object 1. Provide a little height to avoid
    two objects collide and lead to breaking. The engine will make
    object 2 land on the object 1.
    :param controller: AI2THOR Controller
    :param obj1_type: str
    :param obj2_type: str
    :param lift_height: float
    :return: None - currently no feedback since it should be successful if the engine doesn't do anything wired.
    '''
    obj1 = None
    obj2 = None
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj1_type:
            obj1 = obj

        if obj["objectType"] == obj2_type:
            obj2 = obj

    obj2_info = {}
    obj2_info["objectName"] = obj2["name"]
    obj2_info["rotation"] = obj2["rotation"].copy()
    obj2_info["position"] = obj1["position"].copy()
    # move obj2 up a little bit to avoid two objects overlapped
    obj2_info["position"]['y'] += lift_height

    object_poses = []
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj2["objectType"]:
            object_poses.append(obj2_info)
        elif obj["objectType"] == obj1["objectType"]:
            object_poses.append({"objectName": obj["name"],
                                 "rotation": obj["rotation"],
                                 "position": obj["position"]})
        elif obj["objectType"] in removed_objects:
            continue
        else:
            object_poses.append({"objectName": obj["name"],
                                 "rotation": obj["rotation"],
                                 "position": obj["position"]})
    controller.step(
        action='SetObjectPoses',
        objectPoses=object_poses,
        placeStationary=placeStationary,
    )

    # run an amount of Pass action unitl all objects are not moving
    # if exceed the limit, manually set all objects to be static
    scene_static = False
    max_pass = 30
    cnt = 1
    while not scene_static:
        if cnt > max_pass:
            setAllObjectStatic(controller)

        controller.step(action='Pass')
        cnt += 1

        allstatic = True
        for obj in controller.last_event.metadata["objects"]:
            if obj['visible']:
                allstatic &= not obj['isMoving']

        scene_static = allstatic

def spawn_objects_below_microwave(controller: Controller, workRange, obj1_type: str, obj2_type: str,
                                 obj_ref_type: str, removed_objects: List[str], yoffset=0.0, ifyoffset=False,
                                 placeStationary=False) -> Dict[str, float]:
    '''
    This function is designed for spawning objects below those microwaves which are installed
    above the stoveburner. The objects are spawned over the stoveburner therefore it
    requires the information of it.
    :param controller: AI2THOR controller
    :param workRange: offset and angles based on object 2
    :param obj1_type: name of object 1
    :param obj2_type: name of object 2
    :param obj_ref_type: name of reference object, mainly used for getting information of y
    :param removed_objects: list of objects are removed from scene
    :return:
    '''
    obj1 = None
    obj2 = None
    obj_ref = None

    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj1_type:
            obj1 = obj

        if obj["objectType"] == obj2_type:
            obj2 = obj

        if obj["objectType"] == obj_ref_type:
            obj_ref = obj

    obj2_info = {}
    obj2_info["objectName"] = obj2["name"]

    # randomize a little bit offset in x and z axis to make object separate
    offset_x, offset_z = random_offset_dst_angle(workRange[0], workRange[1])
    obj2_info["rotation"] = obj2["rotation"].copy()
    obj2_info["position"] = obj1["position"].copy()
    obj2_info["position"]['x'] += offset_x
    obj2_info["position"]['z'] += offset_z
    obj2_info["position"]['y'] = obj_ref['position']['y']
    if ifyoffset:
        obj2_info["position"]['y'] += yoffset

    # if check_if_objects_nearby(controller, obj2_type, obj2_info["position"]['x'], obj2_info["position"]['z'], 0.15):

    obj1_iy = None
    obj2_iy = None
    object_poses = []
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj2["objectType"]:
            object_poses.append(obj2_info)
            obj2_iy = obj['position']['y']
        elif obj["objectType"] == obj1["objectType"]:
            object_poses.append({"objectName": obj["name"],
                                 "rotation": obj["rotation"],
                                 "position": obj["position"]})
            obj1_iy = obj['position']['y']
        elif obj["objectType"] in removed_objects:
            continue
        else:
            object_poses.append({"objectName": obj["name"],
                                 "rotation": obj["rotation"],
                                 "position": obj["position"]})
    controller.step(
        action='SetObjectPoses',
        objectPoses=object_poses,
        placeStationary=placeStationary
    )

    # run an amount of Pass action unitl all objects are not moving
    # if exceed the limit, manually set all objects to be static
    scene_static = False
    max_pass = 20
    cnt = 1
    obj1_fy = None
    obj2_fy = None
    while not scene_static:
        if cnt > max_pass:
            setAllObjectStatic(controller)

        controller.step(action='Pass')
        cnt += 1

        allstatic = True
        for obj in controller.last_event.metadata["objects"]:
            if obj["objectType"] == obj1["objectType"]:
                obj1_fy = obj['position']['y']

            if obj["objectType"] == obj2["objectType"]:
                obj2_fy = obj['position']['y']

            if obj['visible']:
                allstatic &= not obj['isMoving']

        scene_static = allstatic

    if abs(obj1_iy - obj1_fy) < 0.5 and abs(obj2_iy - obj2_fy) < 0.5:
        res = True
    else:
        res = False

    res &= check_scene_isvalid(controller, obj1_type, obj2_type)

    return res

def spawn_objects_w_workingrange(controller: Controller, workRange, obj1_type: str, obj2_type: str,
                                 removed_objects: List[str], yoffset=0, ifyoffset=False,
                                 placeStationary=False) -> Dict[str, float]:
    '''
    This function is designed for spawning object 2 in the certain areas, which
     is specified as workRange, of object 1.
    :param controller: AI2THOR controller
    :param workRange: offset and angles based on object 2
    :param obj1_type: name of object 1
    :param obj2_type: name of object 2
    :param removed_objects: list of objects are removed from scene
    :param max_attempts: maximal attempts to generate object 2 around object 1
    :return: Bool
    '''
    obj1 = None
    obj2 = None
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj1_type:
            obj1 = obj

        if obj["objectType"] == obj2_type:
            obj2 = obj

    obj2_info = {}
    obj2_info["objectName"] = obj2["name"]

    offset_x, offset_z = random_offset_dst_angle(workRange[0], workRange[1])
    obj2_info["rotation"] = obj2["rotation"].copy()
    obj2_info["position"] = obj1["position"].copy()
    obj2_info["position"]['x'] += offset_x
    obj2_info["position"]['z'] += offset_z

    if ifyoffset:
        obj2_info["position"]['y'] += yoffset

    # if check_if_objects_nearby(controller, obj2_type, obj2_info["position"]['x'], obj2_info["position"]['z'], 0.15):
    #     success = True
    #     break

    object_poses = []
    obj1_iy = None
    obj2_iy = None
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj2["objectType"]:
            object_poses.append(obj2_info)
            obj2_iy = obj["position"]['y']
        elif obj["objectType"] == obj1["objectType"]:
            object_poses.append({"objectName": obj["name"],
                                 "rotation": obj["rotation"],
                                 "position": obj["position"]})
            obj1_iy = obj["position"]['y']
        elif obj["objectType"] in removed_objects:
            continue
        else:
            object_poses.append({"objectName": obj["name"],
                                 "rotation": obj["rotation"],
                                 "position": obj["position"]})
    controller.step(
        action='SetObjectPoses',
        objectPoses=object_poses,
        placeStationary=placeStationary,
    )

    # run an amount of Pass action unitl all objects are not moving
    # if exceed the limit, manually set all objects to be static
    scene_static = False
    max_pass = 20
    cnt = 1
    obj1_fy = None
    obj2_fy = None
    while not scene_static:
        if cnt > max_pass:
            setAllObjectStatic(controller)

        controller.step(action='Pass')
        cnt += 1

        allstatic = True
        for obj in controller.last_event.metadata["objects"]:
            if obj["objectType"] == obj1["objectType"]:
                obj1_fy = obj["position"]['y']

            if obj["objectType"] == obj2["objectType"]:
                obj2_fy = obj["position"]['y']

            if obj['visible']:
                allstatic &= not obj['isMoving']

        scene_static = allstatic

    if abs(obj1_iy - obj1_fy) < 0.35 and abs(obj2_iy - obj2_fy) < 0.35:
        res = True
    else:
        res = False

    res &= check_scene_isvalid(controller, obj1_type, obj2_type)

    return res

def setAllObjectStatic(controller):
    object_poses = []
    for obj in controller.last_event.metadata["objects"]:
        object_poses.append({"objectName": obj["name"],
                             "rotation": obj["rotation"],
                             "position": obj["position"]})
    controller.step(
        action='SetObjectPoses',
        objectPoses=object_poses,
        placeStationary=True,
    )

def isObjExist(controller, obj_type):
    '''
    Check if this object exists in the current scene
    :param controller: AI2THOR Controller
    :param obj_type: str
    :return: Bool
    '''
    obj_exist = False
    for o in controller.last_event.metadata["objects"]:
        if o["objectType"] == obj_type:
            obj_exist = True

    return obj_exist

def isVisible(controller, obj_type: str):
    '''
    Check if the given object is visiable by the agent
    :param controller: AI2THOR Controller
    :param obj_type: str
    :return: Bool or None
    '''
    res = False
    # Condition 1: check if any objects with the same object type
    # are labeled as visible
    for obj in controller.last_event.metadata["objects"]:
        if obj['objectType'] == obj_type:
            # Not exit in case there are multiple objects
            res |= obj['visible']

    # Condition 2: check if any objects' masks have more
    # than 1 pixel
    for objectId in controller.last_event.instance_masks:
        if obj_type in objectId:
            res |= (np.count_nonzero(controller.last_event.instance_masks[objectId]) > 0)

    # Condition 3: check if any objects' bbx has width or height
    # more than 0
    for objectId in controller.last_event.instance_detections2D:
        if obj_type in objectId:
            res |= (controller.last_event.instance_detections2D[objectId][2] -
                    controller.last_event.instance_detections2D[objectId][0]) > 0
            res |= (controller.last_event.instance_detections2D[objectId][3] -
                    controller.last_event.instance_detections2D[objectId][1]) > 0

    return res

def check_scene_isvalid(controller, obj1_type, obj2_type):
    '''
    check if the spawned scene is valid based on the following policies:
    1. Two objects should not be broken
    2. (not included since it is just opposite of visible) Object 2 should not be obstructed
    3. (not implemented) Distance between object 2 between other objects should not be too close
    Notice: visible requiers the agent move to the object, which will be checked later
    :param controller: AI2THOR Controller
    :param obj1_type: str
    :param obj2_type: str
    :return: Bool
    '''
    res = True

    for obj in controller.last_event.metadata["objects"]:
        if obj['objectType'] == obj1_type:
            res &= not obj['isBroken']
            # res &= not obj['obstructed']

        if obj['objectType'] == obj2_type:
            res &= not obj['isBroken']
            # res &= not obj['obstructed']

    return res

def check_if_objects_nearby(controller, obj_type, obj_x, obj_z, threshold):
    for obj in controller.last_event.metadata["objects"]:
        if obj['objectType'] != obj_type:
            if np.sqrt((obj['position']['x'] - obj_x) ** 2 + (obj['position']['z'] - obj_z) ** 2) <= threshold:
                return False

    return True

def spawn_objects_wo_reps(controller: Controller, excludedReceptacles: List[str], excludedObjectIds: List[str], placeStationary=True):
    controller.step(action="InitialRandomSpawn",
                    randomSeed=random.randint(0, 100),
                    forceVisible=False,
                    numPlacementAttempts=15,
                    placeStationary=placeStationary,
                    numDuplicatesOfType=[],
                    excludedReceptacles=excludedReceptacles,
                    excludedObjectIds=excludedObjectIds,
    )

    object_poses = []
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] in excludedObjectIds:
            continue
        else:
            object_poses.append({"objectName": obj["name"],
                                 "rotation": obj["rotation"],
                                 "position": obj["position"]})
    controller.step(
        action='SetObjectPoses',
        objectPoses=object_poses,
        placeStationary=placeStationary
    )

def dirty(controller: Controller, obj_type: str):
    obj = None
    for o in controller.last_event.metadata["objects"]:
        if o["objectType"] == obj_type:
            obj = o

    _ = controller.step(
        action="DirtyObject",
        objectId=obj['objectId'],
        forceAction=True
    )

def contain(controller: Controller, obj1_type: str, obj2_type: str):
    obj1 = None
    obj2 = None
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj1_type:
            obj1 = obj

        if obj["objectType"] == obj2_type:
            obj2 = obj

    obj1['position'] = obj2['position']

    object_poses = []
    for obj in controller.last_event.metadata["objects"]:
        if obj["objectType"] == obj2_type:
            object_poses.append({"objectName": obj2["name"],
                                 "rotation": obj2["rotation"],
                                 "position": obj2["position"]})
        elif obj["objectType"] == obj1_type:
            object_poses.append({"objectName": obj1["name"],
                                 "rotation": obj1["rotation"],
                                 "position": obj1["position"]})
        else:
            object_poses.append({"objectName": obj["name"],
                                 "rotation": obj["rotation"],
                                 "position": obj["position"]})
    controller.step(
        action='SetObjectPoses',
        objectPoses=object_poses
    )

    # setobjectpose action won't lead to the scene change, need to apply some
    # dummy actions like lookup and then lookdown to refresh the image
    # look down by 30 degree
    controller.step(
        action="LookDown",
        degrees=30
    )
    controller.step(
        action="LookUp",
        degrees=30
    )
