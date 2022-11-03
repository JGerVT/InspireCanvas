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
        self.topBar = MainTopBar(self, tabsData = self.tabHashTable, projectName = GetProjectName(self.JSONData), selectedTab = GetSelectedTab(self.JSONData))  # Top Bar 
        self.canvas = MainCanvas(self, self.nodeHashTable, canvasSize= self.JSONData["canvasSize"])  # Main Canvas
        self.zoomButtons = ZoomButtons(self)

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
            print(event.size().height())
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

