# randomNode.py
#   Produces random locations to be used with the Maya instancer node.
import os
import sys

import random

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import inspect

import inspect
import sys
try:
    plugin_path = os.path.abspath(inspect.getsourcefile(lambda: 0))
    plugin_dir = os.path.dirname(plugin_path)
    OpenMaya.MGlobal.displayInfo("Plugin directory: " + plugin_dir)
except Exception as e:
    OpenMaya.MGlobal.displayError("Failed to determine plugin directory: " + str(e))
    plugin_dir = os.getcwd()  # fallback; likely not what you want

if plugin_dir not in sys.path:
    sys.path.insert(0, plugin_dir)

# Useful functions for declaring attributes as inputs or outputs.
def MAKE_INPUT(attr):
    attr.setKeyable(True)
    attr.setStorable(True)
    attr.setReadable(True)
    attr.setWritable(True)
def MAKE_OUTPUT(attr):
    attr.setKeyable(False)
    attr.setStorable(False)
    attr.setReadable(True)
    attr.setWritable(False)

# Define the name of the node
kPluginNodeTypeName = "randomNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
randomNodeId = OpenMaya.MTypeId(0x8704)

# Node definition
class randomNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()
    inNumPoints = OpenMaya.MObject()
    min_x = OpenMaya.MObject()
    max_x = OpenMaya.MObject()
    min_y = OpenMaya.MObject()
    max_y = OpenMaya.MObject()
    min_z = OpenMaya.MObject()
    max_z = OpenMaya.MObject()
    gen_points = OpenMaya.MObject()
    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self,plug,data):
        # TODO:: create the main functionality of the node. Your node should
        #         take in three floats for max position (X,Y,Z), three floats
        #         for min position (X,Y,Z), and the number of random points to
        #         be generated. Your node should output an MFnArrayAttrsData
        #         object containing the random points. Consult the homework
        #         sheet for how to deal with creating the MFnArrayAttrsData.
        if plug==randomNode.gen_points:
            curr_inNumPoints = data.inputValue(randomNode.inNumPoints).asInt()
            curr_min_x = data.inputValue(randomNode.min_x).asFloat()
            curr_max_x = data.inputValue(randomNode.max_x).asFloat()
            curr_min_y = data.inputValue(randomNode.min_y).asFloat()
            curr_max_y = data.inputValue(randomNode.max_y).asFloat()
            curr_min_z = data.inputValue(randomNode.min_z).asFloat()
            curr_max_z = data.inputValue(randomNode.max_z).asFloat()

            pointsData = data.outputValue(randomNode.gen_points)
            pointsAAD = OpenMaya.MFnArrayAttrsData()
            pointsObject = pointsAAD.create()
            positionArray = pointsAAD.vectorArray("position")
            idArray = pointsAAD.doubleArray("id")

            for i in range(0, curr_inNumPoints):
                x = random.uniform(curr_min_x, curr_max_x)
                y = random.uniform(curr_min_y, curr_max_y)
                z = random.uniform(curr_min_z, curr_max_z)
                pos = OpenMaya.MVector(x, y, z)
                positionArray.append(pos)
                idArray.append(i)
            pointsData.setMObject(pointsObject)

        data.setClean(plug)

# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # TODO:: initialize the input and output attributes. Be sure to use the
    #         MAKE_INPUT and MAKE_OUTPUT functions.
    randomNode.inNumPoints=nAttr.create("inNumPoints","npts",OpenMaya.MFnNumericData.kInt,8)
    randomNode.min_x=nAttr.create("min_x","mnx",OpenMaya.MFnNumericData.kFloat,-5.0)
    randomNode.max_x=nAttr.create("max_x","mxx",OpenMaya.MFnNumericData.kFloat,5.0)
    randomNode.min_y=nAttr.create("min_y","mny",OpenMaya.MFnNumericData.kFloat,-5.0)
    randomNode.max_y=nAttr.create("max_y","mxy",OpenMaya.MFnNumericData.kFloat,5.0)
    randomNode.min_z=nAttr.create("min_z","mnz",OpenMaya.MFnNumericData.kFloat,-5.0)
    randomNode.max_z=nAttr.create("max_z","mxz",OpenMaya.MFnNumericData.kFloat,5.0)
    MAKE_INPUT(nAttr)
    randomNode.gen_points=tAttr.create("outPoints","opts",OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        print("Initialization!\n")
        randomNode.addAttribute(randomNode.inNumPoints)
        randomNode.addAttribute(randomNode.min_x)
        randomNode.addAttribute(randomNode.max_x)
        randomNode.addAttribute(randomNode.min_y)
        randomNode.addAttribute(randomNode.max_y)
        randomNode.addAttribute(randomNode.min_z)
        randomNode.addAttribute(randomNode.max_z)
        randomNode.addAttribute(randomNode.gen_points)
        randomNode.attributeAffects(randomNode.inNumPoints,randomNode.gen_points)
        randomNode.attributeAffects(randomNode.min_x,randomNode.gen_points)
        randomNode.attributeAffects(randomNode.max_x,randomNode.gen_points)
        randomNode.attributeAffects(randomNode.min_y,randomNode.gen_points)
        randomNode.attributeAffects(randomNode.max_y,randomNode.gen_points)
        randomNode.attributeAffects(randomNode.min_z,randomNode.gen_points)
        randomNode.attributeAffects(randomNode.max_z,randomNode.gen_points)
    except:
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( randomNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, randomNodeId, nodeCreator, nodeInitializer )
    except Exception as e:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )
        raise e

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( randomNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
