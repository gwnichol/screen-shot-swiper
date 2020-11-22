import numpy as np
# import os
import io  # For io.BytesIO
import subprocess
import sys
import time
from telnetlib import Telnet
from signal import signal, SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM
from PIL import Image

if(len(sys.argv) >= 2):
    book_name = sys.argv[1]
else:
    book_name = "unknown-book"

monkey_proc = subprocess.Popen(["adb", "shell",
                                "monkey -p \"com.overdrive.mobile.android.mediaconsole\" --port 1080"],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)

subprocess.run(["adb", "forward", "tcp:1080", "tcp:1080"],
               stdout=subprocess.DEVNULL)

time.sleep(1)

tn = Telnet("localhost", 1080)

starttime = time.time()

def clean(*args):
    print("\nCompleted")
    # Clean up
    tn.close()
    monkey_proc.kill()
    subprocess.run(["adb", "forward", "--remove", "tcp:1080"],
                   stdout=subprocess.DEVNULL)

    # Telling the adb process to close doesn't kill the monkey process
    subprocess.run(["adb", "shell", "kill $(pgrep monkey)"],
                   stdout=subprocess.DEVNULL)
    sys.exit(0)

for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, clean)

time.sleep(1)

def swipe_right():
    #tn.write(("tap 1000 250\n").encode())
    tn.write(("press 22\n").encode())
    #for i in np.linspace(1000, 500):
    #    tn.write(("touch move %d 250\n" % (i)).encode())
#
 #   tn.write(("touch up %d 250\n" % (i)).encode())


def screenshot(path):
    subprocess.run(["adb", "shell", "screencap", path],
                   stdout=subprocess.DEVNULL)

i = 0;

subprocess.run(["adb", "shell", "mkdir", "/storage/self/primary/Pictures/Screenshots/%s" % (book_name)],
               stdout=subprocess.DEVNULL)

while(1):
    screenshot("/storage/self/primary/Pictures/Screenshots/%s/%s-%04d.png" % (book_name, book_name, i))
    i = i + 1
    swipe_right()
    time.sleep(0.75)

clean()
