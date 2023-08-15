APP_NAME = "APP__save-screenshot.py"
VERSION = "tMZaf6s"

import time
from FCN__time__t62 import t62

t = str(time.strftime('%Y%m%d%H%M%S'))
T62 = t62()

import os
import configparser
from PIL import ImageGrab, ImageStat
from PIL import ImageEnhance, ImageFilter
import logging
import platform
import psutil
from prettytable import PrettyTable
from screeninfo import get_monitors


# todo use this to manage the success vs fail line at very end
ERROR_CODE = 0



# begin stopwatch for performance tracking
start_time = time.perf_counter()
perf_counter_stop = 0
def stopwatch():
    elapsed_time = time.perf_counter() - start_time
    return f"{elapsed_time:.10f}"

# get the path of this python file
PY = os.path.abspath(__file__)

# Constants for configuration keys, pulled from __config.ini
DEFAULT = 'DEFAULT'
ENABLE_LOGGING = 'EnableLogging'
IMAGE_TYPE = 'ImageType'
IMG_DIRECTORY = 'SaveDirectory'
LOG_DIRECTORY = 'LogDirectory'
FILENAME_PREFIX = 'FilenamePrefix'
VERBOSE = 'Verbose'
DIVIDER_CHAR = 'DividerChar'
DIVIDER_NUM = 'DividerNum'
INDENT_CHAR = 'IndentChar'
INDENT_SPACES = 'IndentSpaces'

# main path to pull config file from, also basis for IMG and LOG folders
MAIN_PATH = os.path.dirname(PY)

# get the system info for verbose logging
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

