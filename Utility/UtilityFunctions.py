"""
Description: This python file provides utility functions that are used throughout my software. 

Date Created: 10/18/22 
Date Updated: 11/22/22
"""


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


# Find the main window  https://forum.qt.io/topic/84824/accessing-the-main-window-from-python
def findMainWindow():
    """Global function to find the (open) QMainWindow in application"""
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
