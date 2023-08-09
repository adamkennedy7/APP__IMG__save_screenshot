import os
import PIL.ImageGrab
from FCN__datetime__now import now

IMG = PIL.ImageGrab.grab()
IMG.filename = "IMG__SCREENSHOT__" + str(now())
IMG.filetype = "png"

script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, "IMG", IMG.filename + "." + IMG.filetype)

print("SAVING " + save_path)
IMG.save(save_path)