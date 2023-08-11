import os
import configparser
from PIL import ImageGrab, ImageStat
import logging
from FCN__datetime__now import now
import platform
import psutil

# Constants for configuration keys
DEFAULT = 'DEFAULT'
IMAGE_TYPE = 'ImageType'
SAVE_DIRECTORY = 'SaveDirectory'
LOG_FILE = 'LogFile'
FILENAME_PREFIX = 'FilenamePrefix'
VERBOSE = 'Verbose'

config = {'DEFAULT' : DEFAULT,
          'ImageType' : IMAGE_TYPE,
          'SaveDirectory' : SAVE_DIRECTORY,
          'LogFile' : LOG_FILE,
          'FilenamePrefix' : FILENAME_PREFIX,
          'Verbose' : VERBOSE
}

def gather_system_info():
    """
    Gather system information.
    Returns a dictionary with the findings.
    """
    uname_info = platform.uname()
    
    system_info = {
        'System': uname_info.system,
        'Node Name': uname_info.node,
        'Release': uname_info.release,
        'Version': uname_info.version,
        'Machine': uname_info.machine,
        'Processor (Platform)': uname_info.processor,
        'Processor (PSUtil)': psutil.cpu_freq().current,
        'Physical Cores': psutil.cpu_count(logical=False),
        'Logical Cores': psutil.cpu_count(logical=True)
    }
    
    return system_info

def load_configuration():
    """
    Load application configurations from config.ini.
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    if not config.read(config_path):
        raise ValueError(f"Failed to read config file at {config_path}")
    
    return config

config = load_configuration()

IMG_TYPE = config[DEFAULT][IMAGE_TYPE]
SAVE_DIRECTORY = config[DEFAULT][SAVE_DIRECTORY]
LOG_FILE = config[DEFAULT][LOG_FILE]
FILENAME_PREFIX = config[DEFAULT][FILENAME_PREFIX]
VERBOSE_LEVEL = int(config[DEFAULT][VERBOSE])

# Logging Configuration
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_message(message, level=1):
    """
    Print and log the provided message based on the verbose level.
    """
    if VERBOSE_LEVEL >= level:
        print(message)
    
    # Log everything, regardless of verbose level.
    # If you don't want this, you can add the same verbose condition here.
    logging.info(message)


log_message(f"Reading config.ini ... {str(config)}...", level=3)


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

        log_message(f"Saving screenshot to {save_path}...", level=3)
        IMG.save(save_path)

        # Verbose Level 4: Analyze the image and print attributes
        if VERBOSE_LEVEL >= 4:
            findings = analyze_image(IMG, save_path)
            for key, value in findings.items():
                log_message(f"{key}: {value}", level=4)
        
        log_message(f"Screenshot saved successfully at {save_path}", level=1)
        return True

    except Exception as e:
        error_message = f"An error occurred: {type(e).__name__} - {e}"
        log_message(error_message, level=1)
        return False

if __name__ == '__main__':
    result = save_screenshot()
    if not result:
        log_message("Screenshot saving failed.", level=1)
