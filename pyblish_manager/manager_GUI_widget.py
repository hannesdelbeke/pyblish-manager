import sys
import pyblish.api
from Qt import QtWidgets, QtCore, QtGui
from .pyblish_register_types import *


class DataWidget(QtWidgets.QWidget):
    def __init__(self, data_type, parent=None):
        super(DataWidget, self).__init__(parent)
        self.data_type = data_type

        self.data_list_widget = QtWidgets.QListWidget(self)
        self.data_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.data_list_widget.setDragEnabled(True)
        self.data_list_widget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.data_list_widget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.data_list_widget.setDropIndicatorShown(True)
        self.data_list_widget.setAcceptDrops(True)
        self.data_list_widget.setDragDropOverwriteMode(False)

        self.add_button = QtWidgets.QPushButton('Add')
        self.add_button.clicked.connect(self.add_to_register)
        self.remove_button = QtWidgets.QPushButton('Remove')
        self.remove_button.clicked.connect(self.remove_from_register)

        layout_edit_buttons = QtWidgets.QHBoxLayout()
        layout_edit_buttons.addWidget(self.add_button)
        layout_edit_buttons.addWidget(self.remove_button)

        # self.remove_all_button = QtWidgets.QPushButton('Remove All')
        # self.remove_all_button.clicked.connect(self.remove_all_data)
        # self.list_button = QtWidgets.QPushButton('List')
        # self.list_button.clicked.connect(self.list_data)
        # self.data_list_widget.itemSelectionChanged.connect(self.update_buttons)
        # self.update_buttons()

        self.type_dropdown = QtWidgets.QComboBox()
        self.type_dropdown.addItems([x.name for x in registered_data_types])
        self.type_dropdown.currentIndexChanged.connect(self.change_data_type)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.addWidget(QtWidgets.QLabel('registered'))
        layout_buttons.addWidget(self.type_dropdown)
        layout_buttons.addStretch()

        launch_gui = QtWidgets.QPushButton('Launch GUI')
        launch_gui.clicked.connect(self.launch_gui)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(layout_buttons)
        self.main_layout.addWidget(self.data_list_widget)
        self.main_layout.addLayout(layout_edit_buttons)
        self.main_layout.addWidget(launch_gui)

        # self.scroll_widget = QtWidgets.QWidget()  # placeholder
        self.refresh_scroll()

        self.setLayout(self.main_layout)

    def launch_gui(self):
        # pyblish.api.register_gui()
        show()  # todo for now this will only work in maya

    def change_data_type(self):
        self.data_type = [x for x in registered_data_types if x.name == self.type_dropdown.currentText()][0]
        self.refresh_scroll()
        self.add_button.setEnabled(self.data_type.ui_add_mode is not None)

    def refresh_scroll(self):
        data_list = self.data_type.list_command()
        self.data_list_widget.clear()

        data_list = self.format_data(data_list)

        self.data_list_widget.addItems(data_list)
        print(data_list)

    def format_data(self, data_list):
        # handle dict, example callbacks
        if type(data_list) is dict:
            data_list = [key + ': ' + str(value) for key, value in data_list.items()]

        # handle single entry, example tests
        if type(data_list) is not list:
            data_list = [str(data_list)]

        # handle list of classes, example discovered_plugins
        if len(data_list)>0 and type(data_list[0]) is not str:
            data_list = [str(x) for x in data_list]

        return data_list


    def add_to_register(self):
        data = None

        if self.data_type.ui_add_mode == 'text':
            text, ok = QtWidgets.QInputDialog.getText(self, 'Register '.format(self.data_type.name),
                                                      'Enter {}:'.format(self.data_type.name))
            if ok and text:
                data = str(text)  # convert unicode to string to prevent pyblish ui crashing

        elif self.data_type.ui_add_mode == 'browse':
            path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
            if path:
                data = str(path)  # convert unicode to string to prevent pyblish ui crashing

        elif self.data_type.ui_add_mode:
            data = self.data_type.ui_add_mode(self)

        if data:
            self.data_type.add_command(data)
            self.refresh_scroll()

    def remove_from_register(self):
        selected = self.data_list_widget.selectedItems()
        if not selected:
            return

        for item in selected:
            self.data_type.remove_command(item.text())

        self.refresh_scroll()





def make_config(discover=True, config=None, qapp=True):
    # if discover:
    #
    #     # get all plugins from pyblish
    #
    #     # support creating a pipeline for specific hosts. ex a maya pipeline
    #     # todo set input before we discover. ex host maya
    #     # or pyblish version, see def plugins_from_module() in pyblish.plugin.py
    #
    #     # api.register_host('maya')  # todo change this to not rely on maya
    #     # todo atm some plugins fail because of cannot import cmds from maya, when run from python
    #
    #     plugins = pyblish.api.discover()
    #     # config = get_pipeline_config_from_plugins(plugins)

    if qapp:
        app = QtWidgets.QApplication(sys.argv)


    m = DataWidget(plugin_paths) #QtWidgets.QWidget()

    m.show()
    if qapp:
        app.exec_()

    return m

#make_config(qapp=True)









# stolen from pyblish-maya. ideally this would live in pyblish-base
def _discover_gui():
    """Return the most desirable of the currently registered GUIs"""

    # Prefer last registered
    guis = reversed(pyblish.api.registered_guis())

    for gui in guis:
        try:
            gui = __import__(gui).show
        except (ImportError, AttributeError):
            continue
        else:
            return gui


# stolen from pyblish-maya. ideally this would live in pyblish-base
def show():
    """Try showing the most desirable GUI

    This function cycles through the currently registered
    graphical user interfaces, if any, and presents it to
    the user.

    """

    parent = next(
        o for o in QtWidgets.QApplication.instance().topLevelWidgets()
        if o.objectName() == "MayaWindow"
    )

    gui = _discover_gui()

    if gui is None:
        # _show_no_gui()
        print("no gui found")  # changed
    else:
        return gui(parent)
