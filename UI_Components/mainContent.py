"""
Description: This python file provides the top level and main structure of this PySide application.  

Date Created: 9/27/22 
Date Updated: 10/15/22
"""

# --Imports--
from json import *

#PySide
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

# Custom Imports
from Utility.UtilityFunctions import *
from Utility.ManageJSON import *

#Components Used:
from UI_Components.TopBar.main_topBar import *
from UI_Components.Canvas.main_Canvas import *

class MainContent(QWidget):
    FinishedInitializing = Signal() # When software finishes initialization, emit this signal
    def __init__(self, parent) -> None:
        """This class contains layout with TopBar and MainCanvas. Provides the main structure and layout of the application."""
        super().__init__(parent)

        # Set Attributes
        self.setAttribute(Qt.WA_StyledBackground, True) # Allow background color
        self.setStyleSheet("background-color: #1F2123; border: none") # 1a1c1e

        # Properties
        self.isCanvasEmpty = True
        self.JSONData = LoadJSON(DefaultJSONProjectLocation)
        self.tabHashTable = LoadTabs(self.JSONData)
        self.nodeHashTable = LoadNodes(self.JSONData)

        # Elements
        self.topBar = MainTopBar(self, tabsData = GetTabs(self.JSONData), projectName = GetProjectName(self.JSONData), selectedTab = GetSelectedTab(self.JSONData))  # Top Bar 
        self.canvas = MainCanvas(self, self.nodeHashTable, canvasSize= self.JSONData["canvasSize"])  # Main Canvas

        # Layouts
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.topBar)  # Add Top Bar
        vLayout.addWidget(self.canvas)  # Add Canvas 
        LayoutRemoveSpacing(vLayout)

        # Signals
        self.FinishedInitializing.emit()    # Emit signal when main content has finished initialization

    def TabSelected(self, tabID : str):
        """When a tab is selected in 'self.topBar', a signal will be emitted, calling this function.
        
        Arg:
            tabID (str) : The tabID to set to selected.
        """
        self.canvas.TabSelected(self.tabHashTable[tabID])


    def setCanvasEmpty(self, isCanvasEmpty: bool):
        """Set if the canvas has no CanvasItems.
        This is used to tell the paint event to draw text telling the user to add an item.

        Arg:
            isCanvasEmpty (bool) : If no items on canvas, this is set to true.
        """
        self.isCanvasEmpty = isCanvasEmpty
        self.update()

    # Events:
    def paintEvent(self, event) -> None:
        """If no items are present, paint text to tell user to drag in file or add item."""
        painter = QPainter(self)

        if self.isCanvasEmpty:  # If canvas is empty, tell user to add a canvas item.
            # Paint Text
            painter.setPen(QColor(255, 255, 255, 180))
            painter.setFont(QFont(fontFamily, 13))
            painter.drawText(0, topBarHeight, self.canvas.rect().width(), self.canvas.rect().height(), Qt.AlignCenter, "Drag in file or right-click to add item") # This sets the position and sets the text when no canvas items are present


        return super().paintEvent(event)