# define how to load the config file
def load_config_ini():
    """
    Load application configurations from config.ini.
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(MAIN_PATH, '__config.ini')
    
    if not config.read(config_path):
        raise ValueError(f"Failed to read config file at {config_path}")
    
    return config

# load the config file
config = load_config_ini()

# define various constants
ENABLE_LOGGING = config[DEFAULT][ENABLE_LOGGING]
IMG_TYPE = config[DEFAULT][IMAGE_TYPE]
IMG_DIRECTORY = config[DEFAULT][IMG_DIRECTORY]
LOG_DIRECTORY = config[DEFAULT][LOG_DIRECTORY]
FILENAME_PREFIX = config[DEFAULT][FILENAME_PREFIX]
VERBOSE_LEVEL = int(config[DEFAULT][VERBOSE])
DIVIDER_CHAR = config[DEFAULT][DIVIDER_CHAR]
DIVIDER_NUM = int(config[DEFAULT][DIVIDER_NUM])
INDENT_CHAR = config[DEFAULT][INDENT_CHAR]
INDENT_SPACES = int(config[DEFAULT][INDENT_SPACES])
LOG_PATH = os.path.join(MAIN_PATH, LOG_DIRECTORY, f"LOG__{t}.log")
IMG_PATH = os.path.join(MAIN_PATH, IMG_DIRECTORY, f"IMG__{t}.png")

# setup the logging system which prints to terminal and will save a text file later.
def configure_logging():
    log_path = os.path.join(MAIN_PATH, LOG_DIRECTORY, "LOG__" + t + ".log")
    logging.basicConfig(filename=log_path, level=logging.NOTSET,
                        format='%(asctime)s - %(message)s')

# run the logging setup
configure_logging()

### FCN__log.py
# todo refactor
def log(level, message, emoji=""):
    # Check if ENABLE_LOGGING is False
    if ENABLE_LOGGING == 'False':
        return

    msg = message

    # handle ints
    if isinstance(msg, int):
        msg = str(msg)
        
    # handle lists
    elif isinstance(msg, list):
        for item in msg:
            message = DIVIDER_CHAR + "\t" + str(item)
            log(level, message, emoji)
        return
    
    # handle dictionaries
    elif isinstance(msg, dict):
        table = PrettyTable()
        table.field_names = ["Key", "Value"]
        
        # Set alignment to the left for both columns
        table.align["Key"] = "l"
        table.align["Value"] = "l"
        
        for k, v in msg.items():
            # Handle nested dictionaries and lists
            if isinstance(v, dict) or isinstance(v, list):
                nested_table = PrettyTable()
                nested_table.field_names = ["Index", "Value"]  # Change the heading to "Index"
                nested_table.align["Index"] = "l"
                nested_table.align["Value"] = "l"

                if isinstance(v, dict):
                    for nested_k, nested_v in v.items():
                        nested_table.add_row([nested_k, nested_v])
                elif isinstance(v, list):
                    for idx, item in enumerate(v):
                        nested_table.add_row([str(idx), item])
                    nested_table.junction_char = "-"
                    nested_table.horizontal_char = "-"
                    nested_table.padding_width = 1
        
                table.add_row([k, nested_table])
            else:
                table.add_row([k, v])
        


        table.junction_char = "|"
        table.horizontal_char = "|"
        table.padding_width = 3

        table_string = str(table)
        table_lines = table_string.split('\n')
        for line in table_lines:
            log(level, line, emoji)
        # Customize the table junction characters and horizontal padding
        
        return
    
    # Check for emoji
    if emoji:
        msg = emoji + "  " + msg

    # Shortcut for adding stopwatch to intermediate success flag
    if msg == "Success":
        msg = "✔️  at " + stopwatch() + " sec"

    # build indentation per line
    indent = (INDENT_CHAR + " " * INDENT_SPACES) * level

    # build a divider if the input is "---"
    if msg == "---" and VERBOSE_LEVEL > 0:
        msg_line = "\n" + DIVIDER_CHAR * DIVIDER_NUM + "\n"
        print(msg_line)
        logging.info(msg_line)
        return

    msg_line = indent + msg

    if level==1:
        msg_line += f""

    if VERBOSE_LEVEL >= level:
        print(msg_line)
    
    logging.info(msg_line)
print()
log(0, f"Running {APP_NAME}", "▶️")
log(1, f"Time begin: {t}")
log(2, f"T62: {T62}")

log(1, "---")

log(1, "INITIALIZING", "▶️")
log(2, f"Script path: {PY}", "📂")
log(3, "SYSTEM_INFO")
log(3, SYSTEM_INFO, "ℹ️")
log(3, "NETWORK_INFO", "🌐")
log(3, "coming soon")

def ok(level = 0):
    log(level,f"⏱️  {stopwatch()} sec","")

def get_display_info():
    primary_monitor = get_monitors()[0]  # Get the primary monitor (monitor 0)

    monitor_info = {
        "name": primary_monitor.name,
        "width": primary_monitor.width,
        "height": primary_monitor.height,
        "width_mm": primary_monitor.width_mm,    # Width in millimeters
        "height_mm": primary_monitor.height_mm,  # Height in millimeters
        "is_primary": primary_monitor.is_primary,
    }

    return monitor_info

log(3, "DISPLAY_INFO")
DISPLAY_INFO = get_display_info()
log(3, DISPLAY_INFO, "🖥️")


log(2, f"Logging to ------ {MAIN_PATH}\{LOG_DIRECTORY}")

def get_screenshot():
    global perf_counter_stop
    ok(2)
    log(1, "CAPTURING", "📷")
    log(2, "Capturing a screenshot..")
    try:
        perf_counter_stop = stopwatch()
        
        image = ImageGrab.grab()
        # Collect image information into a dictionary
        image_info = {
            "Image Size": str(image.size),
            "Color Mode": image.mode,
            "Memory Address": hex(id(image)),
            "Image Format": str(image.format),
            "Meta Information": str(image.info),
        }

        # Log the image information using the log function
        log(3, image_info, "↪️")

        log(3, "Success")
        return image
    except Exception as e:
        error_message = f"\n\nAn error occurred: {type(e).__name__} - {e}\n\n"
        log(1, error_message)
        return False

def save_screenshot(image):
    log(2, f"Saving screenshot to {IMG_DIRECTORY}")
    image.save(IMG_PATH)
    log(3, f"IMG saved {IMG_PATH}")
    
    # Count the number of files beginning with "IMG__" adjacent to the image at IMG_PATH
    img_file_count = sum(1 for file in os.listdir(MAIN_PATH + "\\" + IMG_DIRECTORY) if file.startswith("IMG__"))
    log(4, f"IMG file count: {img_file_count}")
    
    log(3, "Success")
    log(1, f"CAPTURED SUCCESSFULLY in {perf_counter_stop} seconds.", "🖼️")


def analyze_image(image, file_path):
    stats = ImageStat.Stat(image)
    width, height = image.size
    file_size = os.path.getsize(file_path)  # Use the passed file path

    # Brightness: Average brightness of the image (1 is original brightness)
    brightness = ImageEnhance.Brightness(image)
    avg_brightness = sum(brightness.enhance(1).convert("L").point(lambda p: p).getdata()) / (width * height)

    # Contrast: Average contrast of the image (1 is original contrast)
    contrast = ImageEnhance.Contrast(image)
    avg_contrast = sum(contrast.enhance(1).convert("L").point(lambda p: p).getdata()) / (width * height)

    # Sharpness: Average sharpness of the image (1 is original sharpness)
    sharpness = ImageEnhance.Sharpness(image)
    avg_sharpness = sum(sharpness.enhance(1).convert("L").point(lambda p: p).getdata()) / (width * height)

    # Entropy: Measures the amount of information/randomness in the image
    entropy = image.entropy()

    findings = {
        'Resolution': f"{width}x{height}",
        'File Size': f"{file_size / 1024:.2f} KB",
        'Mean Color': stats.mean,
        'Extrema': stats.extrema,
        'Brightness': avg_brightness,
        'Contrast': avg_contrast,
        'Sharpness': avg_sharpness,
        'Entropy': entropy,
    }
    
    return findings

# take the screenshot now

image = get_screenshot()
save_screenshot(image)  # Save the image before analyzing

if VERBOSE_LEVEL > 1:
    # log the image analysis
    log(2, "Analyzing IMG file..")
    image_data = analyze_image(image, IMG_PATH)  # Pass the path to the saved image
    log(3, image_data, "🔬")
    log(3, "Success")

log(1, "---")
log(0, f"COMPLETE", "✅")
#State the result
log(1, f"IMG__SCREENSHOT saved to {MAIN_PATH}\{IMG_DIRECTORY}", "⤵️")
log(1, f"Completed {APP_NAME} at {MAIN_PATH}", "⏹️")
log(2, f"Run time {stopwatch()} seconds", "⌚")
log(3, f"T62={t62()}")

log(1, "---")