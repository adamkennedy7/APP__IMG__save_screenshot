APP_NAME = "APP__save-screenshot.py"

"""

TO DO
[i] Refactor the approach to getting formatted strings from dictionaries in a function like log_dict(dict, level=3, marker="-") which returns a string that represents the dictionary including indents via the `marker[0]` character
//[u] Add verbose level 0 logs to indicate single-word tags like INITIALIZING, CAPTURING, SAVING, ANALYZING, LOGGING
    [i] Add some more logs with various levels of verbosity as you see fit, but keep in mind: 1 should be single words, upper-case, 2 is the user-friendly input and output dialogs
[i] Create a helper function which will turn a os.path into an array like ["O:","DAT","OneDrive","CODE","py","APP__IMG__save-screenshot","IMG","IMG__SCREENSHOT__20230809-024609.png"]
[i] Create a "NETWORK_INFO" dictionary which provides network information like IP address, user name and info, etc. So we can print log(log_dict(NETWORK_INFO), 8)
//[u] Define a constant PY as the full path of the current python script that is being executed
    [i]improve so that it also shows the .py file as well as the abspath
[i] Helper function called `dict__log(path__dict(save_path))` which would get a dictionary from a path, and then a formatted string from the dictionary!

"""

import os
import time
import configparser
from PIL import ImageGrab, ImageStat
import logging
from FCN__datetime__now import now
import platform
import psutil
from FCN__time__t42 import t42

t = str(now())
PY = os.path.dirname(os.path.abspath(__file__))

# Clear the terminal
os.system('cls')

# Constants for configuration keys
DEFAULT = 'DEFAULT'
IMAGE_TYPE = 'ImageType'
SAVE_DIRECTORY = 'SaveDirectory'
LOG_DIRECTORY = 'LogDirectory'
    #LOG_FILE = 'LogFile'
FILENAME_PREFIX = 'FilenamePrefix'
VERBOSE = 'Verbose'

# Begin stopwatch
start_time = time.perf_counter()
def stopwatch():
    elapsed_time = time.perf_counter() - start_time
    return f"{elapsed_time:.10f} seconds."

# Not necessary for this current iteration but placing it here for futureproofing. To be refactored and expanded later.
# Get system info for verbose troubleshooting & debugging if necessary
SYSTEM_INFO = {
    'System': platform.uname().system,
    'Node Name': platform.uname().node,
    'Release': platform.uname().release,
    'Version': platform.uname().version,
    'Machine': platform.uname().machine,
    'Processor (Platform)': platform.uname().processor,
    'Processor (PSUtil)': psutil.cpu_freq().current,
    'Physical Cores': psutil.cpu_count(logical=False),
    'Logical Cores': psutil.cpu_count(logical=True)
}

# Define the loading of the configuration
def load_configuration():
    """
    Load application configurations from config.ini.
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    if not config.read(config_path):
        raise ValueError(f"Failed to read config file at {config_path}")
    
    return config

# Load the configuration from config file
config = load_configuration()

# Define config variables as constants
IMG_TYPE = config[DEFAULT][IMAGE_TYPE]
SAVE_DIRECTORY = config[DEFAULT][SAVE_DIRECTORY]
LOG_DIRECTORY = config[DEFAULT][LOG_DIRECTORY]
FILENAME_PREFIX = config[DEFAULT][FILENAME_PREFIX]
VERBOSE_LEVEL = int(config[DEFAULT][VERBOSE])

# Logging Configuration
def configure_logging():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, LOG_DIRECTORY, "LOG__" + now() + ".txt")
    logging.basicConfig(filename=log_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

# Prints information to the terminal and a log file
def log(message, level=1, marker="", comment=""):
    """
    Print and log the provided message based on the verbose level.
    """
    # Get the number of indents and breaks from arg 2
    indent = '|  ' * level
    breaks = ""

    # Add breaks based on verbose level
    #if level<3: breaks = "\n"
    #if level<2: breaks = "\n\n"
    #if level<1: breaks = "\n\n\n"


    # Use a different indentation format if a "marker" is specified    
    if marker: indent = (marker + '  ') * level
    msg_line = breaks + indent + message

    # Add line breaks for formatting
    if comment: msg_line += "\n\n" + comment + "\n\n"
    msg_line += breaks

    if VERBOSE_LEVEL >= level:
        print(msg_line)
    
    # Log everything, regardless of verbose level. 
    logging.info(msg_line)

    # SAVE a history.log file to the \LOG directory
def log_break(): log("\n---\n",1)

# Get the file name / path
log(APP_NAME)
log(PY,2)
log("##todo folder path tree via `dict__log(path__dict(PY))`",3)
log("clock_in = " + t, 2)

log("INITIALIZING...", 1)
log("Reading `config.ini`", 2)
log(str(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')), 3)

# note to self
# config info, EDIT CODE HERE to refactor the parsing of dictionaries to strings, via a helper function called dict_to_indented_string(dict, level=3, marker="-") which applies the indents similar to `log_message(f"{key}: {value}", level=3)`. This would also be helpful at the end when we print the system information

def get_config_ini():
    if VERBOSE_LEVEL >= 3:
        log("[DEFAULT]",4)

        for key, value in config[DEFAULT].items():
            log(f"{key}: {value}", 4)

get_config_ini()


# note to self
# Analysis of a saved image, to expand upon this and refactor later
def analyze_image(image, save_path):
    """
    Analyze the given image for various attributes.
    Returns a dictionary with the findings.
    """
    stats = ImageStat.Stat(image)
    width, height = image.size
    file_size = os.path.getsize(save_path)

    findings = {
        'Resolution': f"{width}x{height}",
        'File Size': f"{file_size / 1024:.2f} KB",
        'Mean Color': stats.mean,
        'Extrema': stats.extrema,
    }
    
    return findings


# to be refactored?
def save_screenshot():
    """
    Capture and save a screenshot.
    """
    log("CAPTURING...")

    log("Attempting to capture screenshot...", 2)
    
    try:
        IMG = ImageGrab.grab()
        IMG.filename = FILENAME_PREFIX + str(now())
        IMG.filetype = IMG_TYPE

        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_dir, SAVE_DIRECTORY, IMG.filename + "." + IMG.filetype)

        log(f"Saving screenshot to {save_path}", 3)
        IMG.save(save_path)
        
        log("SUCCESS.")
        log(f"Saved IMG successfully at {save_path}", level=2)
        log("##todo FOLDER TREE HERE VIA `dict__log(path__dict(save_path))`", 3)

        log("ANALYZING...")
        if VERBOSE_LEVEL >= 4:
            image_data = analyze_image(IMG, save_path) # `dict__log(path__dict(image_data))` 
            for key, value in image_data.items():
                log(f"{key}: {value}", level=3)
        
        log_break()
        log("COMPLETED IN " + stopwatch() + "\n",1)
        log("CURRENT TIME " + str(now()),2)
        return True

    except Exception as e:
        error_message = f"An error occurred: {type(e).__name__} - {e}"
        log(error_message, level=1)
        return False
    

if __name__ == '__main__':
    result = save_screenshot()
    if not result:
        log("Screenshot saving failed.", level=1)
    
    # Verbose Level 6: Gather and print system info
    if VERBOSE_LEVEL >= 6:
        log("SYSTEM_INFO", 5)
        system_info = SYSTEM_INFO
        for key, value in system_info.items():
            log(f"{key}: {value}", level=6)
        print()