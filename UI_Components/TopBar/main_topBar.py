"""
Description: This python file creates the TopBar of the software, which includes: Tabs and Window Buttons (i.e. Maximize, Minimize, and Close buttons)

Date Created: 9/27/22 
Date Updated: 9/28/22
"""

# --Imports--
import copy

#PySide
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from Utility.ManageJSON import CreateTabData

# Custom Imports
from Utility.UtilityFunctions import *
from Settings.settings import *
from UI_Components.ContextMenu.contextMenu import *

class MainTopBar(QWidget):
    def __init__(self, parent, projectName = "Project") -> None:
        """ 
        Top Bar of software. Contains Tabs and window buttons
        
        Args:
            selectedTab: index of current selected tab
            tabs: All tabs imported from JSON to be created on the top bar
        """
        super().__init__(parent)

        # Properties
        self.MainContent = parent
        self.selectedTab = 0
        self.projectName = projectName
        self.tabHashTable = None

        self.copyTab = None     # If a tab is being copied, it will be stored here.

        # Set Attributes
        self.setObjectName = "MainTopBar"
        self.setFixedHeight(topBarHeight)   # set in Settings/settings.py
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #0B0B0C; border-style: solid; border-bottom-color: rgb(41, 46, 55); border-bottom-width: 3px;")

        # Widgets in top bar
        self.hamburgerButton = HamburgerButton(self)
        self.tabScrollbar = TabScrollbar(self, self.MainContent)
        # self.TabContainer = TabContainer(self, MainContent = self.MainContent)
        # self.AddTabButton = AddTabButton(self)

        self.WindowOptions = WindowOptions(self)

        # Layouts
        hLayout = QHBoxLayout(self)
        hLayout.addWidget(self.hamburgerButton)
        hLayout.addWidget(self.tabScrollbar)
        # hLayout.addWidget(self.TabContainer)
        # hLayout.addSpacerItem(QSpacerItem(6,40,QSizePolicy.Minimum, QSizePolicy.Minimum))
        # hLayout.addWidget(self.AddTabButton)
        # hLayout.addSpacerItem(QSpacerItem(MaxSize,40,QSizePolicy.Maximum, QSizePolicy.Minimum))
        hLayout.addWidget(self.WindowOptions)
        LayoutRemoveSpacing(hLayout)

        # Init

    def SetTabs(self, tabHashTable, selectedTab):
        self.tabHashTable = tabHashTable
        self.tabScrollbar.TabContainer.SetTabs(selectedTab)

    def GetCopy(self):
        return self.copyTab

    def SetCopy(self, copy):
        self.copyTab = copy

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            TabBarContextMenu(self, event)
            return

        return super().mousePressEvent(event)

class HamburgerButton(QPushButton):
    def __init__(self, parent):
        """
        Left Hamburger button. (Not Implemented yet)
        """
        super().__init__(parent=parent)
        self.setCheckable(True)
        self.setFixedSize(QSize(50, topBarHeight))

        # self.setCursor(QCursor(Qt.PointingHandCursor))

        self.icon_  = QPixmap('Resources\svg\hamburger.svg')
        self.setIcon(self.icon_)

    def mousePressEvent(self, e) -> None:
        print("Hamburger press")
        return super().mousePressEvent(e)

class TabScrollbar(QScrollArea):
    def __init__(self, parent, MainContent) -> None:
        super().__init__(parent=parent)

        # References
        self.MainContent = MainContent
        self.MainTopBar = parent

        # Set Attributes
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.verticalScrollBar().setDisabled(True)

        self.centralWidget = QWidget(self)
        hBox = QHBoxLayout(self)
        LayoutRemoveSpacing(hBox)
        

        self.setWidget(self.centralWidget)
        self.centralWidget.setLayout(hBox)

        self.TabContainer = TabContainer(self, self.MainTopBar, MainContent = self.MainContent)
        self.AddTabButton = AddTabButton(self)

        # Add Widgets
        hBox.addWidget(self.TabContainer)
        hBox.addSpacerItem(QSpacerItem(6,40,QSizePolicy.Minimum, QSizePolicy.Minimum))
        hBox.addWidget(self.AddTabButton)
        hBox.addSpacerItem(QSpacerItem(10,40,QSizePolicy.Minimum, QSizePolicy.Minimum))
        hBox.addSpacerItem(QSpacerItem(MaxSize,40,QSizePolicy.Maximum, QSizePolicy.Minimum))

    def wheelEvent(self, event):
        QApplication.sendEvent(self.horizontalScrollBar(), event)



