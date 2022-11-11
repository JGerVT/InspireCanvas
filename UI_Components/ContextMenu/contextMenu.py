"""
Description:  This file provides code for context menus when the tab bar or canvas are right clicked. 

Date Created: 11/6/22 
Date Updated: 11/10/22
"""

#PySide
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from Utility.UtilityFunctions import *
import copy

# Temporary Copy variables. When Tabs or CanvasItems are copied, they are set here. 
copyTab = None
copyCanvasItemData = None

def CanvasItemContextMenu(self, event):
    """ Context Menu when the canvas is right clicked
    Args: 
        event: MouseClick event
    
    """
    global copyTab, copyCanvasItemData # Needed to avoid "UnboundLocalError: local variable referenced before assignment" error

    selected = self.selectedItemGroup
    clickPos = self.mapToScene(event.pos())

    contextMenu = QMenu()
    contextMenu.setStyleSheet(qMenuStyle)

    copyItem = contextMenu.addAction("Copy")            # Copy
    pasteItem = contextMenu.addAction("Paste")          # Paste
    deleteItem = contextMenu.addAction("Delete")        # Delete

    if len(selected.childItems()) == 0:
        copyItem.setDisabled(True)
        deleteItem.setDisabled(True)
    if copyCanvasItemData == None:
        pasteItem.setDisabled(True)

    contextMenu.addSeparator()
    insertMenu = contextMenu.addMenu("Insert")          # Insert Menu
    insertImage = insertMenu.addAction("Insert Image")  # Insert Image CanvasItem
    insertFile = insertMenu.addAction("Insert File")    # Insert File CanvasItem
    insertText = insertMenu.addAction("Insert Text")    # Insert Text CanvasItem
    contextMenu.addSeparator()
    saveProject = contextMenu.addAction("Save Project") # Save Project
    loadProject = contextMenu.addAction("Load Project") # Load Project
    newProject = contextMenu.addAction("New Project")   # New Project

    action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    if action == copyItem:
        copyCanvasItemData = []
        for item in selected.childItems(): 
            offsetPos = item.pos() - selected.boundingRect().topLeft()

            nodeID = item.nodeID
            scale = item.GetScale()
            copyCanvasItemData.append({ "offsetPos":offsetPos,
                                        "nodeID": nodeID,
                                        "scale": scale})
        
    elif action == pasteItem and copyCanvasItemData != None:
        self.RemoveAllSelected()
        for item in copyCanvasItemData:
            newLocation = clickPos + item["offsetPos"]

            item = self.DuplicateCanvasItem(item["nodeID"], newLocation, item["scale"])
            item.AddSelected(True)

    elif action == deleteItem:
        for item in selected.childItems():
            self.RemoveCanvasItem(item)

    elif action == insertText:
        self.InsertTextNode("Text", clickPos, 1)
        print("Insert Text")

    elif action == saveProject:
        print("SAVE")

def TabBarContextMenu(self, event):
    """ Context Menu when the tab bar is right clicked

    Args: 
        event: MouseClick event
    """
    global copyTab, copyNodes # Needed to avoid "UnboundLocalError: local variable referenced before assignment" error

    contextMenu = QMenu()
    contextMenu.setStyleSheet(qMenuStyle)

    copyItem = contextMenu.addAction("Copy Tab")            # Copy Tab 
    pasteItem = contextMenu.addAction("Paste Tab")          # Paste Tab
    closeItem = contextMenu.addAction("Delete Tab")         # Delete Tab
    duplicateItem = contextMenu.addAction("Duplicate Tab")  # Duplicate Tab

    if type(self).__name__ != "Tab":
        print("TRUE")
        copyItem.setDisabled(True)
        closeItem.setDisabled(True)
        duplicateItem.setDisabled(True)
    
    if copyTab == None:
        pasteItem.setDisabled(True)

    contextMenu.addSeparator()
    newTabItem = contextMenu.addAction("New Tab")           # Add New Tab
    contextMenu.addSeparator()
    saveProject = contextMenu.addAction("Save Project")     # Save Project
    loadProject = contextMenu.addAction("Load Project")     # Load Project
    newProject = contextMenu.addAction("New Project")       # New Project


    # Actions
    action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    if action == copyItem and type(self).__name__ == "Tab": # If copy tab, set self to copyTab
        copyTab = self
    elif action == pasteItem and copyTab != None:           # If paste item, duplicate copyTab
        if type(self).__name__ == "Tab":
            self.tabContainer.duplicateTab(copyTab ,self.getIndex())
        elif type(self).__name__ == "MainTopBar":
            self.TabContainer.duplicateTab(copyTab)
    elif action == closeItem:                               # If closeItem, delete selected tab
        self.tabContainer.DeleteTab(self)
    elif action == duplicateItem:                           # If duplicate Tab, Duplicate Tab
        self.tabContainer.duplicateTab(self, self.getIndex())
    elif action == newTabItem:                              # If newTabItem, insert a new tab after selected tab
        if type(self).__name__ == "Tab":
            self.tabContainer.createNewTab(self.getIndex())
        else:
            self.tabContainer.createNewTab()
    elif action == saveProject:     # Save Project
        print("SAVE")
    elif action == loadProject:     # Load Project
        print("load")
    elif action == newProject:      # New Project
        print("new")



# Styling for QMenu()
qMenuStyle = """
QMenu{
    color: white;
    margin: 5px;
    border-radius: 10px;
    background: black;
}

QMenu::separator {
    height: 1px;
    background: white;
    margin-left: 5px;
    margin-right: 5px;
}

QMenu::item {
    padding: 4px 6px 4px 6px;
    margin-top: 1px;
    margin-bottom: 2px;
    min-width: 140px;
}

QMenu::item:selected {
    background: rgba(255, 255, 255, 56);
    border-radius: 5px;
}

QMenu::item:disabled {
    color: gray;
}
"""