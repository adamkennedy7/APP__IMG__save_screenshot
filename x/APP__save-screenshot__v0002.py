import os
import PIL.ImageGrab
from FCN__datetime__now import now

IMG = PIL.ImageGrab.grab()
IMG.filename = "IMG__SCREENSHOT__" + str(now())
IMG.filetype = "png"

script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, "IMG", IMG.filename + "." + IMG.filetype)

print("SAVING " + save_path)
IMG.save(save_path)import os
import configparser
import PIL.ImageGrab
import logging
from FCN__datetime__now import now

# Configuration Loading
config = configparser.ConfigParser()
config.read('config.ini')

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

        logging.info("SAVING " + save_path)
        IMG.save(save_path)
        
        return True

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False

if __name__ == '__main__':
    result = save_screenshot()
    if result:
        logging.info("Screenshot saved successfully!")
    else:
        logging.error("Screenshot saving failed.")
