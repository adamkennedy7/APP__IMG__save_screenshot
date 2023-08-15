# APP__save-screenshot.py Documentation

Adam Kennedy

Github @adamkennedy7

## Introduction

The `APP__save-screenshot.py` script captures screenshots, analyzes images, and logs various system and image-related information. It is designed to facilitate the process of capturing, saving, and analyzing screenshots efficiently.

## Features

- Capturing screenshots using the `ImageGrab` module.
- Logging system information and script execution details.
- Saving captured screenshots to designated directories.
- Displaying primary monitor information using the `screeninfo` module.
- Analyzing image statistics using the `ImageStat` module.
- Formatting log output using the `prettytable` module.

## Dependencies

The script requires the following Python libraries:

- `PIL` (Python Imaging Library): Used for capturing screenshots, analyzing image statistics, and enhancing images.
- `prettytable`: Used for formatting dictionaries and nested data structures in the log output.
- `psutil`: Used for retrieving system information like CPU details.
- `screeninfo`: Used to gather information about the primary monitor.

## Usage

To execute the script, run it in your Python environment.

Upon execution, the script performs the following actions:

1. Captures a screenshot using the `ImageGrab` module.
2. Logs detailed system information, including operating system details and processor information.
3. Logs primary monitor information, such as name, dimensions, and primary status.
4. Logs image information, including size, color mode, memory address, format, and meta-information.
5. Saves the captured screenshot to a designated directory.
6. Counts the number of "IMG__" files adjacent to the saved image.
7. Calculates and logs the script's execution time.
8. Outputs a completion message with relevant details.

## Customization

You can customize the behavior of the script by modifying the configuration settings in the `__config.ini` file. This includes enabling or disabling logging, specifying directories, and adjusting verbosity levels.

## Credits

- The script's structure and modular design were influenced by the works of Adam Kennedy.
- Various Python libraries were used to enhance functionality, including `PIL`, `prettytable`, `psutil`, and `screeninfo`.
