import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx

import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog

from ui.tinyblast_options import Ui_TinyblastOptions

from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtCore import QCoreApplication
import shiboken6

# Global variable to store the scriptJob ID
playblast_job_id = None
original_playblast = cmds.playblast

def get_plugin_directory():
    # Get the path of the currently loaded plugin
    plugin_name = "tinyblast"
    plugin_path = cmds.pluginInfo(plugin_name, query=True, path=True)
    return os.path.dirname(plugin_path)

def custom_playblast(*args, **kwargs):
    print("Running tinyblast...")

    kwargs['format'] = 'avi'
    kwargs['percent'] = 100
    kwargs['quality'] = 100
    kwargs['widthHeight'] = (1920, 1080)

    result = original_playblast(*args, **kwargs)
    print(f"{result}")

    if result:
        try:
            ffmpeg_path = os.path.join(get_plugin_directory(), 'ffmpeg.exe')
            print(f"ffmpeg path: {ffmpeg_path}")
            if not os.path.exists(ffmpeg_path):
                raise FileNotFoundError(f"FFmpeg binary not found at {ffmpeg_path}")

            input_file = result  # The file output by playblast
            #output_directory = os.path.dirname(result)  # Get the directory path
            output_directory = os.path.dirname(cmds.file(query=True, sceneName=True))
            input_filename = os.path.basename(result)  # Get the filename with extension

            # Change the extension to .mp4
            output_filename = os.path.splitext(input_filename)[0] + ".mp4"

            # Define the full path for the converted output file
            output_file = os.path.join(output_directory, output_filename)

            # Run FFmpeg conversion
            subprocess.run([ffmpeg_path,
                            '-i', input_file,
                            '-vcodec', 'libx264',
                            '-pix_fmt', 'yuv420p',
                            '-strict', 'experimental',
                            '-b:v', '1m',
                            output_file,
                            '-y'], check=True, shell=True)
            print(f"Video conversion to {output_file} successful!")
            # os.remove(input_file) # Running into permission issues trying to delete from AppData
            # print(f"Original playblast deleted: {input_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during FFmpeg conversion: {e}")

class WindowWatcher:
    """ A class to watch for a particular window in Maya """

    def __init__(self, window_title, on_open_callback, on_close_callback=None):
        self.window_title = window_title
        self.on_open_callback = on_open_callback
        self.on_close_callback = on_close_callback
        self.window_opened = False

    def check_for_window_open(self):
        if not self.window_opened:
            window = self.get_window_by_title(self.window_title)
            if window:
                self.on_open_callback()
                self.window_opened = True
        else:
            window = self.get_window_by_title(self.window_title)
            if not window:
                self.window_opened = False
                if self.on_close_callback:
                    self.on_close_callback()

    def get_window_by_title(self, title):
        # Check all open windows and return the one that matches the title
        windows = cmds.lsUI(windows=True)
        for window in windows:
            if cmds.window(window, query=True, title=True) == title:
                return window
        return None


def add_custom_button_to_playblast():
    # Get the Playblast Options window
    window = get_playblast_options_window()

    if window:
        # Find the layout of the Playblast Options window
        layout = cmds.columnLayout(adjustableColumn=True)
        if layout:
            # Add a custom button below existing UI
            cmds.setParent(layout)  # Set the parent to the top-level layout
            cmds.columnLayout(adjustableColumn=True)
            cmds.button(label="Tinyblast", command=custom_button_action)
        else:
            print("Couldn't find the layout for the Playblast Options window.")
    else:
        print("Playblast Options window not found.")


def custom_button_action(*args):
    cmds.playblast()


def get_playblast_options_window():
    # Check if the Playblast Options window is open
    windows = cmds.lsUI(windows=True)
    for window in windows:
        if cmds.window(window, query=True, title=True) == "Playblast Options":  # Exact title match
            return window
    return None

def setup_script_job():
    global playblast_job_id

    # Kill any previously running scriptJob
    if playblast_job_id is not None and cmds.scriptJob(exists=playblast_job_id):
        cmds.scriptJob(kill=playblast_job_id, force=True)
        print(f"Killed previous scriptJob with ID: {playblast_job_id}")

    # Watch for the Playblast Options window by title
    playblast_watcher = WindowWatcher(
        window_title="Playblast Options",  # Exact window title to look for
        on_open_callback=add_custom_button_to_playblast
    )

    # Set up a new scriptJob
    playblast_job_id = cmds.scriptJob(event=["idle", playblast_watcher.check_for_window_open])

class Tinyblast(ompx.MPxCommand):
    def __init__(self):
        ompx.MPxCommand.__init__(self)

    def doIt(selfself, args):
        print("Tinyblasting...")
        cmds.playblast()

    @staticmethod
    def cmdCreator():
        return ompx.asMPxPtr(Tinyblast())

def get_maya_window():
    import maya.OpenMayaUI as omui
    from PySide6 import QtWidgets
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken6.wrapInstance(int(ptr), QtWidgets.QWidget)
    else:
        return None


class TinyblastOptionsWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TinyblastOptionsWindow, self).__init__(parent or get_maya_window())
        self.ui = Ui_TinyblastOptions()
        self.ui.setupUi(self)

        self.ui.formattingComboBox.currentIndexChanged.connect(self.update_format)

        self.ui.tinyblastButton.clicked.connect(self.tinyblast)
        self.ui.applyButton.clicked.connect(self.apply_settings)
        self.ui.quitButton.clicked.connect(self.quit_window)

        self.ui.qualitySlider.valueChanged.connect(self.update_quality_slider)
        self.ui.qualitySpinBox.valueChanged.connect(self.update_quality_spinbox)

        self.ui.displaySizeComboBox.currentIndexChanged.connect(self.update_display_size)

        self.ui.scaleSlider.valueChanged.connect(self.update_scale_slider)
        self.ui.scaleSpinBox.valueChanged.connect(self.update_scale_spinbox)

        self.ui.framePaddingSlider.valueChanged.connect(self.update_frame_padding_slider)
        self.ui.framePaddingSpinBox.valueChanged.connect(self.update_frame_padding_spinbox)

        self.ui.saveToFileCheckBox.toggled.connect(self.save_to_file_toggle)
        self.ui.browseButton.clicked.connect(self.browse_files)

    def update_format(self, index):
        self.ui.encodingComboBox.clear()
        # MP4
        if index == 0:
            self.ui.encodingComboBox.addItems([
                QCoreApplication.translate("TinyblastOptions", u"HEVC (H.265)", None),
                QCoreApplication.translate("TinyblastOptions", u"H.264", None),
                QCoreApplication.translate("TinyblastOptions", u"AV1", None),
                QCoreApplication.translate("TinyblastOptions", u"MPEG-4", None),
                QCoreApplication.translate("TinyblastOptions", u"VP9", None)
            ])

            if self.ui.filePathTextBox.text():
                split_path = self.ui.filePathTextBox.text().rsplit('.', 1)
                self.ui.filePathTextBox.setText(f"{split_path[0]}.mp4")

        # MKV
        if index == 1:
            self.ui.encodingComboBox.addItems([
                QCoreApplication.translate("TinyblastOptions", u"HEVC (H.265)", None),
                QCoreApplication.translate("TinyblastOptions", u"H.264", None),
                QCoreApplication.translate("TinyblastOptions", u"AV1", None),
                QCoreApplication.translate("TinyblastOptions", u"VP9", None),
                QCoreApplication.translate("TinyblastOptions", u"VP8", None),
                QCoreApplication.translate("TinyblastOptions", u"Theora", None)
            ])

            if self.ui.filePathTextBox.text():
                split_path = self.ui.filePathTextBox.text().rsplit('.', 1)
                self.ui.filePathTextBox.setText(f"{split_path[0]}.mkv")
        # MOV
        if index == 2:
            self.ui.encodingComboBox.addItems([
                QCoreApplication.translate("TinyblastOptions", u"Apple ProRes", None),
                QCoreApplication.translate("TinyblastOptions", u"HEVC (H.265)", None),
                QCoreApplication.translate("TinyblastOptions", u"H.264", None),
                QCoreApplication.translate("TinyblastOptions", u"MPEG-4", None)
            ])

            if self.ui.filePathTextBox.text():
                split_path = self.ui.filePathTextBox.text().rsplit('.', 1)
                self.ui.filePathTextBox.setText(f"{split_path[0]}.mov")
        # AVI
        if index == 3:
            self.ui.encodingComboBox.addItems([
                QCoreApplication.translate("TinyblastOptions", u"H.264", None),
                QCoreApplication.translate("TinyblastOptions", u"MPEG-4", None),
                QCoreApplication.translate("TinyblastOptions", u"DivX", None),
                QCoreApplication.translate("TinyblastOptions", u"Xvid", None),
                QCoreApplication.translate("TinyblastOptions", u"Motion JPEG", None),
            ])

            if self.ui.filePathTextBox.text():
                split_path = self.ui.filePathTextBox.text().rsplit('.', 1)
                self.ui.filePathTextBox.setText(f"{split_path[0]}.avi")
        # WEBM
        if index == 4:
            self.ui.encodingComboBox.addItems([
                QCoreApplication.translate("TinyblastOptions", u"AV1", None),
                QCoreApplication.translate("TinyblastOptions", u"VP9", None),
                QCoreApplication.translate("TinyblastOptions", u"VP8", None)
            ])

            if self.ui.filePathTextBox.text():
                split_path = self.ui.filePathTextBox.text().rsplit('.', 1)
                self.ui.filePathTextBox.setText(f"{split_path[0]}.webm")

    def tinyblast(self):
        print("Tinyblasting...")
        cmds.playblast()

    def apply_settings(self):
        print("TODO")

    def quit_window(self):
        tb_window.close()

    def update_quality_slider(self, value):
        self.ui.qualitySpinBox.setValue(value)
    def update_quality_spinbox(self, value):
        self.ui.qualitySlider.setValue(value)

    def update_display_size(self, index):
        if index == 0:
            self.ui.widthSpinBox.setEnabled(False)
            self.ui.heightSpinBox.setEnabled(False)
        if index == 1:
            self.ui.widthSpinBox.setEnabled(False)
            self.ui.heightSpinBox.setEnabled(False)
        if index == 2:
            self.ui.widthSpinBox.setEnabled(True)
            self.ui.heightSpinBox.setEnabled(True)


    def update_scale_slider(self, value):
        self.ui.scaleSpinBox.setValue(float(value/1000.0))
    def update_scale_spinbox(self, value):
        self.ui.scaleSlider.setValue(int(value*1000))

    def update_frame_padding_slider(self, value):
        self.ui.framePaddingSpinBox.setValue(value)
    def update_frame_padding_spinbox(self, value):
        self.ui.framePaddingSlider.setValue(value)

    def save_to_file_toggle(self):
        if self.ui.saveToFileCheckBox.isChecked():
            self.ui.browseButton.setEnabled(True)
            self.ui.filePathTextBox.setEnabled(True)
        else:
            self.ui.browseButton.setEnabled(False)
            self.ui.filePathTextBox.setEnabled(False)

    def browse_files(self):
        path = self.choose_save_path()
        self.ui.filePathTextBox.setText(f"{path}")

    def choose_save_path(self):
        current_container = str(self.ui.formattingComboBox.currentText()).lower()
        save_path, _ = QFileDialog.getSaveFileName(
            None,
            "Choose Save Location",
            "",
            f"Video (*.{current_container});;All Files (*)"
        )
        return save_path

