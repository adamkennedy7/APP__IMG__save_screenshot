import os
import configparser
import PIL.ImageGrab
import logging
from FCN__datetime__now import now

# Configuration Loading
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(config_path)

if not config.read(config_path):
    raise ValueError(f"Failed to read config file at {config_path}")

for section in config.sections():
    print(section, dict(config[section]))

IMG_TYPE = config['DEFAULT']['ImageType']
SAVE_DIRECTORY = config['DEFAULT']['SaveDirectory']
LOG_FILE = config['DEFAULT']['LogFile']
FILENAME_PREFIX = config['DEFAULT']['FilenamePrefix']

# Logging Configuration
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def save_screenshot():
    try:
        IMG = PIL.ImageGrab.grab()
        IMG.filename = FILENAME_PREFIX + str(now())
        IMG.filetype = IMG_TYPE

        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_dir, SAVE_DIRECTORY, IMG.filename + "." + IMG.filetype)

        logging.info("IMG saved " + save_path)
        IMG.save(save_path)
        
        return True

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False

if __name__ == '__main__':
    result = save_screenshot()
    if not result:
        logging.error("Screenshot saving failed.")