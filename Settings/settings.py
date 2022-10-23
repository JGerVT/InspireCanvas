"""
Description: This python file provides global variables and references  

Date Created: 9/27/22 
Date Updated: 10/15/22
"""

# Default Imports
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utility.UtilityFunctions import *
from Utility import ConsoleLog

# Software Settings
defaultAccentColor = "#23A0FF"
DefaultJSONProjectLocation = u"Data\defaultDatabase.json"
softwareIconLocation = "Resources\inspireCanvasIcon.png" #Icon Location
startingWindowSize = [1200, 800] # Default software size
MaxSize = 16777215
softwareLogLocation = "Data\softwareLog.log"

#--Top Bar--
topBarHeight = 40 # Height of Top-Bar
tabHeight = 35 #Height of tab
tabWidth = 180
TitleBarTopSpacing = 3
#Window Buttons
NavButtonWidth = 45

#Default Font
fontFamily = u"Segoe UI"


# Canvas
# XYDefaultSize = QSize(5000, 5000)
minMaxZoom = [.05, 5]
cornerResizeButtonRadius = 4
minimumImageSize = [100, 100]   # pixels
defaultImageSize = QSizeF(600, 600)   # Sets the default size of a dragged in image. This ensures that images that are too big default to a smaller size
imageFileTypes = [".jpg", ".png", ".jpeg", ".bmp", ".gif", ".webp"]