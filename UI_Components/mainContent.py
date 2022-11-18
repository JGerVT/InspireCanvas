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
from UI_Components.ContextMenu.contextMenu import * # Needed for initialization

class MainContent(QWidget):
    FinishedInitializing = Signal() # When software finishes initialization, emit this signal
    def __init__(self, parent) -> None:
        """This class contains layout with TopBar and MainCanvas. Provides the main structure and layout of the application."""
        super().__init__(parent)

        # Set Attributes
        self.setAttribute(Qt.WA_StyledBackground, True) # Allow background color
        self.setStyleSheet("background-color: #1F2123; border: none") # 1a1c1e

        # Properties
        self.isCanvasEmpty = True       # Managed by self.canvas
        self.projectName = "Project"
        self.JSONData = None
        self.tabHashTable = None
        self.nodeHashTable = None
        self.selectedTab = None
        self.canvasSize = None
        self.saveLocation = u"E:\OneDrive\Software Development\Inspire Canvas - Fall 2022\Inspire Canvas - Applied Software Fall 2022\Data\defaultDatabase.json"

        # Elements
        self.topBar = MainTopBar(self, projectName = self.projectName)  # Top Bar 
        self.canvas = MainCanvas(self)  # Main Canvas
        self.zoomButtons = ZoomButtons(self)

        # Layouts
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.topBar)  # Add Top Bar
        vLayout.addWidget(self.canvas)  # Add Canvas 
        LayoutRemoveSpacing(vLayout)

        # INIT
        #! Load settings before loading project
        self.LoadProject(self.saveLocation)

        # Signals
        self.FinishedInitializing.emit()    # Emit signal when main content has finished initialization

    def LoadProject(self, fileLocation: str = "", JSONData = None):
        """This function is what initializes all of the data within the project and calls the functions to set the data for the canvas and Tabs

        Args:
            fileLocation (str): Where the JSON project data is stored.
        """
        # Get Data from JSON File
        if JSONData == None:
            self.JSONData = LoadJSON(fileLocation)
        else:
            self.JSONData = JSONData
        self.tabHashTable = LoadTabs(self.JSONData)
        self.nodeHashTable = LoadNodes(self.JSONData)
        self.projectName = self.JSONData["projectName"]
        self.selectedTab = self.JSONData["selectedTab"]
        self.canvasSize = self.JSONData["canvasSize"]

        # Initialize Data on Tabs and Canvas
        self.topBar.SetTabs(self.tabHashTable, self.selectedTab)
        self.canvas.SetCanvasData(self.nodeHashTable, canvasSize = self.JSONData["canvasSize"])

        # Initialize Tab Selection
        if self.selectedTab in self.tabHashTable:   # Set selected tab to the selectedTab ID.
            self.canvas.TabSelected(self.tabHashTable[self.selectedTab])
        elif len(self.tabHashTable.items()) > 0:    # If selected tabID is not in database and items exist in tab database, set to 0
            self.canvas.TabSelected(self.JSONData["tabs"][0]["tabID"])
        else:
            ConsoleLog.error("Tab Missing", "Tab [" + str(self.selectedTab) + "] not found in 'tabs'.")

    def SaveProject(self, saveLocation: str = None):
        """Save the project to a JSON file.

        Args:
            saveLocation (str): location where the project will be saved.
        """
        if saveLocation == None:    # If no save location is passed, the currently loaded JSON project will be overwritten 
            saveLocation = self.saveLocation

        self.UpdateJSONData()
        try:    # If unable to save the json file, continue
            SaveJSON(self.JSONData, saveLocation)
            self.saveLocation = saveLocation
        except: 
            pass


    def NewProject(self, projectLocation):
        """Create a new project
        """
        tabID = GenerateID()
        newProjectData = NewProjectData("Project", tabID, [100000,100000], [CreateTabData("Tab", tabID, [])], [])["Project"]

        try:    # If unable to save the json file, continue
            SaveJSON(newProjectData, projectLocation)
            self.saveLocation = projectLocation
            self.LoadProject(JSONData = newProjectData)
        except: 
            print("FAILED")
            pass
        

    def TabSelected(self, tabID : str):
        """When a tab is selected in 'self.topBar', a signal will be emitted, calling this function.
        
        Arg:
            tabID (str) : The tabID to set to selected.
        """
        if tabID != self.selectedTab:    # If new tab is selected, select the tab
            self.canvas.TabSelected(self.tabHashTable[tabID])
            self.selectedTab = tabID
            self.JSONData["selectedTab"] = tabID

    def UpdateJSONData(self):
        dictList = []
        for key, value in self.nodeHashTable.items():
            dictList.append(value)
        self.JSONData["nodes"] = dictList

        tabDictList = []
        for key, value in self.tabHashTable.items():
            tabDictList.append(value)
        self.JSONData["tabs"] = tabDictList



    def setCanvasEmpty(self, isCanvasEmpty: bool):
        """Set if the canvas has no CanvasItems.
        This is used to tell the paint event to draw text telling the user to add an item.

        Arg:
            isCanvasEmpty (bool) : If no items on canvas, this is set to true.
        """
        self.isCanvasEmpty = isCanvasEmpty
        self.update()

    def zoomChanged(self, zoomAmt):
        self.zoomButtons.setZoomAmt(zoomAmt)

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

    def resizeEvent(self, event) -> None:        
        if event.oldSize().height() != self.size().height():    # If Height changed
            self.zoomButtons.setPos(event.size().height())

        return super().resizeEvent(event)

