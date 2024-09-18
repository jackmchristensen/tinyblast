# Tinyblast Plugin v2.0.0-beta

Tinyblast is a custom playblast tool for Maya, designed to offer more flexible control over the output format, codec, and playblast settings than the default Maya playblast options.

## New in v2.0.0-beta
- Removed the button from the Playblast Options window.
- Created a new custom window that contains options to choose the file format and codec.
- Added playblast options such as:
  - Quality slider
  - Resolution scalar
  - Frame padding

## Known Limitations

- **Windows Only**: This release is optimized for Maya’s `.avi` file output on Windows. Future versions may extend support to other platforms and formats.
- **Uncompressed AVI Temporary File**: Tinyblast relies on Maya’s built-in playblast function, which still generates an uncompressed `.avi` file before converting it to the other format. This `.avi` file is temporary and will be deleted by Maya after a few minutes.

## Known Issues
- The `.mov` format currently does not work with the DNxHD, DNxHR, or ProRes codecs.

## Installation
1. Download and install Tinyblast.
2. **Load the Plugin in Maya**:
   - Navigate to `Windows > Settings/Preferences > Plug-in Manager`.
   - If `Tinyblast.py` is not listed, click **Browse** and locate the `Tinyblast.py` file.
   - Check the **Loaded** box to enable the plugin.
   - (Optional) Check **Auto-load** to automatically load the plugin every time Maya starts.
3. Access the Playblast Options window in Maya.

## How to Use
Currently, there is no menu button to open Tinyblast. You will need to run the following command in Maya's script editor:

```python
import maya.cmds as cmds
cmds.openTinyblastOptions()
```

## Future Plans
- Further improvements to format and codec compatibility.
- Adding more formats and codecs if needed.
- Refining the UI for easier access and use.

## Requirements
- Maya (tested on Maya 2025, but should work with any version that supports the same OpenMaya plugin version).
- FFmpeg bundled with the plugin.