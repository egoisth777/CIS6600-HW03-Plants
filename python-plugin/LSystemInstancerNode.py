# randomNode.py
#   Produces random locations to be used with the Maya instancer node.

import sys
import LSystem
from math import sqrt

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds


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
kPluginNodeTypeName = "LSystemInstancerNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
instancerNodeId = OpenMaya.MTypeId(0x8705)


# Node definition
class LSystemInstancerNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()
    iterations = OpenMaya.MObject()
    angle = OpenMaya.MObject()
    step_size = OpenMaya.MObject()
    syntax = OpenMaya.MObject()

    # Output
    gen_branches = OpenMaya.MObject()
    gen_flowers = OpenMaya.MObject()

    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self, plug, data):
        OpenMaya.MGlobal.displayInfo("Computing Lsystem Node")

        data.setClean(plug)


# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # TODO:: initialize the input and output attributes. Be sure to use the
    #         MAKE_INPUT and MAKE_OUTPUT functions.
    # initializing the input data types
    LSystemInstancerNode.iterations = nAttr.create("iterations", "i", OpenMaya.MFnNumericData.kInt, 1)
    LSystemInstancerNode.angle = nAttr.create("angle", "a", OpenMaya.MFnNumericData.kFloat, 45.0)
    LSystemInstancerNode.step_size = nAttr.create("step_size", "ss", OpenMaya.MFnNumericData.kFloat, 1.6)
    syntax_path = "E:\\MayaProjects\\CIS660-HW03-MayaPySWIG\\plants\\flower_grammar_1.txt"
    LSystemInstancerNode.syntax = tAttr.create("grammar", "g", OpenMaya.MFnData.kString,
                                               OpenMaya.MFnStringData.create(syntax_path))
    MAKE_INPUT(nAttr)

    # initializing the output data types
    LSystemInstancerNode.gen_branches = tAttr.create("branches", "obr", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    LSystemInstancerNode.gen_flowers = tAttr.create("flowers", "ofl", OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)
    try:  # @TODO Add the attributes to the node and set up the attribute
        print("Initialization!")
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.iterations)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.step_size)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.syntax)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.angle_deg)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.gen_branches)
        LSystemInstancerNode.addAttribute(LSystemInstancerNode.gen_flowers)

        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.iterations, LSystemInstancerNode.gen_branches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.iterations, LSystemInstancerNode.gen_flowers)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.step_size, LSystemInstancerNode.gen_branches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.step_size, LSystemInstancerNode.gen_flowers)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.syntax, LSystemInstancerNode.gen_branches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.syntax, LSystemInstancerNode.gen_flowers)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.angle_deg, LSystemInstancerNode.gen_branches)
        LSystemInstancerNode.attributeAffects(LSystemInstancerNode.angle_deg, LSystemInstancerNode.gen_flowers)
    except:
        sys.stderr.write(("Failed to create attributes of %s node\n", kPluginNodeTypeName))


# creator
# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( LSystemInstancerNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, instancerNodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

    # mel_path = mplugin.loadPath() + "/menu_opts.mel"
    # with open(mel_path, "r") as file:
    #     mel_script = file.read()
    # OpenMaya.MGlobal.executeCommand(mel_script)

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( instancerNodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )
