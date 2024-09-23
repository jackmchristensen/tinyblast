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
from PySide6.QtCore import QCoreApplication, QSettings
import shiboken6

tinyblast_instance = None

def get_plugin_directory():
    # Get the path of the currently loaded plugin
    plugin_name = "tinyblast"
    plugin_path = cmds.pluginInfo(plugin_name, query=True, path=True)
    return os.path.dirname(plugin_path)

def custom_button_action(*args):
    tinyblast_instance.custom_playblast()

class Tinyblast(ompx.MPxCommand):
    def __init__(self):
        ompx.MPxCommand.__init__(self)
        self.format = 'mp4'
        self.codec = 'libx265'
        self.bitrate = '5m'
        self.pixel_format = 'yuv420p'
        self.resolution = (1920, 1080)
        # self.resolution = (cmds.getAttr("defaultResolution.width"), cmds.getAttr("defaultResolution.height"))
        self.percent = '100'
        self.padding = 4
        self.path = ''
        self.save = True

    def apply_settings(self, format, codec, quality, resolution, scale, file_path, padding, save):
        self.format = format
        self.codec = self.get_codec(codec)
        self.bitrate = f"{round(8 * (resolution[0] * resolution[1]) / (1920 * 1080) * (float(quality) / 100), 1)}M"
        self.resolution = resolution
        self.percent = int(scale * 100)
        self.padding = int(padding)
        self.path = file_path
        self.save = save

    def get_codec(self, pretty_name):
        if pretty_name == 'HEVC (H.265)':
            return 'libx265'
        if pretty_name == 'H.264':
            return 'libx264'
        if pretty_name == 'AV1':
            return 'libaom-av1'
        if pretty_name == 'MPEG-4':
            return 'mpeg4'
        if pretty_name == 'P8':
            return 'libvpx'
        if pretty_name == 'VP9':
            return 'libvpx-vp9'
        if pretty_name == 'Theora':
            return 'libtheora'
        if pretty_name == 'DNxHD':
            return 'dnxhd'
        if pretty_name == 'DNxHR':
            return 'dnxhr'
        if pretty_name == 'Motion JPEG':
            return 'mjpeg'
        return 'Not a codec'

    def doIt(selfself, args):
        print("Tinyblasting...")
        tinyblast_instance.tinyblast()

    @staticmethod
    def cmdCreator():
        return ompx.asMPxPtr(Tinyblast())

    def custom_playblast(self, *args, **kwargs):
        kwargs['format'] = 'avi'
        kwargs['percent'] = int(self.percent)
        kwargs['quality'] = 100
        kwargs['widthHeight'] = self.resolution

        result = cmds.playblast(*args, **kwargs)

        if result and self.save:
            self.blastIt(result)

    def blastIt(self, input_path):
        try:
            ffmpeg_path = os.path.join(get_plugin_directory(), 'ffmpeg.exe')
            if not os.path.exists(ffmpeg_path):
                raise FileNotFoundError(f"FFmpeg binary not found at {ffmpeg_path}")

            input_file = input_path  # The file output by playblast
            #output_directory = os.path.dirname(result)  # Get the directory path
            output_directory = os.path.dirname(cmds.file(query=True, sceneName=True))
            input_filename = os.path.basename(input_path)  # Get the filename with extension

            # Change the extension to .mp4
            output_filename = os.path.splitext(input_filename)[0] + ".mp4"

            # Define the full path for the converted output file
            output_file = self.path

            # Run FFmpeg conversion
            subprocess.run([ffmpeg_path,
                            '-i', input_file,
                            '-vcodec',  self.codec,
                            '-pix_fmt', self.pixel_format,
                            '-strict', 'experimental',
                            '-b:v', self.bitrate,
                            output_file,
                            '-y'], check=True, shell=True)
            print(f"Video conversion to {output_file} successful!")
            # os.remove(input_file) # Running into permission issues trying to delete from AppData
            # print(f"Original playblast deleted: {input_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during FFmpeg conversion: {e}")

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

        self.resize(1280, 720)

        self.restore_settings()

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

    def get_codecs_from_format(self, index):
        if index == 0:
            self.ui.encodingComboBox.addItems([
                QCoreApplication.translate("TinyblastOptions", u"HEVC (H.265)", None),
                QCoreApplication.translate("TinyblastOptions", u"H.264", None),
                QCoreApplication.translate("TinyblastOptions", u"AV1", None),
                QCoreApplication.translate("TinyblastOptions", u"MPEG-4", None),
                QCoreApplication.translate("TinyblastOptions", u"VP9", None)
            ])
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
        # MOV
        if index == 2:
            self.ui.encodingComboBox.addItems([
                QCoreApplication.translate("TinyblastOptions", u"HEVC (H.265)", None),
                QCoreApplication.translate("TinyblastOptions", u"H.264", None),
                QCoreApplication.translate("TinyblastOptions", u"DNxHD", None),
                QCoreApplication.translate("TinyblastOptions", u"DNxHR", None),
                QCoreApplication.translate("TinyblastOptions", u"MPEG-4", None)
            ])
        # AVI
        if index == 3:
            self.ui.encodingComboBox.addItems([
                QCoreApplication.translate("TinyblastOptions", u"H.264", None),
                QCoreApplication.translate("TinyblastOptions", u"MPEG-4", None),
                QCoreApplication.translate("TinyblastOptions", u"Motion JPEG", None),
            ])
        # WEBM
        if index == 4:
            self.ui.encodingComboBox.addItems([
                QCoreApplication.translate("TinyblastOptions", u"AV1", None),
                QCoreApplication.translate("TinyblastOptions", u"VP9", None),
                QCoreApplication.translate("TinyblastOptions", u"VP8", None)
            ])

    # Restore applied settings
    def restore_settings(self):
        settings = QSettings("Jack Christensen", "Tinyblast")

        # Window size
        geometry = settings.value("windowGeometry")
        if geometry:
            self.restoreGeometry(geometry)

        # Format dropdown menu
        formatIndex = settings.value("formatIndex", 0)
        self.ui.formattingComboBox.setCurrentIndex(int(formatIndex))
        self.update_format(int(formatIndex))
        #self.get_codecs_from_format(int(formatIndex))

        # Codec dropdown menu
        codecIndex = settings.value("codecIndex", 0)
        self.ui.encodingComboBox.setCurrentIndex(int(codecIndex))

        # Quality value
        qualityValue = settings.value("qualityValue", 0)
        self.ui.qualitySpinBox.setValue(int(qualityValue))
        self.ui.qualitySlider.setValue(int(qualityValue))

        # Display size dropdown menu
        displaySizeIndex = settings.value("displaySizeIndex", 0)
        self.ui.displaySizeComboBox.setCurrentIndex(int(displaySizeIndex))

        # Resolution values
        resolutionValues = settings.value("resolution", [1920, 1080])
        if isinstance(resolutionValues, list) and len(resolutionValues) == 2:
            self.ui.widthSpinBox.setValue(int(resolutionValues[0]))
            self.ui.heightSpinBox.setValue(int(resolutionValues[1]))

        # Scale value
        scaleValue = settings.value("scaleValue", 0.0)
        self.ui.scaleSpinBox.setValue(float(scaleValue))
        self.ui.scaleSlider.setValue(int(float(scaleValue) * 1000.0))

        # Frame padding
        framePaddingValue = settings.value("framePaddingValue", 0)
        self.ui.framePaddingSpinBox.setValue(int(framePaddingValue))
        self.ui.framePaddingSlider.setValue(int(framePaddingValue))

        # Save to file checkbox
        saveToFile = settings.value("saveToFileCheck", False)
        if saveToFile == 'true':
            self.ui.saveToFileCheckBox.setChecked(True)
            self.ui.filePathTextBox.setEnabled(True)
            self.ui.browseButton.setEnabled(True)
        else:
            self.ui.saveToFileCheckBox.setChecked(False)
            self.ui.filePathTextBox.setEnabled(False)
            self.ui.browseButton.setEnabled(False)

        # Save path
        savePath = settings.value("savePath", 0)
        self.ui.filePathTextBox.setText(str(savePath))

    # settings = QSettings("Jack Christensen", "Tinyblast")
    # settings.setValue("formatIndex", self.ui.formattingComboBox.currentIndex())
    # settings.setValue("codecIndex", self.ui.encodingComboBox.currentIndex())
    # settings.setValue("qualityValue", self.ui.qualitySpinBox.value())
    # settings.setValue("displaySizeIndex", self.ui.displaySizeComboBox.currentIndex())
    # settings.setValue("resolution", (self.ui.widthSpinBox.value(), self.ui.heightSpinBox.value()))
    # settings.setValue("scaleValue", self.ui.scaleSpinBox.value())
    # settings.setValue("framePaddingValue", self.ui.framePaddingSpinBox.value())
    # settings.setValue("saveToFileCheck", self.ui.saveToFileCheckBox.isChecked())
    # settings.setValue("savePath", self.ui.filePathTextBox.text())

    # Save settings on close
    def closeEvent(self, event):
        settings = QSettings("Jack Christensen", "Tinyblast")
        settings.setValue("windowGeometry", self.saveGeometry())

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
                QCoreApplication.translate("TinyblastOptions", u"HEVC (H.265)", None),
                QCoreApplication.translate("TinyblastOptions", u"H.264", None),
                QCoreApplication.translate("TinyblastOptions", u"DNxHD", None),
                QCoreApplication.translate("TinyblastOptions", u"DNxHR", None),
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
        self.apply_settings()
        tinyblast_instance.custom_playblast()

    def apply_settings(self):
        # Directly call the `apply_settings` method of the Tinyblast instance
        if tinyblast_instance is not None:
            tinyblast_instance.apply_settings(
                self.ui.formattingComboBox.currentText(),  # Use the selected format
                self.ui.encodingComboBox.currentText(),  # Use the selected codec
                self.ui.qualitySpinBox.value(),  # Quality as a percentage
                (self.ui.widthSpinBox.value(), self.ui.heightSpinBox.value()),  # Resolution
                self.ui.scaleSpinBox.value(),  # Scale
                self.ui.filePathTextBox.text(),  # File path
                self.ui.framePaddingSpinBox.value(),
                self.ui.saveToFileCheckBox.isChecked()
            )
        settings = QSettings("Jack Christensen", "Tinyblast")
        settings.setValue("formatIndex", self.ui.formattingComboBox.currentIndex())
        settings.setValue("codecIndex", self.ui.encodingComboBox.currentIndex())
        settings.setValue("qualityValue", self.ui.qualitySpinBox.value())
        settings.setValue("displaySizeIndex", self.ui.displaySizeComboBox.currentIndex())
        settings.setValue("resolution", (self.ui.widthSpinBox.value(), self.ui.heightSpinBox.value()))
        settings.setValue("scaleValue", self.ui.scaleSpinBox.value())
        settings.setValue("framePaddingValue", self.ui.framePaddingSpinBox.value())
        settings.setValue("saveToFileCheck", self.ui.saveToFileCheckBox.isChecked())
        settings.setValue("savePath", self.ui.filePathTextBox.text())

    def quit_window(self):
        tb_window.close()

    def update_quality_slider(self, value):
        self.ui.qualitySpinBox.setValue(value)
    def update_quality_spinbox(self, value):
        self.ui.qualitySlider.setValue(value)

    def update_display_size(self, index):
        if index == 0:
            self.ui.widthSpinBox.setEnabled(True)
            self.ui.heightSpinBox.setEnabled(True)
        if index == 1:
            self.ui.widthSpinBox.setEnabled(False)
            self.ui.heightSpinBox.setEnabled(False)

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