def show_my_window():
    global tb_window
    try:
        tb_window.close()
        tb_window.deleteLater()
    except:
        pass
    tb_window = TinyblastOptionsWindow()
    tb_window.show()

class MyPluginCommand(ompx.MPxCommand):
    def __init__(self):
        ompx.MPxCommand.__init__(self)

    def doIt(self, args):
        show_my_window()

def cmdCreator():
    return ompx.asMPxPtr(MyPluginCommand())

def initializePlugin(mobject):
    try:
        mplugin = ompx.MFnPlugin(mobject, "Jack Christensen", "1.0.0", "Any")
        mplugin.registerCommand("tinyblast", Tinyblast.cmdCreator)
        mplugin.registerCommand("myPluginCommand", cmdCreator)
        om.MGlobal.displayInfo("Tinyblast plugin loaded.")
        setup_script_job()
        cmds.playblast = custom_playblast
    except Exception as e:
        om.MGlobal.displayError(f"Failed to initialize plugin: {str(e)}")
        raise

def uninitializePlugin(mobject):
    try:
        mplugin = ompx.MFnPlugin(mobject)
        tb_window.close()
        mplugin.deregisterCommand("tinyblast")
        mplugin.deregisterCommand("myPluginCommand")
        om.MGlobal.displayInfo("Tinyblast plugin unloaded.")
    except Exception as e:
        om.MGlobal.displayError(f"Failed to uninitialize plugin: {str(e)}")
        raise