class TabContainer(QWidget):
    SelectTab = Signal(str) # When tab is selected, send signal to mainContent.py
    def __init__(self, parent, MainTopBar, MainContent) -> None:
        """Container of all tabs in project

        Args:
            selectedTab (int, optional): sets the selected tab. Defaults to 0.
            Tabs (_type_, optional): All tabs from Project JSON data. Defaults to None.
            MainContent (MainContent, optional): Top MainContent class. Used to connect signals Defaults to None.
        """
        super().__init__(parent)

        # References
        self.MainContent = MainContent

        # Set Attributes
        self.setObjectName("TabsContainer")

        # Properties and Data
        self.mainTopBar = MainTopBar
        self.selectedTabIndex = 0
        self.selectedTabWidget = None             

        #Layout
        self.hBoxLayout = QHBoxLayout(self)
        LayoutRemoveSpacing(self.hBoxLayout)

        # Events
        self.MainContent.FinishedInitializing.connect(self.FinishedInitializing)


    # Initialization
    def FinishedInitializing(self): 
        """When the main content is all initialized. This function emits a signal when a new tab is selected and calls self.SetSelected to update the canvas"""
        self.SelectTab.connect(self.MainContent.TabSelected)
        # self.SetSelectedWidget(self.GetTab(self.selectedTabIndex))  # Set selected tab on initialization

    # Add/Set/Removing Tabs
    def SetTabs(self, selectedTab):
        self.selectedTabIndex = selectedTab

        self.RemoveAllTabs()
        self.AddTabsFromData(self.mainTopBar.tabHashTable)

        self.SetSelectedWidget(self.GetTab(selectedTab))

    def RemoveAllTabs(self):
        for index in reversed(range(self.hBoxLayout.count())):
            widget = self.hBoxLayout.itemAt(index).widget()
            if widget.__class__.__name__ == "Tab":
                self.hBoxLayout.removeWidget(widget)
                widget.deleteLater()

    def AddTabsFromData(self, tabsData):
        for key in tabsData:
            self.AddTab(tabsData[key]["tabID"], tabsData[key]["tabName"], tabsData[key]["tabColor"], setSelected = False)

    def createNewTab(self, index = None):
        """Insert a new tab into the tab container

        Args:
            index (int): If the user wants a specific insert location, pass an index. Defaults to None.
        """
        newID = GenerateID()
        
        tabData = CreateTabData(tabName="Tab", tabID = newID, canvasItems=[]) 
        self.mainTopBar.tabHashTable[newID] = tabData
        newTab = self.AddTab(newID, tabData["tabName"], setSelected = False)

        if index != None:
            self.hBoxLayout.removeWidget(newTab)
            self.hBoxLayout.insertWidget(index + 1, newTab)

    def duplicateTab(self, tabWidget, index = None):
        newID = GenerateID()
        tabName = tabWidget.name
        tabColor = tabWidget.color
        canvasItems = copy.deepcopy(self.mainTopBar.tabHashTable[tabWidget.tabID]["canvasItems"])

        tabData = CreateTabData(tabName=tabName, tabColor=tabColor, tabID = newID, canvasItems=canvasItems) 
        self.mainTopBar.tabHashTable[newID] = tabData
        newTab = self.AddTab(newID, tabName, setSelected = False)

        if index != None:
            self.hBoxLayout.removeWidget(newTab)
            self.hBoxLayout.insertWidget(index + 1, newTab)

    def AddTab(self, tabID, name = "", color = "#23A0FF", setSelected = True):
        tab = Tab(self, tabID, name, color, mainContent=self.MainContent)
        self.hBoxLayout.addWidget(tab)
        if setSelected:
            self.SetSelectedWidget(tab)

        return tab

    def DeleteTab(self, tabWidget):
        """Delete a tab from the tab container
        
        Args: 
            tabWidget (QWidget): Tab widget to be deleted

        Returns:
            If deletion was successful, return True, else return False 
        """
        index = self.hBoxLayout.indexOf(tabWidget) 
        nextTab = None
        prevTab = None


        if self.GetNumberOfTabs() > 1:
            # Delete widget
            del self.mainTopBar.tabHashTable[tabWidget.tabID]
            tabWidget.deleteLater()

            if index < self.GetNumberOfTabs() - 1: # If tab is not last in tab container
                nextTab = self.GetTab(index + 1)
            if index - 1 >= 0:                  # If tab is not first in tab container
                prevTab = self.GetTab(index - 1)

            # Set Selection
            if self.selectedTabWidget == tabWidget:
                if nextTab != None:
                    self.SetSelectedWidget(nextTab)
                else:
                    self.SetSelectedWidget(prevTab)
            else:
                self.SetSelectedWidget(self.selectedTabWidget)
            
            return True
        else:
            return False

    def SetSelectedWidget(self, tabWidget):
        self.selectedTabWidget = tabWidget
        if tabWidget != None:
            self.SelectTab.emit(tabWidget.tabID)

        for index in range(self.hBoxLayout.count()):
            widget = self.hBoxLayout.itemAt(index).widget()
            if widget == tabWidget:
                widget.SetSelected(True)
            else:
                widget.SetSelected(False)

    def GetTab(self, tabID: str):
        """Retrieve a tab widget by it's index in the layout
           
        Args:
            tabID (str): get the tab widget with this tabID

        Return:
            If a tab with the desired tabID is found, return the Tab widget
        """

        for index in range(self.hBoxLayout.count()):        # Loop through all tabs in the tabContainer
            tab = self.hBoxLayout.itemAt(index).widget()  
            if tab.__class__.__name__ == "Tab":         
                if tab.tabID == tabID:                 # If a tab with the desired tabID is found, return the Tab widget
                    return tab
        
        return None # If tab was not found, return None.
        

    def GetSelectedIndex(self):
        return self.hBoxLayout.indexOf(self.selectedTabWidget)

    def getIndex(self, widget):
        return self.hBoxLayout.indexOf(widget)

    def GetNumberOfTabs(self):
        return self.hBoxLayout.count()

    def moveTab(self, tabWidget, eventPos):
        """Move tab when dragged to another index within the hboxlayout

        Args:
            tabWidget (Tab): Tab to be moved
            eventPos (QPoint): event position 
        """
        index = self.hBoxLayout.indexOf(tabWidget)
        numberOfTabs = self.GetNumberOfTabs()
        offset = 60 # Offset for how far into next or previous tab mouse needs to travel before it moves tab

        nextPos = self.mapTo(self, tabWidget.pos()).x() + tabWidget.width() + offset
        prevPos = self.mapTo(self, tabWidget.pos()).x() - offset

        if eventPos.x() > nextPos and index+1 < numberOfTabs:
            self.hBoxLayout.removeWidget(tabWidget)
            self.hBoxLayout.insertWidget(index + 1, tabWidget)

        elif eventPos.x() < prevPos and index > 0:
            self.hBoxLayout.removeWidget(tabWidget)
            self.hBoxLayout.insertWidget(index - 1, tabWidget)

    def GetCopy(self):
        return self.mainTopBar.GetCopy()

    def SetCopy(self, copy):
        self.mainTopBar.SetCopy(copy)