class OpenTinyblastOptions(ompx.MPxCommand):
    def __init__(self):
        ompx.MPxCommand.__init__(self)

    def doIt(self, args):
        show_my_window()

def cmdCreator():
    return ompx.asMPxPtr(OpenTinyblastOptions())

def create_custom_shelf():
    # Check if the shelf already exists
    shelf_name = "Tinyblast"
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name)  # Delete the existing shelf (if you want to reset it)

    # Create a new shelf
    cmds.shelfLayout(shelf_name, parent="ShelfLayout")

    # Add a button to the shelf (this will call your UI function)
    cmds.shelfButton(
        label="Tinyblast",
        annotation="Open Tinyblast UI",  # Tooltip text
        image="pythonFamily.png",  # You can replace this with any icon you want
        command="cmds.openTinyblastOptions()"  # Command to open your UI
    )

def initializePlugin(mobject):
    global tinyblast_instance
    tinyblast_instance = Tinyblast()
    try:
        mplugin = ompx.MFnPlugin(mobject, "Jack Christensen", "2.0.0-beta", "Any")
        mplugin.registerCommand("tinyblast", Tinyblast.cmdCreator)
        mplugin.registerCommand("openTinyblastOptions", cmdCreator)
        om.MGlobal.displayInfo("Tinyblast plugin loaded.")
    except Exception as e:
        om.MGlobal.displayError(f"Failed to initialize plugin: {str(e)}")
        raise
    create_custom_shelf()

def uninitializePlugin(mobject):
    try:
        mplugin = ompx.MFnPlugin(mobject)
        tb_window.close()
        mplugin.deregisterCommand("tinyblast")
        mplugin.deregisterCommand("openTinyblastOptions")
        om.MGlobal.displayInfo("Tinyblast plugin unloaded.")
    except Exception as e:
        om.MGlobal.displayError(f"Failed to uninitialize plugin: {str(e)}")
        raise