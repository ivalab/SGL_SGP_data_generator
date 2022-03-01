from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import __init__paths

from ai2thor.controller import Controller

import os
import numpy as np
import random
import time
import cv2
import json
import argparse

from utils.agent_movement import teleport_face_2_obj
from utils.objects import spawn_objects_wo_reps, spawn_object_near_sink, spawn_obj_over_obj, \
    dirty, isObjExist, isVisible


def main(args):
    # load json file
    descriptions = json.load(open(os.path.join(args.save_root, 'task_description.json')))

    # object types for cut and cuttable objects
    obj_clean = descriptions['scene']['kitchen']['objects']['clean']
    obj_cleanable = descriptions['scene']['kitchen']['objects']['cleanable']

    # list of objects won't be included in the scene
    removed_objects = descriptions['scene']['kitchen']['objects']['remove']

    # small objects in the scene
    small_objects = descriptions['scene']['kitchen']['objects']['small_objects']

    # excluded receptacles when call InitialRandomSpawn action
    ex_recep = descriptions['scene']['kitchen']['excluded_receptacles']

    # natural language template
    nl_tmp = descriptions['natural_language']

    # list of objects have contain affordance
    containable_objects = ['Cup', 'Mug', 'Pan', 'Plate', 'Pot', 'Bottle', 'Kettle']

    # spawn type of object cleanable
    basin_spawn_type = ['inside', 'outside']

    # intialize the controller
    controller = Controller(scene="FloorPlan1",
                            # image modalities
                            renderDepthImage=True,
                            renderInstanceSegmentation=True,
                            # camera properties
                            width=640,
                            height=480,
                            )

    if args.continue_gen:
        cnt = len(os.listdir(args.save_root)) - 1
    else:
        cnt = 0
    while cnt < args.number_data:
        scene_rendered = False
        obj1, obj2 = None, None
        obj1_type, obj2_type = '', ''
        miss_type, obj_observed = 0, 0
        task_type = None
        while not scene_rendered:
            # initialize the scene
            scene_idx = random.randint(args.scene_start_idx, args.scene_end_idx)
            scene_idx = str(scene_idx)
            while scene_idx not in descriptions['scene']['kitchen']['floorplan']:
                scene_idx = random.randint(args.scene_start_idx, args.scene_end_idx)
                scene_idx = str(scene_idx)
            scene_type = "FloorPlan{}".format(scene_idx)
            controller.reset(scene=scene_type)

            # randomize the missing type, 0 for missing both and 1 for missing either
            miss_type = random.choice([0, 1])
            if miss_type == 0:
                # number of attempt made for the current floorplan and objects
                attempt = 0

                while attempt < args.max_attempt_per_scene and not scene_rendered:
                    obj1_type = obj_clean[0]
                    obj2_type = random.choice(obj_cleanable)

                    # call InitialRandomSpawn action
                    obj1_exist = obj2_exist = False
                    spawn_objects_wo_reps(controller, ex_recep, [], placeStationary=False)
                    obj1_exist = isObjExist(controller, obj1_type)
                    obj2_exist = isObjExist(controller, obj2_type)

                    if not obj1_exist or not obj2_exist:
                        attempt += 1
                        continue

                    # obj2 has to be outside of obj1 otherwise they will be observed together
                    task_type = 'outside'

                    # randomize either 1st or 2nd object to be observed
                    obj_observed = random.choice([1, 2])

                    if obj_observed == 1:
                        teleport_face_2_obj(controller, obj1_type, look_down_angle=30)

                        # object 1 should be observed
                        scene_rendered = isVisible(controller, obj1_type)
                        # object 2 should be missing
                        scene_rendered &= not isVisible(controller, obj2_type)
                        # sanity check the mask to make sure the target object
                        # is obvious in the scene
                        for objectid in controller.last_event.instance_masks:
                            if objectid.split('|')[0] == obj1_type or objectid.split('|')[-1] == obj1_type:
                                scene_rendered &= (np.count_nonzero(
                                    controller.last_event.instance_masks[objectid] * 255) > 100)
                    elif obj_observed == 2:
                        # make object 2 dirty
                        dirty(controller, obj2_type)

                        teleport_face_2_obj(controller, obj2_type, look_down_angle=30)

                        # object 2 should be observed
                        scene_rendered = isVisible(controller, obj2_type)
                        # object 1 should be missing
                        scene_rendered &= not isVisible(controller, obj1_type)
                        # sanity check the mask to make sure the target object
                        # is obvious in the scene
                        for objectid in controller.last_event.instance_masks:
                            if objectid.split('|')[0] == obj2_type or objectid.split('|')[-1] == obj2_type:
                                scene_rendered &= (np.count_nonzero(
                                    controller.last_event.instance_masks[objectid] * 255) > 100)
                    else:
                        raise ValueError

                    attempt += 1
            elif miss_type == 1:
                # indicator that no objects to be observed
                obj_observed = 0
                # number of attempt made for the current floorplan and objects
                attempt = 0

                obj1_type = obj_clean[0]
                obj2_type = random.choice(obj_cleanable)

                # call InitialRandomSpawn action
                spawn_objects_wo_reps(controller, ex_recep, [], placeStationary=False)

                # randomly determine spawning obj2 inside or outside obj1
                task_type = random.choice(basin_spawn_type)
                if obj2_type in ['Pan', 'Pot']:
                    task_type = 'outside'

                for obj in controller.last_event.metadata["objects"]:
                    if attempt >= args.max_attempt_per_scene or scene_rendered:
                        break

                    if obj["objectType"] != obj1_type and obj["objectType"] != obj2_type:
                        teleport_success = teleport_face_2_obj(controller, obj["objectType"], look_down_angle=30)
                        if teleport_success:
                            # sanity check if both objects are invisible
                            scene_rendered = not isVisible(controller, obj1_type)
                            scene_rendered &= not isVisible(controller, obj2_type)

                        attempt += 1

        for obj in controller.last_event.metadata["objects"]:
            if obj['objectType'] == obj1_type:
                obj1 = obj

            if obj['objectType'] == obj2_type:
                obj2 = obj

        # randomize the material and lighting
        if args.rand_mat:
            controller.step(
                action="RandomizeMaterials",
                useTrainMaterials=None,
                useValMaterials=None,
                useTestMaterials=None,
                inRoomTypes=None
            )
        if args.rand_lit:
            controller.step(
                action="RandomizeLighting",
                brightness=(0.5, 1.5),
                randomizeColor=False,
                hue=(0, 1),
                saturation=(0.5, 1),
                synchronized=False
            )

        if args.debug:
            cv2.imshow('debug', controller.last_event.cv2img)
            cv2.waitKey(0)

        # random select from complete, incomplete and implicit
        nl = nl_tmp[task_type]
        tp = random.choice(list(nl.keys()))

        if tp in ['complete', 'incomplete']:
            nl_type = 'explicit'
        elif tp == 'implicit':
            nl_type = 'implicit'

        nl = nl[tp]
        nl = random.choice(nl)
        if 'obj2' in nl:
            nl = nl.replace('obj2', obj2_type.lower())

        # save the data and annotation
        if not os.path.exists(os.path.join(args.save_root, str(cnt))):
            os.mkdir(os.path.join(args.save_root, str(cnt)))

        # save ground-truth for bounding box label
        all_labels = descriptions['labels']
        with open(os.path.join(args.save_root, str(cnt), 'labels.txt'), 'w+') as f:
            for objectid in controller.last_event.instance_detections2D:
                if objectid.split('|')[0] in all_labels:
                    object_type = objectid.split('|')[0]
                # handle sinkbasin which is a subset to sink
                elif objectid.split('|')[-1] in all_labels:
                    object_type = objectid.split('|')[-1]
                else:
                    continue

                gt = []
                gt.append(objectid)
                gt.append(all_labels[object_type]['Category'][0])
                for aff in all_labels[object_type]['Affordance']:
                    gt.append(aff)
                for attri in all_labels[object_type]['Attribute']:
                    gt.append(attri)

                # only append dirty attribute to the one we make it dirty
                if object_type == obj2_type:
                    gt.append('dirty')

                f.write(' '.join(gt[:]) + '\n')

        # save 2D bounding box for objects
        with open(os.path.join(args.save_root, str(cnt), '2d_bbx.txt'), 'w+') as f:
            for objectid in controller.last_event.instance_detections2D:
                f.write(objectid + ' ' + str(controller.last_event.instance_detections2D[objectid][0]) + ' '
                        + str(controller.last_event.instance_detections2D[objectid][1]) + ' '
                        + str(controller.last_event.instance_detections2D[objectid][2]) + ' '
                        + str(controller.last_event.instance_detections2D[objectid][3])
                        + '\n')

        # save ground-truth for relation between bounding boxes
        all_relations = descriptions['relation']
        with open(os.path.join(args.save_root, str(cnt), 'relations.txt'), 'w+') as f:
            objectid_list = list(controller.last_event.instance_detections2D.keys())
            for object1_id in objectid_list:
                if object1_id.split('|')[0] in all_relations:
                    object1_type = object1_id.split('|')[0]
                elif object1_id.split('|')[-1] in all_relations:
                    object1_type = object1_id.split('|')[-1]
                else:
                    continue

                for object2_id in objectid_list:
                    if object2_id == object1_id:
                        continue
                    elif object2_id.split('|')[0] in all_relations[object1_type]:
                        object2_type = object2_id.split('|')[0]
                    else:
                        continue

                    for relation in all_relations[object1_type][object2_type]:
                        # for clean relation, object2 has to be dirty
                        if relation == 'clean':
                            isDirty = False
                            for obj in controller.last_event.metadata["objects"]:
                                if obj['objectType'] == object2_type:
                                    if obj['isDirty']:
                                        isDirty = True

                            if not isDirty:
                                continue

                        f.write(object1_id + ' ' + object2_id + ' ' + relation + '\n')

        # save rgb image
        cv2.imwrite(os.path.join(args.save_root, str(cnt), 'rgb_image.png'), controller.last_event.cv2img)
        # save depth image
        np.save(os.path.join(args.save_root, str(cnt), 'depth_image.npy'), controller.last_event.depth_frame)
        # save agent information: position, rotation, camera horizon
        with open(os.path.join(args.save_root, str(cnt), 'transformations.json'), 'w+') as f:
            anno = {}
            # agent related information
            anno['agent'] = {}
            anno['agent']['position'] = {}
            anno['agent']['position']['x'] = controller.last_event.metadata["cameraPosition"]['x']
            anno['agent']['position']['y'] = controller.last_event.metadata["cameraPosition"]['y']
            anno['agent']['position']['z'] = controller.last_event.metadata["cameraPosition"]['z']
            anno['agent']['rotation'] = {}
            anno['agent']['rotation']['x'] = controller.last_event.metadata["agent"]["rotation"]['x']
            anno['agent']['rotation']['y'] = controller.last_event.metadata["agent"]["rotation"]['y']
            anno['agent']['rotation']['z'] = controller.last_event.metadata["agent"]["rotation"]['z']
            anno['agent']['rotation']['cameraHorizon'] = controller.last_event.metadata["agent"]["cameraHorizon"]

            # cut object related information
            anno['clean_object'] = {}
            anno['clean_object']['position'] = obj1['position']
            anno['clean_object']['rotation'] = obj1['rotation']

            # cuttable object realted information
            anno['cleanable_object'] = {}
            anno['cleanable_object']['position'] = obj2['position']
            anno['cleanable_object']['rotation'] = obj2['rotation']

            json.dump(anno, f)

        # save masks for objects
        for objectid in controller.last_event.instance_masks:
            cv2.imwrite(os.path.join(args.save_root, str(cnt), '{}_mask.png'.format(objectid)),
                        controller.last_event.instance_masks[objectid] * 255)

        # save natural language template
        with open(os.path.join(args.save_root, str(cnt), 'natural_language.txt'), 'w+') as f:
            f.write(nl)

        # save the type of natural language template
        with open(os.path.join(args.save_root, str(cnt), 'natural_language_type.txt'), 'w+') as f:
            f.write(nl_type)

            # save PDDL goal state
            with open(os.path.join(args.save_root, str(cnt), 'pddl_goal_state.txt'), 'w+') as f:
                if miss_type == 0 and obj_observed == 1:
                    f.write('clean {} {}'.format("unknown", obj1_type.lower()))
                elif miss_type == 0 and obj_observed == 2:
                    f.write('clean {} {}'.format(obj2_type.lower(), "unknown"))
                elif miss_type == 1:
                    f.write('clean {} {}'.format("unknown", "unknown"))
                else:
                    raise ValueError

        # increment the counter by 1
        cnt += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('save_root', type=str, default='../data/official/clean_task',
                        help='Root directory for saving generated data')
    parser.add_argument('--scene_start_idx', type=int, default=1, help='Kitchen[1, 30], Living_rooms[201, 230]')
    parser.add_argument('--scene_end_idx', type=int, default=30, help='Kitchen[1, 30], Living_rooms[201, 230]')
    parser.add_argument('--number_data', type=int, default=20000, help='Total number of data generated')
    parser.add_argument('--rand_mat', action='store_true', help='whether to randomize material during the process of generating dataset')
    parser.add_argument('--rand_lit', action='store_true', help='whether to randomize lighting during the process of generating dataset')
    parser.add_argument('--max_attempt_per_scene', type=int, default=5, help='Maximal attempts for rendering the scene '
                                                                             'under certain combination of floorplan and objects')
    parser.add_argument('--debug', action='store_true',
                        help='whether to visualize the scene')
    parser.add_argument('--continue_gen', action='store_true', help='whether to continue generating the number of data')
    args = parser.parse_args()

    # make the root directory for saving data if not exist
    if not os.path.exists(args.save_root):
        os.mkdir(args.save_root)

    main(args)
