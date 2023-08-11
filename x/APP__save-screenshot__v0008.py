# TO DO
"""
- Refactor the approach to getting formatted strings from dictionaries
- Add verbose level 0 logs to indicate single-word tags like INITIALIZING, CAPTURING, SAVING, ANALYZING, LOGGING
- Create a helper function which will turn a os.path into an array like []





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

# Clear the terminal
os.system('cls')
print("TIME BEGIN: " + t)
print("\n||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n")

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
    return f"{elapsed_time:.10f} seconds"

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
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, LOG_DIRECTORY, "LOG__" + now() + ".txt")

logging.basicConfig(filename=log_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Prints information to the terminal and a log file
def log_message(message, level=0, marker="", comment=""):
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

    if comment: msg_line += "\n\n" + comment + "\n\n"

    msg_line += breaks

    if VERBOSE_LEVEL >= level:
        print(msg_line)
    
    # Log everything, regardless of verbose level. 
    logging.info(msg_line)

    # SAVE a history.log file to the \LOG directory

log_message("INITIALIZING", level=0, marker="")

# LOG LEVEL 3
# app config info, EDIT CODE HERE to refactor the parsing of dictionaries to strings, via a helper function called dict_to_indented_string(dict, level=3, marker="-") which applies the indents similar to `log_message(f"{key}: {value}", level=3)`
if VERBOSE_LEVEL >= 3:
    log_message("Reading config.ini:", 2)
    for key, value in config[DEFAULT].items():
        log_message(f"{key}: {value}", level=3)

def analyze_image(image, save_path):
    """
    Analyze the given image for various attributes.
    Returns a dictionary with the findings.
    """
    stats = ImageStat.Stat(image)
    width, height = image.size
    file_size = os.path.getsize(save_path)  # Use the save_path to get the file size

    findings = {
        'Resolution': f"{width}x{height}",
        'File Size': f"{file_size / 1024:.2f} KB",
        'Mean Color': stats.mean,
        'Extrema': stats.extrema,
    }
    
    return findings

def save_screenshot():
    """
    Capture and save a screenshot.
    """
    log_message("Attempting to capture screenshot...", level=2)
    
    try:
        IMG = ImageGrab.grab()
        IMG.filename = FILENAME_PREFIX + str(now())
        IMG.filetype = IMG_TYPE

        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_dir, SAVE_DIRECTORY, IMG.filename + "." + IMG.filetype)

        log_message(f"Saving screenshot to {save_path}...", 3, "+")
        IMG.save(save_path)

        # Verbose Level 4: Analyze the image and print attributes
        if VERBOSE_LEVEL >= 4:
            findings = analyze_image(IMG, save_path)
            for key, value in findings.items():
                log_message(f"{key}: {value}", level=4)
        
        log_message(f"Screenshot saved successfully at {save_path}", level=1)
        print("\n||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n")
        print("TIME COMPLETE: " + str(now()))
        print("\t--> COMPLETED IN " + stopwatch() + "\n")
        return True

    except Exception as e:
        error_message = f"An error occurred: {type(e).__name__} - {e}"
        log_message(error_message, level=1)
        return False
    

if __name__ == '__main__':
    result = save_screenshot()
    if not result:
        log_message("Screenshot saving failed.", level=1)
    
    # Verbose Level 6: Gather and print system info
    if VERBOSE_LEVEL >= 6:
        system_info = SYSTEM_INFO
        for key, value in system_info.items():
            log_message(f"{key}: {value}", level=6)
