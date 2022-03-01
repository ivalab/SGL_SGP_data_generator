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

    # included floorplan
    file['scene']['kitchen']['floorplan'] = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                             '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                             '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']

    ## excluded receptacles
    ex_receptacles = ['Bowl', 'Plate', 'Pan', 'Pot', 'Shelf', 'Sink', 'SinkBasin', 'Cabinet',
                      'Fridge', 'Drawer', 'GarbageCan']
    file['scene']['kitchen']['excluded_receptacles'] = ex_receptacles
    ## objects
    obj_pick = ['Apple', 'Bread', 'Egg', 'Lettuce', 'Potato', 'Tomato']
    obj_place = ['Bowl', 'Plate', 'Pan', 'Pot']
    file['scene']['kitchen']['objects'] = {}
    file['scene']['kitchen']['objects']['pick'] = obj_pick
    file['scene']['kitchen']['objects']['place'] = obj_place

    ## all labels for object category, affordance and general attribute
    file['labels'] = {}
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


    # list of objects won't be included in the scene
    file['scene']['kitchen']['objects']['remove'] = ['Statue', 'Vase']

    # radius of place object for avoiding overlapping
    file['scene']['kitchen']['objects']['radius'] = {}
    file['scene']['kitchen']['objects']['radius']['Bowl'] = 0.15
    file['scene']['kitchen']['objects']['radius']['Plate'] = 0.15
    file['scene']['kitchen']['objects']['radius']['Pan'] = 0.25
    file['scene']['kitchen']['objects']['radius']['Pot'] = 0.25

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
    file['natural_language']['complete'] = []
    file['natural_language']['complete'].append('Pick the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Grab the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Grasp the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Catch the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Pick the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Grab the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Grasp the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Catch the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Please pick the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Please grab the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Please grasp the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Please catch the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Please pick the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Please grab the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Please grasp the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Please catch the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Help me pick the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Help me grab the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Help me grasp the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Help me catch the obj1 and place the obj1 in the obj2.')
    file['natural_language']['complete'].append('Help me pick the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Help me grab the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Help me grasp the obj1 and put the obj1 in the obj2.')
    file['natural_language']['complete'].append('Help me catch the obj1 and put the obj1 in the obj2.')
    # incomplete task command
    file['natural_language']['incomplete'] = []
    file['natural_language']['incomplete'].append('Pick the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Grab the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Grasp the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Catch the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Pick the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Grab the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Grasp the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Catch the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Please pick the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Please grab the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Please grasp the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Please catch the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Please pick the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Please grab the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Please grasp the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Please catch the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Help me pick the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Help me grab the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Help me grasp the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Help me catch the obj1 and place it in the obj2.')
    file['natural_language']['incomplete'].append('Help me pick the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Help me grab the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Help me grasp the obj1 and put it in the obj2.')
    file['natural_language']['incomplete'].append('Help me catch the obj1 and put it in the obj2.')

    file['natural_language']['incomplete'].append('Move the obj1 to the obj2.')
    file['natural_language']['incomplete'].append('Relocate the obj1 to the obj2.')
    file['natural_language']['incomplete'].append('Please move the obj1 to the obj2.')
    file['natural_language']['incomplete'].append('Please relocate the obj1 to the obj2.')
    file['natural_language']['incomplete'].append('Help me move the obj1 to the obj2.')
    file['natural_language']['incomplete'].append('Help me relocate the obj1 to the obj2.')

    file['natural_language']['incomplete'].append('Put the obj1 in the obj2.')
    file['natural_language']['incomplete'].append('Place the obj1 in the obj2.')
    file['natural_language']['incomplete'].append('Please put the obj1 in the obj2.')
    file['natural_language']['incomplete'].append('Please place the obj1 in the obj2.')
    file['natural_language']['incomplete'].append('Help me put the obj1 in the obj2.')
    file['natural_language']['incomplete'].append('Help me place the obj1 in the obj2.')

    file['natural_language']['incomplete'].append('Use obj2 to contain the obj1.')
    file['natural_language']['incomplete'].append('Please use obj2 to contain the obj1.')
    file['natural_language']['incomplete'].append('Help me use obj2 to contain the obj1.')
    # implicit task description
    # file['natural_language']['implicit'] = []
    # file['natural_language']['implicit'].append('The obj2 is unwashed and requires to be cleaned up.')

    with open(os.path.join(args.save_path, 'task_description.json'), 'w') as json_file:
      json.dump(file, json_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('save_path', type=str, default='../data/official/pick_n_place', help='Root directory for data')
    args = parser.parse_args()

    main(args)