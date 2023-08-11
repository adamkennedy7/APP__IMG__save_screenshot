APP_NAME = "APP__save-screenshot.py"

"""

TO DO

[] add directory link at end of log:
    |  APP DIRECTORY
    |  |  o:\DAT\ ...

[] add verbose flag to log name
        "LOG__20230809-020735__lv=9001"

[] fcn_log() adds a verbose log() which states the name of the function containing fcn_log() and its arguments. 

[] Refactor log() and give it logic to determine `msg` and if necessary:
    [] parse int to str
    [] parse array to formatted str with line breaks
    [] parse dict to formatted str with line breaks

[] Create a helper function which will turn a os.path into an array like ["O:","DAT","OneDrive","CODE","py","APP__IMG__save-screenshot","IMG","IMG__SCREENSHOT__20230809-024609.png"]
        # might be able to pull this from `file mermaid`

[] Create a "NETWORK_INFO" dictionary which provides network information like IP address, user name and info, etc. So we can print log(network_info_dict, 8)

[x] Define a constant PY as the full path of the current python script that is being executed
    []improve so that it also shows the .py file as well as the abspath

## FCN__path_to_dictionary(path) to get a file `path` and return a dictionary of arrays with the following key value pairs
        'breadcrumb_index' : [name, file_id] # other info TBD

                ? What else would I want to convert to dictionaries...?

## FCN dict_to_log(dict, n)
    inputs any dictionary like the above `path_to_dictionary()`
    Produces log() lines
    return void 

####################

## Edge cases to check
[] what if it tries to save two within the same second, would it overwrite the other or have an error?





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
# os.system('cls')

# Constants for configuration keys
DEFAULT = 'DEFAULT'
IMAGE_TYPE = 'ImageType'
SAVE_DIRECTORY = 'SaveDirectory'
LOG_DIRECTORY = 'LogDirectory'
FILENAME_PREFIX = 'FilenamePrefix'
VERBOSE = 'Verbose'
DIVIDER_CHAR = 'DividerChar'
DIVIDER_NUM = 'DividerNum'
INDENT_CHAR = 'IndentChar'
INDENT_SPACES = 'IndentSpaces'

# Begin stopwatch
start_time = time.perf_counter()
def stopwatch():
    elapsed_time = time.perf_counter() - start_time
    return f"{elapsed_time:.10f}"
perf_counter_stop = 0

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
def load_config_ini():
    """
    Load application configurations from config.ini.
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '__config.ini')
    
    if not config.read(config_path):
        raise ValueError(f"Failed to read config file at {config_path}")
    
    return config

# Load the configuration from config file
config = load_config_ini()

# Define config variables as constants
IMG_TYPE = config[DEFAULT][IMAGE_TYPE]
SAVE_DIRECTORY = config[DEFAULT][SAVE_DIRECTORY]
LOG_DIRECTORY = config[DEFAULT][LOG_DIRECTORY]
FILENAME_PREFIX = config[DEFAULT][FILENAME_PREFIX]
VERBOSE_LEVEL = int(config[DEFAULT][VERBOSE])
DIVIDER_CHAR = config[DEFAULT][DIVIDER_CHAR]
DIVIDER_NUM = int(config[DEFAULT][DIVIDER_NUM])
INDENT_CHAR = config[DEFAULT][INDENT_CHAR]
INDENT_SPACES = int(config[DEFAULT][INDENT_SPACES])

# Logging Configuration
def configure_logging():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(script_dir, LOG_DIRECTORY, "LOG__" + now() + ".txt")
    logging.basicConfig(filename=log_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

# Prints information to the terminal and a log file
def log(message, level=1, marker="", comment=""):
    #todo : check IF message is a dict, reformat it appropriately with indentation.
    #todo : check IF message is an array, reformat it...
    
    message = str(message)
    # Check for divider line key "---"
    if message == "---":
        if VERBOSE_LEVEL>0: 
            msg_line = "\n"+DIVIDER_CHAR * DIVIDER_NUM+"\n"
            print(msg_line)
            logging.info(msg_line)
            return
    
    """
    Print and log the provided message based on the verbose level.
    """
    # Get the number of indents and breaks from arg 2
    indent = (INDENT_CHAR + " " * INDENT_SPACES) * level
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
    # SAVE LOG TO TXT FILE 
    logging.info(msg_line)

# This is the shortcut for adding a line divider
log("---")

# Log app name information
log(APP_NAME)
log(PY,2)
log("##todo add folder path tree",3)
log("Current time: " + t, 2)

# Print log path to log
log("Logging to: " + os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_DIRECTORY, "LOG__" + now() + ".txt"),2)

log("---")
log("INITIALIZING...", 1)
log("Reading config.ini", 2)
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
    global perf_counter_stop
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
        if VERBOSE_LEVEL >= 2:
            image_data = analyze_image(IMG, save_path) # `dict__log(path__dict(image_data))` 
            for key, value in image_data.items():
                log(f"{key}: {value}", level=2)
        log("RESULTS LOGGED.")
        # Print log path to log
        log("Log file: = " + os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_DIRECTORY, "LOG__" + now() + ".txt"),2)


        log("---")
        log("APP directory: " + script_dir)
        perf_counter_stop = stopwatch()
        log("COMPLETED SUCCESSFULLY in " + perf_counter_stop +  "seconds.\n",1)
        
        log("Python version ")
        log("# path to python.exe")
        log("# list dependencies")
        
        log("---")
        
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
        
    log("\n📷 🤖 ✅ Success at " + perf_counter_stop + " seconds >>> IMG__SCREENSHOT saved to " + os.path.dirname(os.path.abspath(__file__)) + "\\" + SAVE_DIRECTORY + "\n",0)