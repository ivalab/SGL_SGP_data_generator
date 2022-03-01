import json
import numpy as np
import os
import argparse

def main(args):
    file = {}

    #############################
    # scene related information #
    #############################
    file['scene'] = {}

    # kitchen
    file['scene']['kitchen'] = {}

    ## excluded receptacles
    ex_receptacles = ['Microwave', 'StoveBurner', 'Toaster']
    file['scene']['kitchen']['excluded_receptacles'] = ex_receptacles
    ## objects
    obj_cook = ['StoveBurner', 'Microwave', 'Toaster'] # 'Toaster'
    obj_subject = ['Egg', 'Potato', 'Lettuce', 'Bread'] # 'BreadSliced' - work together with Toaster, 'EggCracked' - need to be placed in the bowl, 'PotatoSliced' - Potato has to be sliced first
    file['scene']['kitchen']['objects'] = {}
    file['scene']['kitchen']['objects']['cook'] = obj_cook
    file['scene']['kitchen']['objects']['cookable'] = obj_subject

    ## all labels for object category, affordance and general attribute
    file['labels'] = {}
    file['labels']['Toaster'] = {}
    file['labels']['Toaster']['Category'] = ['toaster']
    file['labels']['Toaster']['Affordance'] = ['contain']
    file['labels']['Toaster']['Attribute'] = ['__background__']
    file['labels']['Knife'] = {}
    file['labels']['Knife']['Category'] = ['knife']
    file['labels']['Knife']['Affordance'] = ['cut']
    file['labels']['Knife']['Attribute'] = ['graspable']
    file['labels']['ButterKnife'] = {}
    file['labels']['ButterKnife']['Category'] = ['knife']
    file['labels']['ButterKnife']['Affordance'] = ['cut']
    file['labels']['ButterKnife']['Attribute'] = ['graspable']
    file['labels']['Egg'] = {}
    file['labels']['Egg']['Category'] = ['egg']
    file['labels']['Egg']['Affordance'] = ['__background__']
    file['labels']['Egg']['Attribute'] = ['cooking', 'graspable']
    file['labels']['Apple'] = {}
    file['labels']['Apple']['Category'] = ['apple']
    file['labels']['Apple']['Affordance'] = ['__background__']
    file['labels']['Apple']['Attribute'] = ['cutting', 'graspable', 'cooking', 'edible']
    file['labels']['BreadSliced'] = {}
    file['labels']['BreadSliced']['Category'] = ['bread']
    file['labels']['BreadSliced']['Affordance'] = ['__background__']
    file['labels']['BreadSliced']['Attribute'] = ['cutting', 'graspable', 'cooking', 'edible']
    file['labels']['Bread'] = {}
    file['labels']['Bread']['Category'] = ['bread']
    file['labels']['Bread']['Affordance'] = ['__background__']
    file['labels']['Bread']['Attribute'] = ['cutting', 'graspable', 'cooking', 'edible']
    file['labels']['Lettuce'] = {}
    file['labels']['Lettuce']['Category'] = ['lettuce']
    file['labels']['Lettuce']['Affordance'] = ['__background__']
    file['labels']['Lettuce']['Attribute'] = ['cutting', 'graspable', 'cooking', 'edible']
    file['labels']['Potato'] = {}
    file['labels']['Potato']['Category'] = ['potato']
    file['labels']['Potato']['Affordance'] = ['__background__']
    file['labels']['Potato']['Attribute'] = ['cutting', 'graspable', 'cooking']
    file['labels']['Tomato'] = {}
    file['labels']['Tomato']['Category'] = ['tomato']
    file['labels']['Tomato']['Affordance'] = ['__background__']
    file['labels']['Tomato']['Attribute'] = ['cutting', 'graspable', 'cooking', 'edible']
    file['labels']['SinkBasin'] = {}
    file['labels']['SinkBasin']['Category'] = ['sink']
    file['labels']['SinkBasin']['Affordance'] = ['clean', 'contain']
    file['labels']['SinkBasin']['Attribute'] = ['__background__']
    file['labels']['Bowl'] = {}
    file['labels']['Bowl']['Category'] = ['bowl']
    file['labels']['Bowl']['Affordance'] = ['contain']
    file['labels']['Bowl']['Attribute'] = ['graspable']
    file['labels']['Cup'] = {}
    file['labels']['Cup']['Category'] = ['cup']
    file['labels']['Cup']['Affordance'] = ['contain']
    file['labels']['Cup']['Attribute'] = ['graspable']
    file['labels']['Mug'] = {}
    file['labels']['Mug']['Category'] = ['mug']
    file['labels']['Mug']['Affordance'] = ['contain']
    file['labels']['Mug']['Attribute'] = ['graspable']
    file['labels']['Pan'] = {}
    file['labels']['Pan']['Category'] = ['pan']
    file['labels']['Pan']['Affordance'] = ['contain', 'cook']
    file['labels']['Pan']['Attribute'] = ['graspable']
    file['labels']['Plate'] = {}
    file['labels']['Plate']['Category'] = ['plate']
    file['labels']['Plate']['Affordance'] = ['contain']
    file['labels']['Plate']['Attribute'] = ['graspable']
    file['labels']['Pot'] = {}
    file['labels']['Pot']['Category'] = ['pot']
    file['labels']['Pot']['Affordance'] = ['contain']
    file['labels']['Pot']['Attribute'] = ['graspable']
    file['labels']['Microwave'] = {}
    file['labels']['Microwave']['Category'] = ['microwave']
    file['labels']['Microwave']['Affordance'] = ['cook', 'contain']
    file['labels']['Microwave']['Attribute'] = ['__background__']
    file['labels']['Book'] = {}
    file['labels']['Book']['Category'] = ['book']
    file['labels']['Book']['Affordance'] = ['__background__']
    file['labels']['Book']['Attribute'] = ['graspable']
    file['labels']['Bottle'] = {}
    file['labels']['Bottle']['Category'] = ['bottle']
    file['labels']['Bottle']['Affordance'] = ['contain']
    file['labels']['Bottle']['Attribute'] = ['graspable']
    file['labels']['CellPhone'] = {}
    file['labels']['CellPhone']['Category'] = ['cellphone']
    file['labels']['CellPhone']['Affordance'] = ['__background__']
    file['labels']['CellPhone']['Attribute'] = ['graspable']
    file['labels']['DishSponge'] = {}
    file['labels']['DishSponge']['Category'] = ['sponge']
    file['labels']['DishSponge']['Affordance'] = ['__background__']
    file['labels']['DishSponge']['Attribute'] = ['graspable']
    file['labels']['Fork'] = {}
    file['labels']['Fork']['Category'] = ['fork']
    file['labels']['Fork']['Affordance'] = ['__background__']
    file['labels']['Fork']['Attribute'] = ['graspable']
    file['labels']['Kettle'] = {}
    file['labels']['Kettle']['Category'] = ['kettle']
    file['labels']['Kettle']['Affordance'] = ['contain']
    file['labels']['Kettle']['Attribute'] = ['graspable']
    file['labels']['Ladle'] = {}
    file['labels']['Ladle']['Category'] = ['ladle']
    file['labels']['Ladle']['Affordance'] = ['__background__']
    file['labels']['Ladle']['Attribute'] = ['graspable']
    file['labels']['PaperTowel'] = {}
    file['labels']['PaperTowel']['Category'] = ['tissue']
    file['labels']['PaperTowel']['Affordance'] = ['__background__']
    file['labels']['PaperTowel']['Attribute'] = ['graspable']
    file['labels']['Pen'] = {}
    file['labels']['Pen']['Category'] = ['pen']
    file['labels']['Pen']['Affordance'] = ['__background__']
    file['labels']['Pen']['Attribute'] = ['graspable']
    file['labels']['Pencil'] = {}
    file['labels']['Pencil']['Category'] = ['pencil']
    file['labels']['Pencil']['Affordance'] = ['__background__']
    file['labels']['Pencil']['Attribute'] = ['graspable']
    file['labels']['PepperShaker'] = {}
    file['labels']['PepperShaker']['Category'] = ['pepper']
    file['labels']['PepperShaker']['Affordance'] = ['contain']
    file['labels']['PepperShaker']['Attribute'] = ['graspable']
    file['labels']['SaltShaker'] = {}
    file['labels']['SaltShaker']['Category'] = ['salt']
    file['labels']['SaltShaker']['Affordance'] = ['contain']
    file['labels']['SaltShaker']['Attribute'] = ['graspable']
    file['labels']['SoapBottle'] = {}
    file['labels']['SoapBottle']['Category'] = ['soap']
    file['labels']['SoapBottle']['Affordance'] = ['contain']
    file['labels']['SoapBottle']['Attribute'] = ['graspable']
    file['labels']['Spatula'] = {}
    file['labels']['Spatula']['Category'] = ['spatula']
    file['labels']['Spatula']['Affordance'] = ['__background__']
    file['labels']['Spatula']['Attribute'] = ['graspable']
    file['labels']['Spoon'] = {}
    file['labels']['Spoon']['Category'] = ['spoon']
    file['labels']['Spoon']['Affordance'] = ['__background__']
    file['labels']['Spoon']['Attribute'] = ['graspable']
    file['labels']['WineBottle'] = {}
    file['labels']['WineBottle']['Category'] = ['wine']
    file['labels']['WineBottle']['Affordance'] = ['contain']
    file['labels']['WineBottle']['Attribute'] = ['graspable']

    ## all relations between bounding boxes
    file['relation'] = {}
    file['relation']['Toaster'] = {}
    file['relation']['Toaster']['BreadSliced'] = ['contain']
    file['relation']['Knife'] = {}
    file['relation']['Knife']['Apple'] = ['cut']
    file['relation']['Knife']['Bread'] = ['cut']
    file['relation']['Knife']['Lettuce'] = ['cut']
    file['relation']['Knife']['Potato'] = ['cut']
    file['relation']['Knife']['Tomato'] = ['cut']
    file['relation']['ButterKnife'] = {}
    file['relation']['ButterKnife']['Apple'] = ['cut']
    file['relation']['ButterKnife']['Bread'] = ['cut']
    file['relation']['ButterKnife']['Lettuce'] = ['cut']
    file['relation']['ButterKnife']['Potato'] = ['cut']
    file['relation']['ButterKnife']['Tomato'] = ['cut']
    file['relation']['SinkBasin'] = {}
    file['relation']['SinkBasin']['Bowl'] = ['clean']
    file['relation']['SinkBasin']['Cup'] = ['clean']
    file['relation']['SinkBasin']['Mug'] = ['clean']
    file['relation']['SinkBasin']['Pan'] = ['clean']
    file['relation']['SinkBasin']['Plate'] = ['clean']
    file['relation']['SinkBasin']['Pot'] = ['clean']
    file['relation']['SinkBasin']['Apple'] = ['contain']
    file['relation']['SinkBasin']['Egg'] = ['contain']
    file['relation']['SinkBasin']['Potato'] = ['contain']
    file['relation']['SinkBasin']['Lettuce'] = ['contain']
    file['relation']['SinkBasin']['Tomato'] = ['contain']
    file['relation']['SinkBasin']['Bread'] = ['contain']
    file['relation']['SinkBasin']['Knife'] = ['contain']
    file['relation']['SinkBasin']['Bowl'] = ['contain']
    file['relation']['SinkBasin']['Cup'] = ['contain']
    file['relation']['SinkBasin']['Mug'] = ['contain']
    file['relation']['SinkBasin']['Plate'] = ['contain']
    file['relation']['SinkBasin']['Fork'] = ['contain']
    file['relation']['SinkBasin']['Spoon'] = ['contain']
    file['relation']['SinkBasin']['Pen'] = ['contain']
    file['relation']['SinkBasin']['DishSponge'] = ['contain']
    file['relation']['SinkBasin']['Pencil'] = ['contain']
    file['relation']['SinkBasin']['PepperShaker'] = ['contain']
    file['relation']['SinkBasin']['SaltShaker'] = ['contain']
    file['relation']['SinkBasin']['Book'] = ['contain']
    file['relation']['SinkBasin']['CellPhone'] = ['contain']
    file['relation']['SinkBasin']['Ladle'] = ['contain']
    file['relation']['SinkBasin']['DishSoap'] = ['contain']
    file['relation']['SinkBasin']['Spatula'] = ['contain']
    file['relation']['Microwave'] = {}
    file['relation']['Microwave']['Egg'] = ['cook', 'contain']
    file['relation']['Microwave']['Potato'] = ['cook', 'contain']
    file['relation']['Microwave']['Lettuce'] = ['cook', 'contain']
    file['relation']['Microwave']['Tomato'] = ['cook', 'contain']
    file['relation']['Microwave']['Bread'] = ['cook', 'contain']
    file['relation']['Microwave']['Apple'] = ['cook', 'contain']
    file['relation']['Microwave']['Knife'] = ['contain']
    file['relation']['Microwave']['Bowl'] = ['contain']
    file['relation']['Microwave']['Cup'] = ['contain']
    file['relation']['Microwave']['Mug'] = ['contain']
    file['relation']['Microwave']['Plate'] = ['contain']
    file['relation']['Microwave']['Fork'] = ['contain']
    file['relation']['Microwave']['Spoon'] = ['contain']
    file['relation']['Microwave']['Pen'] = ['contain']
    file['relation']['Microwave']['DishSponge'] = ['contain']
    file['relation']['Microwave']['Pencil'] = ['contain']
    file['relation']['Microwave']['PepperShaker'] = ['contain']
    file['relation']['Microwave']['SaltShaker'] = ['contain']
    file['relation']['Microwave']['Book'] = ['contain']
    file['relation']['Microwave']['CellPhone'] = ['contain']
    file['relation']['Microwave']['Ladle'] = ['contain']
    file['relation']['Microwave']['DishSoap'] = ['contain']
    file['relation']['Microwave']['Spatula'] = ['contain']
    file['relation']['Pan'] = {}
    file['relation']['Pan']['Egg'] = ['cook', 'contain']
    file['relation']['Pan']['Potato'] = ['cook', 'contain']
    file['relation']['Pan']['Lettuce'] = ['cook', 'contain']
    file['relation']['Pan']['Tomato'] = ['cook', 'contain']
    file['relation']['Pan']['Bread'] = ['cook', 'contain']
    file['relation']['Pan']['Apple'] = ['cook', 'contain']
    file['relation']['Pan']['Knife'] = ['contain']
    file['relation']['Pan']['Bowl'] = ['contain']
    file['relation']['Pan']['Cup'] = ['contain']
    file['relation']['Pan']['Mug'] = ['contain']
    file['relation']['Pan']['Plate'] = ['contain']
    file['relation']['Pan']['Fork'] = ['contain']
    file['relation']['Pan']['Spoon'] = ['contain']
    file['relation']['Pan']['Pen'] = ['contain']
    file['relation']['Pan']['DishSponge'] = ['contain']
    file['relation']['Pan']['Pencil'] = ['contain']
    file['relation']['Pan']['PepperShaker'] = ['contain']
    file['relation']['Pan']['SaltShaker'] = ['contain']
    file['relation']['Pan']['Ladle'] = ['contain']
    file['relation']['Pan']['Spatula'] = ['contain']
    file['relation']['Bowl'] = {}
    file['relation']['Bowl']['Apple'] = ['contain']
    file['relation']['Bowl']['Egg'] = ['contain']
    file['relation']['Bowl']['Potato'] = ['contain']
    file['relation']['Bowl']['Lettuce'] = ['contain']
    file['relation']['Bowl']['Tomato'] = ['contain']
    file['relation']['Bowl']['Bread'] = ['contain']
    file['relation']['Bowl']['Knife'] = ['contain']
    file['relation']['Bowl']['Cup'] = ['contain']
    file['relation']['Bowl']['Mug'] = ['contain']
    file['relation']['Bowl']['Fork'] = ['contain']
    file['relation']['Bowl']['Spoon'] = ['contain']
    file['relation']['Bowl']['Pen'] = ['contain']
    file['relation']['Bowl']['DishSponge'] = ['contain']
    file['relation']['Bowl']['Pencil'] = ['contain']
    file['relation']['Bowl']['PepperShaker'] = ['contain']
    file['relation']['Bowl']['SaltShaker'] = ['contain']
    file['relation']['Plate'] = {}
    file['relation']['Plate']['Apple'] = ['contain']
    file['relation']['Plate']['Egg'] = ['contain']
    file['relation']['Plate']['Potato'] = ['contain']
    file['relation']['Plate']['Lettuce'] = ['contain']
    file['relation']['Plate']['Tomato'] = ['contain']
    file['relation']['Plate']['Bread'] = ['contain']
    file['relation']['Plate']['Knife'] = ['contain']
    file['relation']['Plate']['Bowl'] = ['contain']
    file['relation']['Plate']['Cup'] = ['contain']
    file['relation']['Plate']['Mug'] = ['contain']
    file['relation']['Plate']['Fork'] = ['contain']
    file['relation']['Plate']['Spoon'] = ['contain']
    file['relation']['Plate']['PepperShaker'] = ['contain']
    file['relation']['Plate']['SaltShaker'] = ['contain']
    file['relation']['Pot'] = {}
    file['relation']['Pot']['Apple'] = ['contain']
    file['relation']['Pot']['Egg'] = ['contain']
    file['relation']['Pot']['Potato'] = ['contain']
    file['relation']['Pot']['Lettuce'] = ['contain']
    file['relation']['Pot']['Tomato'] = ['contain']
    file['relation']['Pot']['Bread'] = ['contain']
    file['relation']['Pot']['Knife'] = ['contain']
    file['relation']['Pot']['Bowl'] = ['contain']
    file['relation']['Pot']['Cup'] = ['contain']
    file['relation']['Pot']['Mug'] = ['contain']
    file['relation']['Pot']['Fork'] = ['contain']
    file['relation']['Pot']['Spoon'] = ['contain']
    file['relation']['Cup'] = {}
    file['relation']['Cup']['Apple'] = ['contain']
    file['relation']['Cup']['Egg'] = ['contain']
    file['relation']['Cup']['Potato'] = ['contain']
    file['relation']['Cup']['Tomato'] = ['contain']
    file['relation']['Cup']['Knife'] = ['contain']
    file['relation']['Cup']['Fork'] = ['contain']
    file['relation']['Cup']['Spoon'] = ['contain']
    file['relation']['Mug'] = {}
    file['relation']['Mug']['Apple'] = ['contain']
    file['relation']['Mug']['Egg'] = ['contain']
    file['relation']['Mug']['Potato'] = ['contain']
    file['relation']['Mug']['Tomato'] = ['contain']
    file['relation']['Mug']['Knife'] = ['contain']
    file['relation']['Mug']['Fork'] = ['contain']
    file['relation']['Mug']['Spoon'] = ['contain']
    # file['relation']['Bottle'] = {}
    # file['relation']['Bottle']['Apple'] = ['contain']
    # file['relation']['Bottle']['Egg'] = ['contain']
    # file['relation']['Bottle']['Potato'] = ['contain']
    # file['relation']['Bottle']['Lettuce'] = ['contain']
    # file['relation']['Bottle']['Tomato'] = ['contain']
    # file['relation']['Bottle']['Bread'] = ['contain']
    file['relation']['Kettle'] = {}
    file['relation']['Kettle']['Egg'] = ['contain']
    # file['relation']['Kettle']['Potato'] = ['contain']
    # file['relation']['Kettle']['Lettuce'] = ['contain']
    # file['relation']['Kettle']['Tomato'] = ['contain']
    # file['relation']['Kettle']['Bread'] = ['contain']
    # file['relation']['PepperShaker'] = {}
    # file['relation']['PepperShaker']['Apple'] = ['contain']
    # file['relation']['PepperShaker']['Egg'] = ['contain']
    # file['relation']['PepperShaker']['Potato'] = ['contain']
    # file['relation']['PepperShaker']['Lettuce'] = ['contain']
    # file['relation']['PepperShaker']['Tomato'] = ['contain']
    # file['relation']['PepperShaker']['Bread'] = ['contain']
    # file['relation']['SaltShaker'] = {}
    # file['relation']['SaltShaker']['Apple'] = ['contain']
    # file['relation']['SaltShaker']['Egg'] = ['contain']
    # file['relation']['SaltShaker']['Potato'] = ['contain']
    # file['relation']['SaltShaker']['Lettuce'] = ['contain']
    # file['relation']['SaltShaker']['Tomato'] = ['contain']
    # file['relation']['SaltShaker']['Bread'] = ['contain']
    # file['relation']['SoapBottle'] = {}
    # file['relation']['SoapBottle']['Apple'] = ['contain']
    # file['relation']['SoapBottle']['Egg'] = ['contain']
    # file['relation']['SoapBottle']['Potato'] = ['contain']
    # file['relation']['SoapBottle']['Lettuce'] = ['contain']
    # file['relation']['SoapBottle']['Tomato'] = ['contain']
    # file['relation']['SoapBottle']['Bread'] = ['contain']
    # file['relation']['WineBottle'] = {}
    # file['relation']['WineBottle']['Apple'] = ['contain']
    # file['relation']['WineBottle']['Egg'] = ['contain']
    # file['relation']['WineBottle']['Potato'] = ['contain']
    # file['relation']['WineBottle']['Lettuce'] = ['contain']
    # file['relation']['WineBottle']['Tomato'] = ['contain']
    # file['relation']['WineBottle']['Bread'] = ['contain']

    ### Height of the StoveBurner/Pot to be placed over stoveburner
    file['scene']['kitchen']['objects']['PlaceHeight'] = {}
    file['scene']['kitchen']['objects']['PlaceHeight']['0.0'] = [3, 8, 11, 13, 14, 16, 17, 18, 20, 29, 30]
    file['scene']['kitchen']['objects']['PlaceHeight']['0.035'] = [1, 2, 4, 5, 6, 7, 9, 10, 12, 15, 19, 21, 22, 23, 24, 25,
                                                                   26, 27, 28]

    ## dictionary for where microwave locates to index of scene type
    ## 0 -> over the stoveburner
    ## 1 -> on the countertop or just some flat surface where other objects can be plcaed
    file['scene']['kitchen']['objects']['Microwave'] = {}
    file['scene']['kitchen']['objects']['Microwave']['type'] = {}
    file['scene']['kitchen']['objects']['Microwave']['type']['0'] = [1, 7, 9, 10, 13, 16, 23] # 15
    file['scene']['kitchen']['objects']['Microwave']['type']['1'] = [2, 3, 4, 5, 6, 11, 17, 18, 19, 20, 21, 22, 25,
                                                                     26, 27, 30] #8, 14

    # spawn range for those type 0 microwaves which are installed over the StoveBurner
    file['scene']['kitchen']['objects']['Microwave']['1'] = [[0.0, 0.2], [[0, 360]]]
    file['scene']['kitchen']['objects']['Microwave']['7'] = [[0.0, 0.2], [[0, 360]]]
    file['scene']['kitchen']['objects']['Microwave']['9'] = [[0.0, 0.3], [[180, 360]]]
    file['scene']['kitchen']['objects']['Microwave']['10'] = [[0.0, 0.2], [[0, 360]]]
    file['scene']['kitchen']['objects']['Microwave']['13'] = [[0.0, 0.2], [[0, 360]]]
    # temporarily remove no.15 since excludedreceptacles doesn't always work
    # file['scene']['kitchen']['object']['Microwave']['15'] = [[0.0, 0.2], [-90, 90]]
    file['scene']['kitchen']['objects']['Microwave']['16'] = [[0.0, 0.2], [[0, 360]]]
    file['scene']['kitchen']['objects']['Microwave']['23'] = [[0.0, 0.2], [[0, 360]]]


    # spawn range for those type 1 microwaves which are placed on the CounterTop
    file['scene']['kitchen']['objects']['Microwave']['2'] = [[0.25, 0.4], [[135, 225]]]
    file['scene']['kitchen']['objects']['Microwave']['3'] = [[0.25, 0.4], [[135, 225]]]
    file['scene']['kitchen']['objects']['Microwave']['4'] = [[0.25, 0.3], [[60, 150]]]
    file['scene']['kitchen']['objects']['Microwave']['5'] = [[0.25, 0.35], [[165, 255]]]
    file['scene']['kitchen']['objects']['Microwave']['6'] = [[0.25, 0.4], [[-45, 45]]]
    # removed, countertop not flat
    # file['scene']['kitchen']['object']['Microwave']['8'] = [[0.2, 0.4], [0, 360]]
    file['scene']['kitchen']['objects']['Microwave']['11'] = [[0.25, 0.35], [[45, 135]]]
    # temporarily remove no.14 since excludedreceptacles doesn't always work
    # file['scene']['kitchen']['objects']['Microwave']['14'] = [[0.2, 0.4], [[135, 225]]]
    file['scene']['kitchen']['objects']['Microwave']['17'] = [[0.25, 0.35], [[-75, 15]]]
    file['scene']['kitchen']['objects']['Microwave']['18'] = [[0.35, 0.45], [[45, 135]]]
    file['scene']['kitchen']['objects']['Microwave']['19'] = [[0.25, 0.35], [[135, 225]]]
    file['scene']['kitchen']['objects']['Microwave']['20'] = [[0.25, 0.35], [[-45, 45]]]
    file['scene']['kitchen']['objects']['Microwave']['21'] = [[0.25, 0.4], [[45, 115]]]
    file['scene']['kitchen']['objects']['Microwave']['22'] = [[0.25, 0.4], [[45, 135]]]
    file['scene']['kitchen']['objects']['Microwave']['25'] = [[0.25, 0.35], [[-45, 45]]]
    file['scene']['kitchen']['objects']['Microwave']['26'] = [[0.25, 0.4], [[90, 135]]]
    file['scene']['kitchen']['objects']['Microwave']['27'] = [[0.25, 0.4], [[-45, 45]]]
    file['scene']['kitchen']['objects']['Microwave']['30'] = [[0.25, 0.35], [[-45, 45]]]


    # spwan range of toaster in x and z-axis, represented by range of distance and angles
    file['scene']['kitchen']['objects']['Toaster'] = {}
    file['scene']['kitchen']['objects']['Toaster']['2'] = [[0.25, 0.4], [[90, 225]]]
    file['scene']['kitchen']['objects']['Toaster']['3'] = [[0.3, 0.5], [[-90, 90]]]
    file['scene']['kitchen']['objects']['Toaster']['4'] = [[0.3, 0.5], [[180, 270]]]
    file['scene']['kitchen']['objects']['Toaster']['5'] = [[0.3, 0.4], [[-45, 45]]]
    file['scene']['kitchen']['objects']['Toaster']['6'] = [[0.3, 0.4], [[-90, 45]]]
    file['scene']['kitchen']['objects']['Toaster']['7'] = [[0.3, 0.5], [[90, 180]]]
    file['scene']['kitchen']['objects']['Toaster']['8'] = [[0.3, 0.5], [[0, 90]]]
    file['scene']['kitchen']['objects']['Toaster']['9'] = [[0.3, 0.5], [[0, 90]]]
    file['scene']['kitchen']['objects']['Toaster']['10'] = [[0.3, 0.4], [[180, 270]]]
    file['scene']['kitchen']['objects']['Toaster']['11'] = [[0.3, 0.5], [[-135, -45]]]
    file['scene']['kitchen']['objects']['Toaster']['12'] = [[0.3, 0.4], [[-90, -45]]]
    file['scene']['kitchen']['objects']['Toaster']['13'] = [[0.3, 0.5], [[-45, 45], [135, 225]]]
    file['scene']['kitchen']['objects']['Toaster']['15'] = [[0.3, 0.5], [[-135, 0]]]
    file['scene']['kitchen']['objects']['Toaster']['16'] = [[0.3, 0.5], [[-45, 45]]]
    file['scene']['kitchen']['objects']['Toaster']['17'] = [[0.3, 0.5], [[-135, -90]]]
    file['scene']['kitchen']['objects']['Toaster']['19'] = [[0.3, 0.5], [[45, 135], [-135, -45]]]
    file['scene']['kitchen']['objects']['Toaster']['20'] = [[0.3, 0.5], [[135, 180]]]
    file['scene']['kitchen']['objects']['Toaster']['21'] = [[0.3, 0.6], [[-180, 0]]]
    file['scene']['kitchen']['objects']['Toaster']['22'] = [[0.3, 0.5], [[-90, 0]]]
    file['scene']['kitchen']['objects']['Toaster']['26'] = [[0.3, 0.5], [[180, 270]]]
    file['scene']['kitchen']['objects']['Toaster']['27'] = [[0.3, 0.5], [[90, 135]]]
    file['scene']['kitchen']['objects']['Toaster']['28'] = [[0.3, 0.5], [[0, 45]]]
    file['scene']['kitchen']['objects']['Toaster']['29'] = [[0.3, 0.5], [[0, 90]]]
    file['scene']['kitchen']['objects']['Toaster']['30'] = [[0.3, 0.4], [[-45, 90]]]


    # spawn range of pan/pot in x and z-axis, represented by range of distance and range of angles
    file['scene']['kitchen']['objects']['Pan'] = {}
    file['scene']['kitchen']['objects']['Pan']['1'] = [[0.15, 0.3], [[0, 180]]]
    file['scene']['kitchen']['objects']['Pan']['2'] = [[0.2, 0.4], [[90, 270]]]
    file['scene']['kitchen']['objects']['Pan']['3'] = [[0.15, 0.3], [[0, 180]]]
    file['scene']['kitchen']['objects']['Pan']['4'] = [[0.15, 0.3], [[0, 180]]]
    file['scene']['kitchen']['objects']['Pan']['5'] = [[0.2, 0.3], [[45, 135], [225, 315]]]
    file['scene']['kitchen']['objects']['Pan']['6'] = [[0.15, 0.3], [[45, 135]]]
    file['scene']['kitchen']['objects']['Pan']['7'] = [[0.17, 0.3], [[-45, 45], [135, 225]]]
    file['scene']['kitchen']['objects']['Pan']['8'] = [[0.17, 0.3], [[0, 180]]]
    file['scene']['kitchen']['objects']['Pan']['9'] = [[0.2, 0.4], [[180, 360]]]
    file['scene']['kitchen']['objects']['Pan']['10'] = [[0.17, 0.35], [[90, 270]]]
    file['scene']['kitchen']['objects']['Pan']['11'] = [[0.15, 0.3], [[-45, 45], [135, 225]]]
    file['scene']['kitchen']['objects']['Pan']['12'] = [[0.2, 0.25], [[45, 135], [225, 315]]]
    file['scene']['kitchen']['objects']['Pan']['13'] = [[0.2, 0.4], [[45, 180]]]
    # temporarily removed since excludedreceptacles doesn't always work
    # file['scene']['kitchen']['objects']['Pan']['14'] = [[0.17, 0.3], [[45, 135]]]
    # file['scene']['kitchen']['objects']['Pan']['15'] = [[0.2, 0.4], [[45, 135], [225, 315]]]
    file['scene']['kitchen']['objects']['Pan']['16'] = [[0.15, 0.25], [[-45, 45], [135, 225]]]
    file['scene']['kitchen']['objects']['Pan']['17'] = [[0.15, 0.3], [[-45, 45]]]
    file['scene']['kitchen']['objects']['Pan']['18'] = [[0.2, 0.35], [[45, 135], [225, 315]]]
    file['scene']['kitchen']['objects']['Pan']['19'] = [[0.2, 0.4], [[90, 270]]]
    file['scene']['kitchen']['objects']['Pan']['20'] = [[0.2, 0.4], [[90, 270]]]
    file['scene']['kitchen']['objects']['Pan']['21'] = [[0.2, 0.4], [[180, 360]]]
    file['scene']['kitchen']['objects']['Pan']['22'] = [[0.25, 0.4], [[-90, 90]]]
    file['scene']['kitchen']['objects']['Pan']['23'] = [[0.2, 0.4], [[0, 180]]]
    file['scene']['kitchen']['objects']['Pan']['24'] = [[0.2, 0.4], [[0, 90]]]
    # file['scene']['kitchen']['objects']['Pan']['25'] = [[0.2, 0.4], [[45, 135], [225, 315]]]
    file['scene']['kitchen']['objects']['Pan']['26'] = [[0.2, 0.4], [[270, 360]]]
    file['scene']['kitchen']['objects']['Pan']['27'] = [[0.2, 0.4], [[45, 135], [225, 315]]]
    file['scene']['kitchen']['objects']['Pan']['28'] = [[0.2, 0.4], [[90, 270]]]
    file['scene']['kitchen']['objects']['Pan']['29'] = [[0.2, 0.3], [[-45, 45], [135, 225]]]
    file['scene']['kitchen']['objects']['Pan']['30'] = [[0.2, 0.4], [[-45, 45], [135, 225]]]

    # list of objects won't be included in the scene
    file['scene']['kitchen']['objects']['remove'] = ['Statue', 'Vase']

    # all objects except large furniture
    file['scene']['kitchen']['objects']['small_objects'] = ['Apple', 'AluminumFoil', 'Book', 'Bottle',
                                                            'Bowl', 'Bread', 'ButterKnife', 'CellPhone',
                                                            'CoffeeMachine', 'CreditCard', 'Cup', 'DishSponge',
                                                            'Egg', 'Fork', 'Kettle', 'Knife', 'Ladle',
                                                            'Lettuce', 'Mirror', 'Mug', 'Pan',
                                                            'PaperTowelRoll', 'Pen', 'Pencil', 'PepperShaker',
                                                            'Plate', 'Pot', 'Potato', 'SaltShaker',
                                                            'SoapBottle', 'Spatula', 'Spoon', 'SprayBottle',
                                                            'Toaster', 'Tomato', 'WineBottle']

    # all furniture objects
    file['scene']['kitchen']['objects']['large_objects'] = ['Blinds', 'Cabinet', 'Chair', 'CounterTop',
                                                            'Curtains', 'DiningTable', 'Drawer', 'Faucet',
                                                            'Floor', 'Fridge', 'GarbageBag', 'GarbageCan',
                                                            'HousePlant', 'LightSwitch', 'Microwave', 'Safe',
                                                            'Shelf', 'ShelvingUnit', 'SideTable', 'Sink',
                                                            'SinkBasin', 'Stool', 'StoveBurner', 'StoveKnob',
                                                            'Window']

    #############################
    # Natural language template #
    #############################
    file['natural_language'] = {}
    # complete task command
    file['natural_language']['complete'] = {}
    file['natural_language']['complete']['Microwave'] = []
    file['natural_language']['complete']['Microwave'].append('Open the microwave, grasp the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Open the microwave, grab the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Open the microwave, pick the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Open the microwave, catch the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Open the microwave, grasp the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Open the microwave, grab the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Open the microwave, pick the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Open the microwave, catch the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Please open the microwave, grasp the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Please open the microwave, grab the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Please open the microwave, pick the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Please open the microwave, catch the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Please open the microwave, grasp the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Please open the microwave, grab the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Please open the microwave, pick the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Please open the microwave, catch the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Help me open the microwave, grasp the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Help me open the microwave, grab the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Help me open the microwave, pick the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Help me open the microwave, catch the obj2, '
                                                             'place the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Help me open the microwave, grasp the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Help me open the microwave, grab the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Help me open the microwave, pick the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')
    file['natural_language']['complete']['Microwave'].append('Help me open the microwave, catch the obj2, '
                                                             'put the obj2 in the microwave, '
                                                             'close the microwave and turn the microwave on.')

    file['natural_language']['complete']['StoveBurner'] = []
    file['natural_language']['complete']['StoveBurner'].append('Grasp the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Grab the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Pick the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Catch the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Grasp the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Grab the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Pick the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Catch the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Please grasp the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Please grab the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Please pick the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Please catch the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Please grasp the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Please grab the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Please pick the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Please catch the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Help me grasp the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Help me grab the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Help me pick the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Help me catch the obj2, place the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Help me grasp the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Help me grab the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Help me pick the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')
    file['natural_language']['complete']['StoveBurner'].append('Help me catch the obj2, put the obj2 in the pan and '
                                                               'turn the stove burner on.')

    file['natural_language']['complete']['Toaster'] = []
    file['natural_language']['complete']['Toaster'].append('Grasp the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Grab the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Pick the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Catch the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Grasp the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Grab the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Pick the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Catch the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Please grasp the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Please grab the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Please pick the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Please catch the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Please grasp the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Please grab the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Please pick the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Please catch the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Help me grasp the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Help me grab the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Help me pick the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Help me catch the obj2, place the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Help me grasp the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Help me grab the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Help me pick the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    file['natural_language']['complete']['Toaster'].append('Help me catch the obj2, put the obj2 in the toaster and '
                                                           'turn the toaster on.')
    # file['natural_language']['complete']['StoveBurner'].append('Grasp the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Grab the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Pick the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Catch the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Grasp the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Grab the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Pick the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Catch the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Please grasp the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Please grab the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Please pick the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Please catch the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Please grasp the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Please grab the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Please pick the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Please catch the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Help me grasp the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Help me grab the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Help me pick the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Help me catch the obj2, place the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Help me grasp the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Help me grab the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Help me pick the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')
    # file['natural_language']['complete']['StoveBurner'].append('Help me catch the obj2, put the obj2 in the StoveBurner and '
    #                                                            'turn the StoveBurner on.')

    # incomplete task command
    file['natural_language']['incomplete'] = {}
    file['natural_language']['incomplete']['Microwave'] = []
    file['natural_language']['incomplete']['Microwave'].append('Cook the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Make the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Microwave the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Heat the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Please cook the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Please make the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Please microwave the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Please heat the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Help me cook the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Help me make the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Help me microwave the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Help me heat the obj2.')
    file['natural_language']['incomplete']['Microwave'].append('Open the microwave, grasp the obj2, '
                                                               'place it in the microwave, '
                                                               'close the microwave and turn it on.')
    file['natural_language']['incomplete']['Microwave'].append('Open the microwave, grab the obj2, '
                                                               'place it in the microwave, c'
                                                               'lose the microwave and turn it on.')
    file['natural_language']['incomplete']['Microwave'].append('Open the microwave, pick the obj2, '
                                                               'place it in the microwave, '
                                                               'close the microwave and turn it on.')
    file['natural_language']['incomplete']['Microwave'].append('Open the microwave, catch the obj2, '
                                                               'place it in the microwave, '
                                                               'close the microwave and turn it on.')
    file['natural_language']['incomplete']['Microwave'].append('Open the microwave, grasp the obj2, '
                                                               'put it in the microwave, '
                                                               'close the microwave and turn it on.')
    file['natural_language']['incomplete']['Microwave'].append('Open the microwave, grab the obj2, '
                                                               'put it in the microwave, '
                                                               'close the microwave and turn it on.')
    file['natural_language']['incomplete']['Microwave'].append('Open the microwave, pick the obj2, '
                                                               'put it in the microwave, '
                                                               'close the microwave and turn it on.')
    file['natural_language']['incomplete']['Microwave'].append('Open the microwave, catch the obj2, '
                                                               'put it in the microwave, '
                                                               'close the microwave and turn it on.')

    file['natural_language']['incomplete']['Microwave'].append('Place the obj2 in the microwave and cook it.')
    file['natural_language']['incomplete']['Microwave'].append('Put the obj2 in the microwave and cook it.')
    file['natural_language']['incomplete']['Microwave'].append('Place the obj2 in the microwave and make it.')
    file['natural_language']['incomplete']['Microwave'].append('Put the obj2 in the microwave and make it.')
    file['natural_language']['incomplete']['Microwave'].append('Place the obj2 in the microwave and heat it.')
    file['natural_language']['incomplete']['Microwave'].append('Put the obj2 in the microwave and heat it.')
    file['natural_language']['incomplete']['Microwave'].append('Please place the obj2 in the microwave and cook it.')
    file['natural_language']['incomplete']['Microwave'].append('Please put the obj2 in the microwave and cook it.')
    file['natural_language']['incomplete']['Microwave'].append('Please place the obj2 in the microwave and make it.')
    file['natural_language']['incomplete']['Microwave'].append('Please put the obj2 in the microwave and make it.')
    file['natural_language']['incomplete']['Microwave'].append('Please place the obj2 in the microwave and heat it.')
    file['natural_language']['incomplete']['Microwave'].append('Please put the obj2 in the microwave and heat it.')
    file['natural_language']['incomplete']['Microwave'].append('Help me place the obj2 in the microwave and cook it.')
    file['natural_language']['incomplete']['Microwave'].append('Help me put the obj2 in the microwave and cook it.')
    file['natural_language']['incomplete']['Microwave'].append('Help me place the obj2 in the microwave and make it.')
    file['natural_language']['incomplete']['Microwave'].append('Help me put the obj2 in the microwave and make it.')
    file['natural_language']['incomplete']['Microwave'].append('Help me place the obj2 in the microwave and heat it.')
    file['natural_language']['incomplete']['Microwave'].append('Help me put the obj2 in the microwave and heat it.')

    file['natural_language']['incomplete']['StoveBurner'] = []
    file['natural_language']['incomplete']['StoveBurner'].append('Cook the obj2.')
    file['natural_language']['incomplete']['StoveBurner'].append('Make the obj2.')
    file['natural_language']['incomplete']['StoveBurner'].append('Heat the obj2.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please cook the obj2.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please make the obj2.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please heat the obj2.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me cook the obj2.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me make the obj2.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me heat the obj2.')
    file['natural_language']['incomplete']['StoveBurner'].append('Grasp the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Grab the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Pick the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Catch the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please grasp the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please grab the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please pick the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please catch the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me grasp the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me grab the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me pick the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me catch the obj2, place it in the pan and '
                                                                 'turn the stove burner on.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Grasp the obj2, place it in the stoveburner and '
    #                                                              'turn it on.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Grab the obj2, place it in the stoveburner and '
    #                                                              'turn it on.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Pick the obj2, place it in the stoveburner and '
    #                                                              'turn it on.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Catch the obj2, place it in the stoveburner and '
    #                                                              'turn it on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Grasp the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Grab the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Pick the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Catch the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please grasp the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please grab the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please pick the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please catch the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me grasp the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me grab the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me pick the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me catch the obj2, put it in the pan and '
                                                                 'turn the stove burner on.')
    file['natural_language']['incomplete']['StoveBurner'].append('Place the obj2 in the pan and cook it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Put the obj2 in the pan and cook it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Place the obj2 in the pan and make it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Put the obj2 in the pan and make it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Place the obj2 in the pan and heat it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Put the obj2 in the pan and heat it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please place the obj2 in the pan and cook it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please put the obj2 in the pan and cook it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please place the obj2 in the pan and make it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please put the obj2 in the pan and make it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please place the obj2 in the pan and heat it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Please put the obj2 in the pan and heat it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me place the obj2 in the pan and cook it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me put the obj2 in the pan and cook it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me place the obj2 in the pan and make it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me put the obj2 in the pan and make it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me place the obj2 in the pan and heat it.')
    file['natural_language']['incomplete']['StoveBurner'].append('Help me put the obj2 in the pan and heat it.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Grasp the obj2, put it in the stoveburner and turn it on.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Grab the obj2, put it in the stoveburner and turn it on.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Pick the obj2, put it in the stoveburner and turn it on.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Catch the obj2, put it in the stoveburner and turn it on.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Place the obj2 in the stoveburner and cook it.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Put the obj2 in the stoveburner and cook it.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Place the obj2 in the stoveburner and make it.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Put the obj2 in the stoveburner and make it.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Place the obj2 in the stoveburner and heat it.')
    # file['natural_language']['incomplete']['StoveBurner'].append('Put the obj2 in the stoveburner and heat it.')

    file['natural_language']['incomplete']['Toaster'] = []
    file['natural_language']['incomplete']['Toaster'].append('Cook the obj2.')
    file['natural_language']['incomplete']['Toaster'].append('Make the obj2.')
    file['natural_language']['incomplete']['Toaster'].append('Heat the obj2.')
    file['natural_language']['incomplete']['Toaster'].append('Please cook the obj2.')
    file['natural_language']['incomplete']['Toaster'].append('Please make the obj2.')
    file['natural_language']['incomplete']['Toaster'].append('Please heat the obj2.')
    file['natural_language']['incomplete']['Toaster'].append('Help me cook the obj2.')
    file['natural_language']['incomplete']['Toaster'].append('Help me make the obj2.')
    file['natural_language']['incomplete']['Toaster'].append('Help me heat the obj2.')
    file['natural_language']['incomplete']['Toaster'].append('Grasp the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Grab the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Pick the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Catch the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Please grasp the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Please grab the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Please pick the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Please catch the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Help me grasp the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Help me grab the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Help me pick the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Help me catch the obj2, place it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Grasp the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Grab the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Pick the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Catch the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Please grasp the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Please grab the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Please pick the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Please catch the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Help me grasp the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Help me grab the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Help me pick the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Help me catch the obj2, put it in the toaster and '
                                                             'turn the toaster on.')
    file['natural_language']['incomplete']['Toaster'].append('Place the obj2 in the toaster and cook it.')
    file['natural_language']['incomplete']['Toaster'].append('Put the obj2 in the toaster and cook it.')
    file['natural_language']['incomplete']['Toaster'].append('Place the obj2 in the toaster and make it.')
    file['natural_language']['incomplete']['Toaster'].append('Put the obj2 in the toaster and make it.')
    file['natural_language']['incomplete']['Toaster'].append('Place the obj2 in the toaster and heat it.')
    file['natural_language']['incomplete']['Toaster'].append('Put the obj2 in the toaster and heat it.')
    file['natural_language']['incomplete']['Toaster'].append('Please place the obj2 in the toaster and cook it.')
    file['natural_language']['incomplete']['Toaster'].append('Please put the obj2 in the toaster and cook it.')
    file['natural_language']['incomplete']['Toaster'].append('Please place the obj2 in the toaster and make it.')
    file['natural_language']['incomplete']['Toaster'].append('Please put the obj2 in the toaster and make it.')
    file['natural_language']['incomplete']['Toaster'].append('Please place the obj2 in the toaster and heat it.')
    file['natural_language']['incomplete']['Toaster'].append('Please put the obj2 in the toaster and heat it.')
    file['natural_language']['incomplete']['Toaster'].append('Help me place the obj2 in the toaster and cook it.')
    file['natural_language']['incomplete']['Toaster'].append('Help me put the obj2 in the toaster and cook it.')
    file['natural_language']['incomplete']['Toaster'].append('Help me place the obj2 in the toaster and make it.')
    file['natural_language']['incomplete']['Toaster'].append('Help me put the obj2 in the toaster and make it.')
    file['natural_language']['incomplete']['Toaster'].append('Help me place the obj2 in the toaster and heat it.')
    file['natural_language']['incomplete']['Toaster'].append('Help me put the obj2 in the toaster and heat it.')

    # implicit task description
    file['natural_language']['implicit'] = {}
    file['natural_language']['implicit']['Microwave'] = []
    file['natural_language']['implicit']['Microwave'].append('I want cooked obj2.')
    file['natural_language']['implicit']['Microwave'].append('I really want cooked obj2.')
    file['natural_language']['implicit']['Microwave'].append('I am hungry and want to have obj2.')
    file['natural_language']['implicit']['Microwave'].append('I am starved and want to have obj2.')
    file['natural_language']['implicit']['Microwave'].append('I am hungry and want to eat obj2.')
    file['natural_language']['implicit']['Microwave'].append('I am starved and want to eat obj2.')

    file['natural_language']['implicit']['StoveBurner'] = []
    file['natural_language']['implicit']['StoveBurner'].append('I want cooked obj2.')
    file['natural_language']['implicit']['StoveBurner'].append('I really want cooked obj2.')
    file['natural_language']['implicit']['StoveBurner'].append('I am hungry and want to have obj2.')
    file['natural_language']['implicit']['StoveBurner'].append('I am starved and want to have obj2.')
    file['natural_language']['implicit']['StoveBurner'].append('I am hungry and want to eat obj2.')
    file['natural_language']['implicit']['StoveBurner'].append('I am starved and want to eat obj2.')

    file['natural_language']['implicit']['Toaster'] = []
    file['natural_language']['implicit']['Toaster'].append('I want cooked obj2.')
    file['natural_language']['implicit']['Toaster'].append('I really want cooked obj2.')
    file['natural_language']['implicit']['Toaster'].append('I am hungry and want to have obj2.')
    file['natural_language']['implicit']['Toaster'].append('I am starved and want to have obj2.')
    file['natural_language']['implicit']['Toaster'].append('I am hungry and want to eat obj2.')
    file['natural_language']['implicit']['Toaster'].append('I am starved and want to eat obj2.')

    with open(os.path.join(args.save_path, 'task_description.json'), 'w') as json_file:
      json.dump(file, json_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('save_path', type=str, default='../data/official/cook_task', help='Root directory for data')
    args = parser.parse_args()

    main(args)
