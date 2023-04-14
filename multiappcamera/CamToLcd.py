import os.path
from ws1in44lcd import LCD
from pathlib import Path
import time

from picamera2 import Picamera2, Preview

def start():

    # tuning file provided by vendor
    tuning_file =os.path.join(Path.cwd(),"Arducam-477M.json")
    tuning = Picamera2.load_tuning_file(tuning_file)
    algo = Picamera2.find_tuning_algo(tuning, "rpi.agc")

    # create a cam instance
    picam2 = Picamera2(tuning=tuning)
    preview_config = picam2.create_preview_configuration(main={"size": (128, 128)})
    picam2.configure(preview_config)
    picam2.start_preview(Preview.NULL)
    picam2.start()
    time.sleep(2)

    # Setup the display https://github.com/tsbarnes/ws1in44lcd/blob/main/src/ws1in44lcd/demo.py
    display = LCD.LCD()
    display.init(LCD.SCAN_DIR_DFT)
    display.clear()

    # Image to display screen
    while True:
        try:
            # picam2.capture_file("/mnt/ramdisk/cam.jpg")
            # get an image then send to the display. no saving to disk
            image = picam2.capture_image()
            display.show_image(image)
        except (KeyboardInterrupt):
            break

    display.clear()
    print("Closing app")
    picam2.close()