class ZoomButtons(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        # References
        self.mainContent = parent

        # Set Attributes
        self.setAttribute(Qt.WA_StyledBackground, False) # Allow background color
        # self.setStyleSheet("background-color: red")
        self.setFixedHeight(35)
        self.setFixedWidth(120)

        font = QFont()
        font.setPointSize(10)

        self.prevText = ""

        # Buttons
        self.zoomOutButton = QPushButton(self)
        self.zoomOutButton.setFixedSize(27,26)
        self.zoomOutButton.setStyleSheet("background-color: #363636; border-radius: 5px; color: white")
        self.zoomOutButton.setText("-")
        self.zoomOutButton.setFont(font)
        self.zoomOutButton.setCursor(Qt.PointingHandCursor)

        self.zoomInButton = QPushButton(self)
        self.zoomInButton.setStyleSheet("background-color: #363636; border-radius: 5px; color: white")
        self.zoomInButton.setFixedSize(27,26)
        self.zoomInButton.setText("+")
        self.zoomInButton.setFont(font)
        self.zoomInButton.setCursor(Qt.PointingHandCursor)

        # Text
        self.zoomAMT = ClickableLineEdit(self)
        self.zoomAMT.setFixedSize(50,26)
        self.zoomAMT.setStyleSheet("background-color: #363636; border-radius: 5px; color: white; padding-left: 5px; padding-bottom: 2px")
        self.zoomAMT.setFont(font)
        self.zoomAMT.setAlignment(Qt.AlignVCenter)
        self.zoomAMT.setMaxLength(5)
               
        # Layout
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setSpacing(4)
        self.hLayout.setContentsMargins(7,0,0,7)
        self.hLayout.addWidget(self.zoomOutButton)
        self.hLayout.addWidget(self.zoomInButton)
        self.hLayout.addWidget(self.zoomAMT)


        # Init
        self.setZoomAmt(1)
        self.zoomOutButton.pressed.connect(self.zoomOut)
        self.zoomInButton.pressed.connect(self.zoomIn)
        self.zoomAMT.clicked.connect(self.textClicked)
        self.zoomAMT.editingFinished.connect(self.textChange)

    def zoomOut(self):
        self.mainContent.canvas.AddSubtractZoom(-.25)

    def zoomIn(self):
        self.mainContent.canvas.AddSubtractZoom(.25)

    def setZoomAmt(self, zoomAmt: int):
        formattedZoomAmt = str(round(zoomAmt * 100))
        self.prevText = formattedZoomAmt + "%"
        self.zoomAMT.setText(self.prevText)

    def textClicked(self):
        self.zoomAMT.setText("")

    def textChange(self):
        text = self.zoomAMT.text().removesuffix("%")
        if text.isdigit():
            text = int(text)/100

            if text > minMaxZoom[1]:
                text = minMaxZoom[1]
            elif text < minMaxZoom[0]:
                text = minMaxZoom[0]

            self.mainContent.canvas.SetZoomScale(text)
            self.setZoomAmt(text)
            
        else:
            self.zoomAMT.setText(self.prevText)

        self.zoomAMT.clearFocus()

    def setPos(self, yPos: int):
        """Sets the vertical position of the Zoom Buttons
        
        Args:
            yPos (int) : height of the window that will set the position of the Zoom Buttons
        """
        self.setGeometry(QRect(QPoint(self.pos().x(), yPos - self.height()), self.size()))


class ClickableLineEdit(QLineEdit):
    clicked = Signal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QLineEdit.mousePressEvent(self, event)

