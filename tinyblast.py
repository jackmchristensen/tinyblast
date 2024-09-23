import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
import os
import subprocess
import sys

def get_plugin_directory():
    # Get the path of the currently loaded plugin
    plugin_name = "tinyblast"
    plugin_path = cmds.pluginInfo(plugin_name, query=True, path=True)
    return os.path.dirname(plugin_path)

def custom_playblast(*args, **kwargs):
    print("Running playblast...")

    kwargs['format'] = 'avi'
    kwargs['percent'] = 100
    kwargs['quality'] = 100
    kwargs['widthHeight'] = (1920, 1080)

    result = cmds.playblast(*args, **kwargs)
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
    custom_playblast()

def get_playblast_options_window():
    # Check if the Playblast Options window is open
    windows = cmds.lsUI(windows=True)
    for window in windows:
        if cmds.window(window, query=True, title=True) == "Playblast Options":  # Exact title match
            return window
    return None

def setup_script_job(playblast_job_id):
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
        print("Executing custom playblast command.")
        custom_playblast()

def tinyblastCmd():
   return ompx.asMPxPtr(Tinyblast())

def initializePlugin(mobject):
    try:
        mplugin = ompx.MFnPlugin(mobject, "Jack Christensen", "1.0.1", "Any")
        mplugin.registerCommand("tinyblast", tinyblastCmd)
        om.MGlobal.displayInfo("Tinyblast plugin loaded.")
        playblast_job_id = None
        setup_script_job(playblast_job_id)
    except Exception as e:
        om.MGlobal.displayError(f"Failed to initialize plugin: {str(e)}")
        raise

def uninitializePlugin(mobject):
    try:
        mplugin = ompx.MFnPlugin(mobject)
        mplugin.deregisterCommand("tinyblast")
        om.MGlobal.displayInfo("Tinyblast plugin unloaded.")
    except Exception as e:
        om.MGlobal.displayError(f"Failed to uninitialize plugin: {str(e)}")
        raise