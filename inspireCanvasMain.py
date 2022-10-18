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

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        '''
        Main Software Initialization - This is a required function that is called to create a new Window. 

        Attributes:
            self.mainTopLayout (QWidget): The central QWidget of the main window
        '''
        super(MainWindow, self).__init__(*args, **kwargs)

        # Set Attributes
        self.SetStyleSheet("Settings\style.qss")
        self.setWindowTitle("Inspire Canvas")
        self.setWindowIcon(QIcon(softwareIconLocation))
        self.resize(startingWindowSize[0], startingWindowSize[1])   # Set default window size to window size set in settings
    
        # Central Widget
        self.mainContent = MainContent(self)
        self.setCentralWidget(self.mainContent)

    def SetStyleSheet(self, styleLocation):
        '''
        Load QSS Theme and set as MainWindow stylesheet

        Args:
            styleLocation (string): the .qss file location to be set as the MainWindow stylesheet
        '''
        with open(styleLocation, 'r') as f:
            style = f.read()
            
            self.setStyleSheet(style)

# Execute software.
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
