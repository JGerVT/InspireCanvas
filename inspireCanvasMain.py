""" 
Description:    This python file creates the window that the program will be set in.
                This file is the first file of the software, which can be executed.

Date Created: 9/27/22 
Date Updated: 9/28/22
"""

# --Imports--
import sys

#PySide
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

# Custom Imports
from Settings.settings import *

#Components Used:
from UI_Components.mainContent import *
from Utility.SideGrips import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        '''Main Software Initialization - This is a required function that is called to create a new Window. 

        Attributes:
            self.mainTopLayout (QWidget): The central QWidget of the main window
        '''
        super(MainWindow, self).__init__(*args, **kwargs)

        # Set Attributes
        self.SetStyleSheet("Settings\style.qss")
        self.setWindowTitle("Inspire Canvas")
        self.setWindowIcon(QIcon(softwareIconLocation))
        self.resize(startingWindowSize[0], startingWindowSize[1])   # Set default window size to window size set in settings
        self.setMinimumSize(650,400)

        # ----- Frameless code from https://stackoverflow.com/a/62812752 -----
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.gripSize = 7
        self.grips = []
        self.sideGrips = [
            SideGrip(self, Qt.LeftEdge), 
            SideGrip(self, Qt.TopEdge), 
            SideGrip(self, Qt.RightEdge), 
            SideGrip(self, Qt.BottomEdge), 
        ]

        self.cornerGrips = [QSizeGrip(self) for i in range(4)]

        for i in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)
            self.cornerGrips[i].setStyleSheet("""
                background-color: transparent; 
            """)

        # Central Widget
        self.mainContent = MainContent(self)
        self.setCentralWidget(self.mainContent)

    def SetStyleSheet(self, styleLocation):
        '''Load QSS Theme and set as MainWindow stylesheet

        Args:
            styleLocation (string): the .qss file location to be set as the MainWindow stylesheet
        '''
        with open(styleLocation, 'r') as f:
            style = f.read()
            
            self.setStyleSheet(style)

    # Grips and Side grips
    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        # top left grip doesn't need to be moved...
        # top right
        self.grips[1].move(rect.right() - self.gripSize, 0)
        # bottom right
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grips[3].move(0, rect.bottom() - self.gripSize)

    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        """Update position of all grips"""
        for grip in self.cornerGrips:
            grip.raise_()
        for grip in self.sideGrips:
            grip.raise_()

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
            -self.gripSize, -self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(
            QRect(outRect.topLeft(), inRect.topLeft()))
        # top right
        self.cornerGrips[1].setGeometry(
            QRect(outRect.topRight(), inRect.topRight()).normalized())
        # bottom right
        self.cornerGrips[2].setGeometry(
            QRect(inRect.bottomRight(), outRect.bottomRight()))
        # bottom left
        self.cornerGrips[3].setGeometry(
            QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(), 
            inRect.top(), self.gripSize, inRect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(), 
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        self.updateGrips()

# Execute software.
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

