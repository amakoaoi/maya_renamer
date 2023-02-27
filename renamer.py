from PySide2.QtWidgets import QGridLayout, QPushButton, QLineEdit, QLabel, QFrame, QRadioButton, QCheckBox, QWidget, QTabWidget, QHBoxLayout
from PySide2 import QtWidgets as Q
from PySide2 import QtGui
from maya import cmds
from maya_helper import MayaDockableWindow, UndoStack
import re


class MayaRenamer(MayaDockableWindow):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setWindowTitle("Maya Renamer Tool")

        main_layout = QGridLayout()
        self.setLayout(main_layout)

        suffix_button = QPushButton("Add")
        suffix_button.clicked.connect(self.suffix)

        prefix_button = QPushButton("Add")
        prefix_button.clicked.connect(self.add_prefix)

        self.suffix_edit = QLineEdit()
        self.suffix_edit.setPlaceholderText("Suffix")

        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText("Prefix")

        suffix_label = QLabel("Suffix")
        prefix_label = QLabel("Prefix")

        line = QFrame()
        line.setFrameStyle(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)

        line2 = QFrame()
        line2.setFrameStyle(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        line2.setLineWidth(1)

        line3 = QFrame()
        line3.setFrameStyle(QFrame.HLine)
        line3.setFrameShadow(QFrame.Sunken)
        line3.setLineWidth(1)

        presets = QHBoxLayout()

        search_label = QLabel("Search for:")
        replace_label = QLabel("Replace with:")

        replace_button = QPushButton("Replace")
        replace_button.clicked.connect(self.replace)

        group_button = QPushButton("grp")
        group_button.clicked.connect(lambda: self.rename_presets("grp"))
        geo_button = QPushButton("geo")
        geo_button.clicked.connect(lambda: self.rename_presets("geo"))
        ctl_button = QPushButton("ctl")
        ctl_button.clicked.connect(lambda: self.rename_presets("ctl"))
        jnt_button = QPushButton("jnt")
        jnt_button.clicked.connect(lambda: self.rename_presets("jnt"))

        self.left_radio = QRadioButton("Left")
        self.right_radio = QRadioButton("Right")
        self.none_radio = QRadioButton("None")
        self.none_radio.setChecked(True)
        position_radio_grp = Q.QButtonGroup(self)
        position_radio_grp.addButton(self.left_radio)
        position_radio_grp.addButton(self.right_radio)
        position_radio_grp.addButton(self.none_radio)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search for")

        self.replace_edit = QLineEdit()
        self.replace_edit.setPlaceholderText("Replace with")

        self.selected_radio = QRadioButton("Selected")
        self.selected_radio.setChecked(True)
        hierarchy_radio = QRadioButton("Hierarchy")
        self.case_checkbox = QCheckBox("Case insensitive")
        replace_radio_grp = Q.QButtonGroup(self)
        replace_radio_grp.addButton(self.selected_radio)
        replace_radio_grp.addButton(hierarchy_radio)

        padding_rename_label = QLabel("Rename: ")
        padding_start_label = QLabel("Start: ")
        padding_label = QLabel("Padding: ")

        self.rename_padding_edit = QLineEdit()
        self.rename_padding_edit.setPlaceholderText("New name")
        self.padding_start_edit = Q.QSpinBox()
        self.padding_start_edit.setValue(1)
        self.padding_start_edit.setMinimum(0)
        self.padding_edit = Q.QSpinBox()
        self.padding_edit.setValue(1)
        self.padding_edit.setMinimum(1)
        padding_button = QPushButton("Rename and number")
        padding_button.clicked.connect(self.padding_rename)

        padding_layout = QHBoxLayout()

        main_layout.addWidget(prefix_label, 0, 0)
        main_layout.addWidget(self.prefix_edit, 0, 1)
        main_layout.addWidget(prefix_button, 0, 2)

        main_layout.addWidget(suffix_label, 1, 0)
        main_layout.addWidget(self.suffix_edit, 1, 1)
        main_layout.addWidget(suffix_button, 1, 2)

        main_layout.addWidget(line, 2, 0, 1, 3)

        main_layout.addWidget(search_label, 3, 0)
        main_layout.addWidget(replace_label, 5, 0)

        main_layout.addWidget(self.search_edit, 3, 1, 1, 2)
        main_layout.addWidget(self.case_checkbox, 4 , 1)
        main_layout.addWidget(self.replace_edit, 5, 1, 1, 2)

        main_layout.addWidget(self.selected_radio, 6, 1)
        main_layout.addWidget(hierarchy_radio, 6, 2)

        main_layout.addWidget(replace_button, 7, 1, 1, 2)

        main_layout.addWidget(line2, 8, 0, 1, 3)

        main_layout.addLayout(presets, 10, 0, 1, 3)

        presets.addWidget(group_button)
        presets.addWidget(geo_button)
        presets.addWidget(ctl_button)
        presets.addWidget(jnt_button)

        main_layout.addWidget(self.left_radio, 9, 0)
        main_layout.addWidget(self.right_radio,9, 1)
        main_layout.addWidget(self.none_radio, 9, 2)

        main_layout.addWidget(line3, 11, 0, 1, 3)

        main_layout.addWidget(padding_rename_label, 12, 0)
        main_layout.addWidget(self.rename_padding_edit, 12, 1, 1, 2)
        main_layout.addLayout(padding_layout, 13, 0, 1, 3)

        padding_layout.addWidget(padding_start_label)
        padding_layout.addWidget(self.padding_start_edit)
        padding_layout.addWidget(padding_label)
        padding_layout.addWidget(self.padding_edit)

        main_layout.addWidget(padding_button, 14, 0, 1, 3)

        self.show()

    def add_prefix(self):
        prefix = self.prefix_edit.text()
        if not prefix:
            return
        selection = cmds.ls(selection=True, long=True)
        selection.sort(reverse=True)
        with UndoStack("addPrefix"):
            for node in selection:
                name = node.split("|")[-1]
                name = "{}{}".format(prefix, name)
                self.rename_node(node, name)

    def suffix(self):
        suffix = self.suffix_edit.text()
        if not suffix:
            return
        self.add_suffix(suffix)

    def add_suffix(self, suffix):
        selection = cmds.ls(selection=True, long=True)
        selection.sort(reverse=True)
        with UndoStack("addSuffix"):
            for node in selection:
                name = node.split("|")[-1]
                name = "{}{}".format(name, suffix)
                self.rename_node(node, name)

    def rename_node(self, node, name):
        try:
            cmds.rename(node, name)
        except RuntimeError:
            cmds.warning("Cannot rename {}".format(node))
            return

    def replace(self):
        search = self.search_edit.text()
        replace = self.replace_edit.text()

        if not search or not replace:
            return

        selection = cmds.ls(selection=True, long=True)
        selection.sort(reverse=True)

        nodes = []
        if not self.selected_radio.isChecked():
            for node_path in selection:
                if not cmds.objectType(node_path, isType="transform"):
                    continue
                children = cmds.listRelatives(node_path, allDescendents=True, fullPath=True, type="transform") or []
                for child in children:
                    if child not in nodes:
                        nodes.append(child)
                if node_path not in nodes:
                    nodes.append(node_path)
        else:
            nodes = selection

        with UndoStack("replace"):
            for node_path in nodes:
                name = node_path.split("|")[-1]

                if self.case_checkbox.isChecked():
                    index = name.lower().index(search.lower())
                    search = name[index:index + len(search)]

                name = name.replace(search, replace)
                self.rename_node(node_path, name)

    def rename_presets(self, node_type):
        correct_suffix = ""
        if self.right_radio.isChecked():
            correct_suffix = "_R_{}".format(node_type)
        elif self.left_radio.isChecked():
            correct_suffix = "_L_{}".format(node_type)
        else:
            correct_suffix = "_{}".format(node_type)

        selection = cmds.ls(selection=True, long=True)
        selection.sort(reverse=True)
        with UndoStack("renamePresets"):
            for node in selection:
                name = node.split("|")[-1]
                check = re.findall("(_[LR])?_(geo|ctl|jnt|grp)$", name)
                if not check:
                    name = "{}{}".format(name, correct_suffix)
                else:
                    name = re.sub("(_[LR])?_(geo|ctl|jnt|grp)$", correct_suffix, name)
                self.rename_node(node, name)

    def padding_rename(self):
        padding_name = self.rename_padding_edit.text()

        if not padding_name:
            return

        start = self.padding_start_edit.value()
        padding = self.padding_edit.value()

        selection = cmds.ls(selection=True, long=True)
        selection.sort(reverse=True)
        with UndoStack("padding"):
            for node in selection:
                zero = padding - len(str(start))
                new_name = "{}_{}{}".format(padding_name, "0" * zero, start)
                self.rename_node(node, new_name)
                start += 1