class Tab(QWidget):
    def __init__(self, parent, tabID, name = "Tab", color = "#23A0FF", mainContent = None)  -> None:
        """Clickable button that displays the current tab the user is on. Clicking the tab while switch to that tab, remove all nodes from the canvas and add all nodes from selected tab.

        Args:
            name (str, optional): Name of Tab. Defaults to "Tab".
            color (str, optional): Color of Tab. Defaults to "#23A0FF".
        """
        super().__init__(parent)

        # References
        self.tabContainer = parent
        self.MainContent = mainContent

        # Set Attributes
        self.setObjectName("Tab")
        self.installEventFilter(self)

        # Properties
        self.tabID = tabID
        self.name = name
        self.color = color
        self.selected = False

        # Set size of tab
        self.setFixedSize(QSize(tabWidth, tabHeight))
        # self.setMinimumSize(QSize(tabWidth, tabHeight))

        # Set tab color
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("Background-color: #292E37; margin-top: " + str(TitleBarTopSpacing) + "px; border-top-left-radius: 8px; border-top-right-radius: 8px;")

        # Set cursor to pointing hand on hover
        self.setCursor(QCursor(Qt.PointingHandCursor))

        # Font for label of tab
        font = QFont()
        font.setFamily(fontFamily)
        font.setPointSize(10)

        # Label of Tab
        self.label = TabText(name, self)
        self.label.setStyleSheet("color: white; border-color: transparent; background-color: transparent; margin-top: 0px;")
        self.label.setFont(font)

        # Delete Button
        self.deleteButton = QPushButton()
        self.deleteButton.setIcon(QPixmap("Resources\svg\Window Buttons\closeButton.svg"))
        self.deleteButton.setFixedSize(20,20)
        self.deleteButton.setStyleSheet("""
        QPushButton{
            margin-top: 0px; border-radius: 
            5px; border:none; 
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 35);;
        }
        """)
        self.deleteButton.setIconSize(QSize(8,8))
        self.deleteButton.hide()
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

        #Opacity
        self.op=QGraphicsOpacityEffect(self) # Opacity
        self.setGraphicsEffect(self.op)
        self.op.setOpacity(1)

        #Layout
        hBoxLayout = QHBoxLayout(self)
        LayoutRemoveSpacing(hBoxLayout) # Remove layout spacing
        hBoxLayout.setContentsMargins(30,4,5,0)
        hBoxLayout.addWidget(self.label)
        hBoxLayout.addWidget(self.deleteButton)

        # Initialization
        self.SetSelected(False)

    def GetCopy(self):
        return self.tabContainer.GetCopy()

    def SetCopy(self, copy):
        self.tabContainer.SetCopy(copy)

    def getIndex(self):
        return self.tabContainer.getIndex(self)

    def SetSelected(self, isSelected):
        """Set selected tab. If isSelected, this tab will be selected"""

        self.selected = isSelected
        self.SetStyleSheet()


    def SetStyleSheet(self):
        """Update the stylesheet, depending on if selected or not."""
        if self.selected:
            self.op.setOpacity(1)
        else:
            self.op.setOpacity(.7)


    # ----- Events -----
    def deleteButtonClicked(self):
        self.tabContainer.DeleteTab(self)
        pass

    # Click on tab to select tab
    def mousePressEvent(self, event):
        
        if event.button() == Qt.MouseButton.RightButton:
            TabBarContextMenu(self, event)
            return
        elif event.button() == Qt.MouseButton.LeftButton:
            self.parent().SetSelectedWidget(self)
            self.setFocus()
        return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:

        if event.button() == Qt.MouseButton.LeftButton:
            self.label.mouseDoubleClickEvent(event)
        # return super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.tabContainer.moveTab(self, self.mapToParent(event.pos()))
        return super().mouseMoveEvent(event)

    def eventFilter(self, watched, event) -> bool:
        if event.type() == QEvent.Enter: # Show/hide delete button when tab is hovered over
            self.deleteButton.show()
        elif event.type() == QEvent.Leave:
            self.deleteButton.hide()
        return super().eventFilter(watched, event)

    # Paint colored dot 
    def paintEvent(self, event) -> None:
        dotSize = 10
        
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor(self.color),  1, Qt.SolidLine))
        p.setBrush(QBrush(QColor(self.color), Qt.SolidPattern))
        p.drawEllipse(14, ((self.height() ) /2) - (dotSize/2) + 2, dotSize, dotSize)

        return super().paintEvent(event)

    def SaveTabText(self, text):
        self.tabContainer.mainTopBar.tabHashTable[self.tabID]["tabName"] = text
