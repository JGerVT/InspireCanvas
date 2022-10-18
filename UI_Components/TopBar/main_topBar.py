"""
Description: This python file creates the TopBar of the software, which includes: Tabs and Window Buttons (i.e. Maximize, Minimize, and Close buttons)

Date Created: 9/27/22 
Date Updated: 9/28/22
"""

# --Imports--
#PySide
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

# Custom Imports
from Utility.UtilityFunctions import *
from Settings.settings import *


class MainTopBar(QWidget):
    def __init__(self, parent, selectedTab : int, tabsData, projectName = "Project") -> None:
        """ 
        Top Bar of software. Contains Tabs and window buttons
        
        Args:
            selectedTab: index of current selected tab
            tabs: All tabs imported from JSON to be created on the top bar
        """
        super().__init__(parent)

        # Properties
        self.MainContent = parent
        self.selectedTab = selectedTab
        self.tabsData = tabsData
        self.projectName = projectName

        # Set Attributes
        self.setObjectName = "MainTopBar"
        self.setFixedHeight(topBarHeight)   # set in Settings/settings.py
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: #0B0B0C; border-style: solid; border-bottom-color: rgb(41, 46, 55); border-bottom-width: 3px;")

        # Widgets in top bar
        self.hamburgerButton = HamburgerButton(self)
        self.TabContainer = TabContainer(self, selectedTab = self.selectedTab, tabsData = self.tabsData, MainContent = self.MainContent)
        self.AddTabButton = AddTabButton(self)
        self.WindowOptions = WindowOptions(self)


        # Layouts
        hLayout = QHBoxLayout(self)
        hLayout.addWidget(self.hamburgerButton)
        hLayout.addWidget(self.TabContainer)
        hLayout.addWidget(self.AddTabButton)
        hLayout.addSpacerItem(QSpacerItem(MaxSize,40,QSizePolicy.Maximum, QSizePolicy.Minimum))
        hLayout.addWidget(self.WindowOptions)
        LayoutRemoveSpacing(hLayout)

        # Init


class HamburgerButton(QPushButton):
    def __init__(self, parent):
        """
        Left Hamburger button. (Not Implemented yet)
        """
        super().__init__(parent=parent)
        self.setCheckable(True)
        self.setFixedSize(QSize(50, topBarHeight))

        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.icon_  = QPixmap('Resources\svg\hamburger.svg')
        self.setIcon(self.icon_)

    def mousePressEvent(self, e) -> None:
        print("Hamburger press")
        return super().mousePressEvent(e)


class TabContainer(QWidget):
    SelectTab = Signal(str) # When tab is selected, send signal to mainContent.py
    def __init__(self, parent, tabsData, MainContent, selectedTab = 0) -> None:
        """Container of all tabs in project

        Args:
            selectedTab (int, optional): sets the selected tab. Defaults to 0.
            Tabs (_type_, optional): All tabs from Project JSON data. Defaults to None.
            MainContent (MainContent, optional): Top MainContent class. Used to connect signals Defaults to None.
        """
        super().__init__(parent)

        # Properties
        self.MainContent = MainContent
        self.selectedTab = selectedTab
        self.tabsData = tabsData

        # Set Attributes
        self.setObjectName("TabsContainer")

        #Layout
        self.hBoxLayout = QHBoxLayout(self)
        LayoutRemoveSpacing(self.hBoxLayout)
        # self.hBoxLayout.setSpacing(2)

        # Events
        self.MainContent.FinishedInitializing.connect(self.FinishedInitializing)


        # Add Tabs
        self.AddTabsData(self.tabsData)

    def FinishedInitializing(self): 
        """When the main content is all initialized. This function emits a signal when a new tab is selected and calls self.SetSelected to update the canvas"""
        self.SelectTab.connect(self.MainContent.TabSelected)
        self.SetSelected(self.selectedTab, self.GetTab(self.selectedTab).tabID)

    def AddTabsData(self, tabsData):
        for tab in tabsData:
            self.AddTab(tab["tabID"], tab["tabName"], tab["tabColor"])

    def AddTab(self, tabID, name = "", color = "#23A0FF"):
        tab = Tab(self, tabID, name, color)
        self.hBoxLayout.addWidget(tab)
        self.SetSelected(self.selectedTab, tabID)

    def GetTab(self, index):
        for ind in range(self.hBoxLayout.count()):
            if self.hBoxLayout.itemAt(index).widget().__class__.__name__ == "Tab":
                if ind == index:
                    return self.hBoxLayout.itemAt(index).widget()

    def SetSelected(self, selectedIndex, tabID):
        self.selectedTab = selectedIndex

        for index in range(self.hBoxLayout.count()):
            if self.hBoxLayout.itemAt(index).widget().__class__.__name__ == "Tab":
                if index == selectedIndex:
                    self.hBoxLayout.itemAt(index).widget().SetSelected(True)
                else:
                    self.hBoxLayout.itemAt(index).widget().SetSelected(False)

        self.SelectTab.emit(tabID)

