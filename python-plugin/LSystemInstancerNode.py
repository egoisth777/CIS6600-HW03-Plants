import sys
import random
import LSystem
from math import sqrt
import maya.cmds as cmds

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

import inspect
import os
# Set the Plugin directory
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
kPluginNodeTypeName = "LSystemInstancerNode"

# Give the node a unique ID. Make sure this ID is different from all of your
# other nodes!
nodeId = OpenMaya.MTypeId(0x8705)

# Node definition
class LSystemInstancerNode(OpenMayaMPx.MPxNode):
    # Declare class variables:
    # TODO:: declare the input and output class variables
    #         i.e. inNumPoints = OpenMaya.MObject()
    iterations=OpenMaya.MObject()
    step_size=OpenMaya.MObject()
    syntax=OpenMaya.MObject()
    angle_deg=OpenMaya.MObject()
    gen_branches=OpenMaya.MObject()
    gen_flowers=OpenMaya.MObject()
    # constructor
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    # compute
    def compute(self,plug,data):

        OpenMaya.MGlobal.displayInfo("Computing lsystem node")
        if plug==LSystemInstancerNode.gen_branches or plug==LSystemInstancerNode.gen_flowers:
            curr_iter=data.inputValue(LSystemInstancerNode.iterations).asInt()
            curr_step=data.inputValue(LSystemInstancerNode.step_size).asFloat()
            curr_syntax=data.inputValue(LSystemInstancerNode.syntax).asString()
            curr_angle=data.inputValue(LSystemInstancerNode.angle_deg).asFloat()

            genBranchesData=data.outputValue(LSystemInstancerNode.gen_branches)
            genBranchesAAD=OpenMaya.MFnArrayAttrsData()
            genBranchesObject=genBranchesAAD.create()
            branchesPositionArray=genBranchesAAD.vectorArray("position")
            branchesAimDArray=genBranchesAAD.vectorArray("aimDirection")
            branchesScaleArr=genBranchesAAD.vectorArray("scale")
            branchesIdArray=genBranchesAAD.doubleArray("id")
            genFlowersData=data.outputValue(LSystemInstancerNode.gen_flowers)
            genFlowersAAD=OpenMaya.MFnArrayAttrsData()
            genFlowersObject=genFlowersAAD.create()
            flowersPositionArray=genFlowersAAD.vectorArray("position")
            flowersIdArray=genFlowersAAD.doubleArray("id")

            lsystem=LSystem.LSystem()
            lsystem.loadProgram(str(curr_syntax))
            lsystem.setDefaultAngle(curr_angle)
            lsystem.setDefaultStep(curr_step)
            branches=LSystem.VectorPyBranch()
            flowers=LSystem.VectorPyBranch()
            OpenMaya.MGlobal.displayInfo("Num branches:"+str(len(branches)))
            OpenMaya.MGlobal.displayInfo("Num flowers:"+str(len(flowers)))
            lsystem.processPy(curr_iter, branches, flowers)
            for i in range(len(branches)):
                x0=(branches[i][0],branches[i][1],branches[i][2])
                x1=(branches[i][3],branches[i][4],branches[i][5])
                pos=get_mid_point(x0,x1)
                dir=get_dir(x0,x1)
                dist=get_dist(x0,x1)
                branchesIdArray.append(i)
                branchesPositionArray.append(pos)
                branchesAimDArray.append(dir)
                branchesScaleArr.append(OpenMaya.MVector(dist, 1, 1))

            for i in range(len(flowers)):
                pos = OpenMaya.MVector(flowers[i][0], flowers[i][1], flowers[i][2])
                flowersPositionArray.append(pos)
                flowersIdArray.append(i)

            genBranchesData.setMObject(genBranchesObject)
            genFlowersData.setMObject(genFlowersObject)


        data.setClean(plug)

def get_dir(x0,x1):
    return OpenMaya.MVector(x1[0]-x0[0],x1[1]-x0[1],x1[2]-x0[2])

def get_mid_point(x0,x1):
    return OpenMaya.MVector((x1[0]+x0[0])*0.5,(x1[1]+x0[1])*0.5,(x1[2]+x0[2])*0.5)

def get_dist(x0,x1):
    v=(x1[0]-x0[0],x1[1]-x0[1],x1[2]-x0[2])
    return sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])

# initializer
def nodeInitializer():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    # TODO:: initialize the input and output attributes. Be sure to use the
    #         MAKE_INPUT and MAKE_OUTPUT functions.
    LSystemInstancerNode.iterations=nAttr.create("iterations", "i", OpenMaya.MFnNumericData.kInt, 5)
    LSystemInstancerNode.step_size=nAttr.create("step_size", "ss", OpenMaya.MFnNumericData.kFloat, 1.62)
    syntax_path = plugin_dir + "/flower_grammar_1.txt"
    OpenMaya.MGlobal.displayInfo(syntax_path)
    LSystemInstancerNode.syntax=tAttr.create("grammar", "gram", OpenMaya.MFnData.kString, OpenMaya.MFnStringData().create(syntax_path))
    LSystemInstancerNode.angle_deg=nAttr.create("angle", "a", OpenMaya.MFnNumericData.kFloat, 45.0)
    MAKE_INPUT(nAttr)
    LSystemInstancerNode.gen_branches=tAttr.create("outBranches", "obr",  OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    LSystemInstancerNode.gen_flowers=tAttr.create("outFlowers", "ofl",  OpenMaya.MFnArrayAttrsData.kDynArrayAttrs)
    MAKE_OUTPUT(tAttr)

    try:
        # TODO:: add the attributes to the node and set up the
        #         attributeAffects (addAttribute, and attributeAffects)
        print("Initialization!\n")
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
        sys.stderr.write( ("Failed to create attributes of %s node\n", kPluginNodeTypeName) )

# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr( LSystemInstancerNode() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeTypeName, nodeId, nodeCreator, nodeInitializer )
    except:
        sys.stderr.write( "Failed to register node: %s\n" % kPluginNodeTypeName )

    mel_path = mplugin.loadPath() + "/menu_opts.mel"
    with open(mel_path, "r") as file:
        mel_script = file.read()
    OpenMaya.MGlobal.executeCommand(mel_script)

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)

    # Remove the menu by its unique name (LSystemInstanceMenu).
    OpenMaya.MGlobal.executeCommand('if (`menu -exists "LSystemInstanceMenu"`) deleteUI "LSystemInstanceMenu";')
    try:
        OpenMaya.MGlobal.executeCommand('delete `ls -type "LSystemInstancerNode"`;')
        mplugin.deregisterNode( nodeId )
    except:
        sys.stderr.write( "Failed to unregister node: %s\n" % kPluginNodeTypeName )