class TabText(QLineEdit):
    def __init__(self, text, parent)  -> None:
        super().__init__(text, parent)
        self.setEnabled(False)

        # References
        self.Tab = parent


        self.returnPressed.connect(self.StopEdit)

    def StopEdit(self):
        self.setEnabled(False)
        self.Tab.SaveTabText(self.text())


    def focusOutEvent(self, arg__1) -> None:
        self.StopEdit()
        return super().focusOutEvent(arg__1)

    def mouseDoubleClickEvent(self, event) -> None:
        if not self.isEnabled():
            self.setEnabled(True)
            self.setFocus()
            self.selectAll()
        # return super().mouseDoubleClickEvent(event)


class AddTabButton(QPushButton):
    def __init__(self, parent):
        """+ Button to add new tab
        """
        super().__init__(parent=parent)

        # Properties
        self.minOpacity = .3
        self.maxOpacity = 1

        # References
        self.parentTopBar = parent    
        self.tabContainer = parent.TabContainer    

        self.setStyleSheet("""
        QPushButton{
            background-color: transparent; 
            border-width: 0px;
            border-radius: 12px;
        }
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(25)
        self.setFixedWidth(25)
        self.setIconSize(QSize(13,13))

        self.setIcon(QPixmap("Resources\svg\AddTab.svg"))
        self.installEventFilter(self)

        #Opacity
        self.op=QGraphicsOpacityEffect(self) # Opacity
        self.setGraphicsEffect(self.op)
        self.op.setOpacity(self.minOpacity)

    def mousePressEvent(self, e) -> None:
        self.AddTab()
        return super().mousePressEvent(e)

    def AddTab(self):
        self.tabContainer.createNewTab()

    def eventFilter(self, object, event):
        if event.type() == QEvent.HoverEnter:
            self.op.setOpacity(self.maxOpacity)
            self.setStyleSheet("""
            QPushButton{
                background-color: transparent; 
                border-width: 0px;
                border-radius: 12px;
                background-color: rgba(41,46,55,200); 
            }
            """)
            return True
        if event.type() == QEvent.HoverLeave:
            self.op.setOpacity(self.minOpacity)
            self.setStyleSheet("""
            QPushButton{
                background-color: transparent; 
                border-width: 0px;
                border-radius: 12px;
                background-color: rgba(255,255,255,0); 
            }
            """)
            return True
        return False


class WindowOptions(QWidget):
    def __init__(self, parent):
        """Container of window navigation buttons. (i.e. minimize, maximize, close)"""
        super().__init__(parent=parent)
        self.setFixedHeight(parent.height())

        # Nav Buttons
        minimizeWindow = NavButtons(self, "minimizeWindow", "Resources\svg\Window Buttons\minimizeButton.svg")
        maximizeWindow = NavButtons(self, "maximizeWindow", "Resources\svg\Window Buttons\maximizeButton.svg")
        closeWindow = NavButtons(self, "closeWindow", "Resources\svg\Window Buttons\closeButton.svg")

        #Layout 
        hLayout = QHBoxLayout(self)
        LayoutRemoveSpacing(hLayout)
        hLayout.setSpacing(3)

        hLayout.addWidget(minimizeWindow)
        hLayout.addWidget(maximizeWindow)
        hLayout.addWidget(closeWindow)
        hLayout.addSpacerItem(QSpacerItem(0, MaxSize, QSizePolicy.Minimum, QSizePolicy.Maximum))


class NavButtons(QPushButton):
    def __init__(self, parent, name:str, imgLocation:str):
        """Nav buttons - i.e. close, maximize, minimize

        Args:
            name (str): name of button that is used to determine which button was clicked
            imgLocation (str): location of the image used for the NavButton
        """
        super().__init__(parent=parent)
        self.setObjectName("NavButton")

        self.name = name

        self.setFixedSize(NavButtonWidth,parent.height())
        self.setFixedWidth(NavButtonWidth)
        imageSize = QSize(11,11)

        self.setCursor(QCursor(Qt.PointingHandCursor))

        # Images
        self.pixmap = QPixmap(QIcon(imgLocation).pixmap(imageSize))
        self.pixmap.scaled(imageSize.width(), imageSize.height(), Qt.KeepAspectRatio)
        self.setIcon(self.pixmap)

    #Click mouse button
    def mousePressEvent(self, e) -> None:
        if self.name == "closeWindow":
            findMainWindow().close()
        elif self.name == "minimizeWindow":
            findMainWindow().showMinimized()

        elif self.name == "maximizeWindow": 
            if findMainWindow().isMaximized():
                findMainWindow().showNormal()
            else:
                findMainWindow().showMaximized()
        return super().mousePressEvent(e)