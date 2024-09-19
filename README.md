# Tinyblast v1.0.0

# **Important!**

FFmpeg is no longer bundled with Tinyblast directly in the source. In order to download the plugin with FFmpeg please go to the [release page on this repo](https://git.jackmchristensen.com/jack/tinyblast/-/releases/v1.0.0) and download tinyblast_v1.0.0.zip or download it [here](https://drive.proton.me/urls/JVV34W2H3R#VOJzkesz0Cgq). If you only download the source, the plugin **will not work**.

## Overview

Tinyblast is a lightweight plugin designed to enhance Maya’s playblast workflow by converting uncompressed `.avi` files to compressed `.mp4` files using the efficient H.264 codec. It adds a custom button to Maya's Playblast Options window, enabling users to save playblasts in the more storage-friendly `.mp4` format, significantly reducing file sizes without sacrificing quality.

## Features

- **Playblast to MP4 Conversion**: Automatically converts uncompressed `.avi` playblast files generated by Maya to `.mp4` format using the H.264 (libx264) codec.
- **Seamless Integration**: Adds a custom button to Maya's Playblast Options window for quick access to conversion options.
- **Improved File Size Efficiency**: Compresses uncompressed `.avi` files, which Maya creates by default, into `.mp4` files with minimal quality loss, freeing up disk space and improving workflow efficiency.

## Known Limitations

- **Windows Only**: This release is optimized for Maya’s `.avi` file output on Windows. Future versions may extend support to other platforms and formats.
- **Uncompressed AVI Temporary File**: Tinyblast relies on Maya’s built-in playblast function, which still generates an uncompressed `.avi` file before converting it to `.mp4`. This `.avi` file is temporary and will be deleted by Maya after a few minutes.

## Installation

1. Download and install Tinyblast.
2. **Load the Plugin in Maya**:
   - Navigate to `Windows > Settings/Preferences > Plug-in Manager`.
   - If `Tinyblast.py` is not listed, click **Browse** and locate the `Tinyblast.py` file.
   - Check the **Loaded** box to enable the plugin.
   - (Optional) Check **Auto-load** to automatically load the plugin every time Maya starts.
3. Access the Playblast Options window in Maya. A new "Tinyblast" button will now be available to convert playblasts to `.mp4`.

## License

This project is licensed under the GPLv3 license.

## Acknowledgments

This project uses the following third-party libraries:

- **FFmpeg**: Licensed under the [GNU General Public License (GPL)](https://ffmpeg.org/legal.html). FFmpeg is a powerful multimedia framework used in this project for video conversion.
- **Qt6**: Licensed under the [GNU Lesser General Public License (LGPL) v3](https://www.qt.io/licensing). Qt is used for building the user interface of this project.
- **PySide6**: Licensed under the [GNU Lesser General Public License (LGPL) v3](https://doc.qt.io/qtforpython/licenses.html). PySide6 provides Python bindings for the Qt framework.
- **Shiboken6**: Licensed under the [GNU Lesser General Public License (LGPL) v3](https://doc.qt.io/qtforpython/shiboken6/). Shiboken6 is used for generating Python bindings for Qt.

Please refer to the respective licenses for each library for more information.
