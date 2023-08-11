import os
import configparser
from PIL import ImageGrab
import logging
from FCN__datetime__now import now

# Constants for configuration keys
DEFAULT = 'DEFAULT'
IMAGE_TYPE = 'ImageType'
SAVE_DIRECTORY = 'SaveDirectory'
LOG_FILE = 'LogFile'
FILENAME_PREFIX = 'FilenamePrefix'
VERBOSE = 'Verbose'

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
