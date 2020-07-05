import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import mayautils

def maya_main_window():
    """Return maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class smartsaveui(QtWidgets.QDialog):

    def __init__(self):
        '''Constructor'''
        #Allows constructor to work with python 2 and 3
        super(smartsaveui, self).__init__(parent=maya_main_window())
        self.scene = mayautils.SceneFile()

        self.setWindowTitle("Maya Smart Save")
        self.resize(500,200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create widgets for our UI"""
        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 50px")

        self.dir_lbl = QtWidgets.QLabel("Directory")
        self.dir_le = QtWidgets.QLineEdit()
        self.dir_le.setText(self.scene.dir)
        self.browse_btn = QtWidgets.QPushButton("Browse...")

        self.descriptor_lbl = QtWidgets.QLabel("Descriptor")
        self.descriptor_le = QtWidgets.QLineEdit("main")
        self.descriptor_le.setText(self.scene.descriptor)

        self.version_lbl = QtWidgets.QLabel("Version")
        self.version_spinbox = QtWidgets.QSpinBox()
        self.version_spinbox.setValue(1)
        self.version_spinbox.setValue(self.scene.version)

        self.ext_lbl = QtWidgets.QLabel("Extension")
        self.ext_le = QtWidgets.QLineEdit("ma")
        self.ext_le.setText(self.scene.ext)

        self.save_btn = QtWidgets.QPushButton("Save")
        self.increment_save_btn = QtWidgets.QPushButton("Increment & Save")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        """Arranges the layout for the widgets in UI"""
        self.main_layout = QtWidgets.QVBoxLayout()

        self.descriptor_lay = QtWidgets.QHBoxLayout()
        self.descriptor_lay.addWidget(self.descriptor_lbl)
        self.descriptor_lay.addWidget(self.descriptor_le)

        self.version_lay = QtWidgets.QHBoxLayout()
        self.version_lay.addWidget(self.version_lbl)
        self.version_lay.addWidget(self.version_spinbox)

        self.ext_lay = QtWidgets.QHBoxLayout()
        self.ext_lay.addWidget(self.ext_lbl)
        self.ext_lay.addWidget(self.ext_le)

        self.directory_lay = QtWidgets.QHBoxLayout()
        self.directory_lay.addWidget(self.dir_lbl)
        self.directory_lay.addWidget(self.dir_le)
        self.directory_lay.addWidget(self.browse_btn)

        self.bottom_btn_lay = QtWidgets.QHBoxLayout()
        self.bottom_btn_lay.addWidget(self.save_btn)
        self.bottom_btn_lay.addWidget(self.increment_save_btn)
        self.bottom_btn_lay.addWidget(self.cancel_btn)

        self.main_layout.addWidget(self.title_lbl)
        self.main_layout.addLayout(self.directory_lay)
        self.main_layout.addLayout(self.descriptor_lay)
        self.main_layout.addLayout(self.version_lay)
        self.main_layout.addLayout(self.ext_lay)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.bottom_btn_lay)
        self.setLayout(self.main_layout)

    def create_connections(self):
        """Connects the widget signals to each button/widget"""
        self.cancel_btn.clicked.connect(self.cancel)
        self.save_btn.clicked.connect(self.save)
        self.increment_save_btn.clicked.connect(self.smartSave)
        self.browse_btn.clicked.connect(self.browse)

    @QtCore.Slot()
    def cancel(self):
        """Quits the dialog, closing the save window"""
        self.close()

    def _updateSceneVars(self):
        """"Saves data entered into UI window to SceneFile"""
        self.scene.dir = self.dir_le.text()
        self.scene.descriptor = self.descriptor_le.text()
        self.scene.version = self.version_spinbox.value()
        self.scene.ext = self.ext_le.text()

    @QtCore.Slot()
    def save(self):
        """Saves the scene's info to sceneFile"""
        self._updateSceneVars()
        self.scene.save()

    @QtCore.Slot()
    def smartSave(self):
        """Increments file version based on latest version before saving"""
        self._updateSceneVars()
        self.scene.increment_and_save()

    @QtCore.Slot()
    def browse(self):
        """Opens file browser to select file save location"""
        fileName = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder',
                                                              str(self.scene.dir),
                                                              QtWidgets.QFileDialog.ShowDirsOnly)
        if fileName != '':
            self.dir_le.setText(fileName)