class Tab(QWidget):
    def __init__(self, parent, tabID, name = "Tab", color = "#23A0FF")  -> None:
        """Clickable button that displays the current tab the user is on. Clicking the tab while switch to that tab, remove all nodes from the canvas and add all nodes from selected tab.

        Args:
            name (str, optional): Name of Tab. Defaults to "Tab".
            color (str, optional): Color of Tab. Defaults to "#23A0FF".
        """
        super().__init__(parent)

        # Set Attributes
        self.setObjectName("Tab")

        # Properties
        self.tabID = tabID
        self.name = name
        self.color = color
        self.selected = False

        # Set size of tab
        self.setFixedSize(QSize(tabWidth, tabHeight))

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
        self.label = QLabel(name, self)
        self.label.setStyleSheet("color: white; padding-left: 30px; border-color: transparent; background-color: transparent; margin-top: 6px;")
        self.label.setFont(font)

        #Opacity
        self.op=QGraphicsOpacityEffect(self) # Opacity
        self.setGraphicsEffect(self.op)
        self.op.setOpacity(1)

        #Layout
        hBoxLayout = QHBoxLayout(self)
        LayoutRemoveSpacing(hBoxLayout) # Remove layout spacing
        hBoxLayout.addWidget(self.label)

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

    # Click on tab to select tab
    def mousePressEvent(self, event):
        self.parent().SetSelected(self.parent().hBoxLayout.indexOf(self), self.tabID)
        return super().mousePressEvent(event)

    # Paint colored dot 
    def paintEvent(self, event) -> None:
        dotSize = 10
        
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(QPen(QColor(self.color),  1, Qt.SolidLine))
        p.setBrush(QBrush(QColor(self.color), Qt.SolidPattern))
        p.drawEllipse(14, ((self.height() ) /2) - (dotSize/2) + 3, dotSize, dotSize)

        return super().paintEvent(event)

class AddTabButton(QPushButton):
    def __init__(self, parent):
        """+ Button to add new tab
        """
        super().__init__(parent=parent)
        self.setStyleSheet("background-color: transparent; border-width: 0px;")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(topBarHeight)
        self.setFixedWidth(topBarHeight)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border-width: 0px;")
        self.label.setPixmap(QPixmap("Resources\svg\AddTab.svg"))

        self.installEventFilter(self)

        #Opacity
        self.op=QGraphicsOpacityEffect(self) # Opacity
        self.setGraphicsEffect(self.op)
        self.op.setOpacity(.2)

        #Layout 
        self.hBoxLayout = QHBoxLayout(self)
        LayoutRemoveSpacing(self.hBoxLayout)
        self.hBoxLayout.addWidget(self.label)

    def eventFilter(self, object, event):
        if event.type() == QEvent.HoverEnter:
            self.op.setOpacity(.5)
            return True
        if event.type() == QEvent.HoverLeave:
            self.op.setOpacity(.2)
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