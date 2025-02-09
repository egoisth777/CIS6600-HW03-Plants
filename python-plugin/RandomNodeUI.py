"""
randomNodeUI.py

A PyQt (PySide2) based GUI for creating a randomNode and an associated instancer.
This tool allows the user to select an object to instance, choose the number of instances,
set min/max bounds for X, Y, and Z, and then create/connect the nodes.
"""
from re import error

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import sys

# Try to import PySide2 (for Maya 2017+). If not available, fallback to PySide.
try:
    from PySide2 import QtWidgets, QtCore, QtGui
    from shiboken2 import wrapInstance
except Exception as e:
    sys.stderr.write("Warning: Failed to import PySide2. Falling back to PySide.\n")
    raise e

def get_maya_main_window():
    """Return the Maya main window widget as a Python object."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    # In Python 2, you might need to use long(main_window_ptr)
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class RandomNodeUI(QtWidgets.QDialog):
    def __init__(self, parent=get_maya_main_window()):
        super(RandomNodeUI, self).__init__(parent)

        self.setWindowTitle("Random Node Creator")
        # Optional: Make the window a tool window (keeps it on top of Maya)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(350, 300)

        # Store the selected object name (to instance) here.
        self.selected_object = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        # --- Widget to record selected object ---
        self.selectObjButton = QtWidgets.QPushButton("Select Object")
        self.selectedObjLabel = QtWidgets.QLabel("No object selected")
        self.selectedObjLabel.setStyleSheet("color: red;")

        # --- Widget for number of points ---
        self.numPointsLabel = QtWidgets.QLabel("Number of Points:")
        self.numPointsSpin = QtWidgets.QSpinBox()
        self.numPointsSpin.setRange(1, 1000)
        self.numPointsSpin.setValue(8)  # default as in plugin

        # --- Widgets for bounds ---
        # For each axis, create a pair of double spin boxes.
        self.min_x_spin = QtWidgets.QDoubleSpinBox()
        self.min_x_spin.setRange(-1000.0, 1000.0)
        self.min_x_spin.setValue(-5.0)
        self.max_x_spin = QtWidgets.QDoubleSpinBox()
        self.max_x_spin.setRange(-1000.0, 1000.0)
        self.max_x_spin.setValue(5.0)

        self.min_y_spin = QtWidgets.QDoubleSpinBox()
        self.min_y_spin.setRange(-1000.0, 1000.0)
        self.min_y_spin.setValue(-5.0)
        self.max_y_spin = QtWidgets.QDoubleSpinBox()
        self.max_y_spin.setRange(-1000.0, 1000.0)
        self.max_y_spin.setValue(5.0)

        self.min_z_spin = QtWidgets.QDoubleSpinBox()
        self.min_z_spin.setRange(-1000.0, 1000.0)
        self.min_z_spin.setValue(-5.0)
        self.max_z_spin = QtWidgets.QDoubleSpinBox()
        self.max_z_spin.setRange(-1000.0, 1000.0)
        self.max_z_spin.setValue(5.0)

        # --- Button to create the random node ---
        self.createNodeButton = QtWidgets.QPushButton("Create Random Node")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # --- Selection layout ---
        select_layout = QtWidgets.QHBoxLayout()
        select_layout.addWidget(self.selectObjButton)
        select_layout.addWidget(self.selectedObjLabel)
        main_layout.addLayout(select_layout)
        main_layout.addSpacing(10)

        # --- Number of Points layout ---
        points_layout = QtWidgets.QHBoxLayout()
        points_layout.addWidget(self.numPointsLabel)
        points_layout.addWidget(self.numPointsSpin)
        main_layout.addLayout(points_layout)
        main_layout.addSpacing(10)

        # --- Bounds layout in a group box ---
        bounds_group = QtWidgets.QGroupBox("Bounds")
        bounds_layout = QtWidgets.QGridLayout()
        # Row labels
        bounds_layout.addWidget(QtWidgets.QLabel("Axis"), 0, 0)
        bounds_layout.addWidget(QtWidgets.QLabel("Min"), 0, 1)
        bounds_layout.addWidget(QtWidgets.QLabel("Max"), 0, 2)
        # X row
        bounds_layout.addWidget(QtWidgets.QLabel("X:"), 1, 0)
        bounds_layout.addWidget(self.min_x_spin, 1, 1)
        bounds_layout.addWidget(self.max_x_spin, 1, 2)
        # Y row
        bounds_layout.addWidget(QtWidgets.QLabel("Y:"), 2, 0)
        bounds_layout.addWidget(self.min_y_spin, 2, 1)
        bounds_layout.addWidget(self.max_y_spin, 2, 2)
        # Z row
        bounds_layout.addWidget(QtWidgets.QLabel("Z:"), 3, 0)
        bounds_layout.addWidget(self.min_z_spin, 3, 1)
        bounds_layout.addWidget(self.max_z_spin, 3, 2)

        bounds_group.setLayout(bounds_layout)
        main_layout.addWidget(bounds_group)
        main_layout.addSpacing(10)

        # --- Create Node button ---
        main_layout.addWidget(self.createNodeButton)
        main_layout.addStretch()

    def create_connections(self):
        self.selectObjButton.clicked.connect(self.record_selected_object)
        self.createNodeButton.clicked.connect(self.create_random_node)

    def record_selected_object(self):
        """Records the currently selected object in Maya and updates the label."""
        sel = cmds.ls(selection=True)
        if not sel:
            cmds.warning("No object selected!")
            self.selectedObjLabel.setText("No object selected")
            self.selectedObjLabel.setStyleSheet("color: red;")
            self.selected_object = None
        else:
            # For simplicity, we take the first object in the selection list.
            self.selected_object = sel[0]
            self.selectedObjLabel.setText(self.selected_object)
            self.selectedObjLabel.setStyleSheet("color: green;")
            cmds.inViewMessage( amg='Selected object: <hl>%s</hl>' % self.selected_object, pos='topCenter', fade=True )

    def create_random_node(self):
        """Creates the randomNode and associated instancer using the user parameters."""
        # Make sure an object is selected.
        if not self.selected_object:
            cmds.warning("Please select an object to instance before creating the node.")
            return

        # Get parameters from the UI.
        num_points = self.numPointsSpin.value()
        min_x = self.min_x_spin.value()
        max_x = self.max_x_spin.value()
        min_y = self.min_y_spin.value()
        max_y = self.max_y_spin.value()
        min_z = self.min_z_spin.value()
        max_z = self.max_z_spin.value()

        # Create the randomNode.
        try:
            rand_node = cmds.createNode("randomNode", name="randomNode1")
            cmds.setAttr(rand_node + ".inNumPoints", num_points)
            cmds.setAttr(rand_node + ".min_x", min_x)
            cmds.setAttr(rand_node + ".max_x", max_x)
            cmds.setAttr(rand_node + ".min_y", min_y)
            cmds.setAttr(rand_node + ".max_y", max_y)
            cmds.setAttr(rand_node + ".min_z", min_z)
            cmds.setAttr(rand_node + ".max_z", max_z)
            cmds.confirmDialog(title='Random Node Created', message='Created node: ' + rand_node, button=['OK'])
        except Exception as e:
            cmds.error("Failed to create or set attributes on randomNode: %s" % e)
            return

        # Create the instancer node.
        try:
            inst_node = cmds.createNode("instancer", name="randomInstancer1")
        except Exception as e:
            cmds.error("Failed to create instancer node: %s" % e)
            return

        # Connect the selected object's matrix to the instancer's input hierarchy.
        # This tells the instancer which object to instance.
        try:
            cmds.connectAttr(self.selected_object + ".matrix", inst_node + ".inputHierarchy[0]", force=True)
        except Exception as e:
            cmds.error("Failed to connect selected object to instancer: %s" % e)
            return

        # Connect the random node's output points to the instancer.
        # (Note: The attribute names on the instancer may need adjustment
        # depending on your workflow and Maya version.)
        try:
            cmds.connectAttr(rand_node + ".outPoints", inst_node + ".inputPoints", force=True)
        except Exception as e:
            cmds.error("Failed to connect randomNode to instancer: %s" % e)
            return


        cmds.inViewMessage( amg='Random node and instancer created successfully!', pos='topCenter', fade=True )

def showRandomNodeUI():
    """If a previous instance exists, delete it and show a new one."""
    global randomNodeDialog
    try:
        randomNodeDialog.close()  # Try to close the previous window.
        randomNodeDialog.deleteLater()
    except:
        pass
    randomNodeDialog = RandomNodeUI()
    randomNodeDialog.show()

# To launch the UI, simply run:
showRandomNodeUI()
