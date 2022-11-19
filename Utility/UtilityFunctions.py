from datetime import datetime
from uuid import uuid4
import os
import sys

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *



# Remove all spacing on layout
def LayoutRemoveSpacing(QLayout_):
    QLayout_.setSpacing(0)
    QLayout_.setContentsMargins(0, 0, 0, 0)


#https://forum.qt.io/topic/84824/accessing-the-main-window-from-python
# Find the main window
def findMainWindow():
    # Global function to find the (open) QMainWindow in application
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None

def GenerateID():
    return str(uuid4())

def GetFileType(string:str):
    split_tup = os.path.splitext(string)
    return  split_tup[1]



def openFile(file):
    if sys.platform == 'linux2':
        subprocess.call(["xdg-open", file])
    else:
        os.startfile(file)
