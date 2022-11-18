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
from Utility.ManageJSON import *

def CanvasItemContextMenu(self, event):
    """ Context Menu when the canvas is right clicked
    Args: 
        event: MouseClick event
    
    """

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
    if self.copyCanvasItemData == None:
        pasteItem.setDisabled(True)

    contextMenu.addSeparator()                          # Insert Canvas Items
    insertMenu = contextMenu.addMenu("Insert")              # Insert Menu
    insertImage = insertMenu.addAction("Insert Image")      # Insert Image CanvasItem
    insertText = insertMenu.addAction("Insert Text")        # Insert Text CanvasItem
    insertFile = insertMenu.addAction("Insert File")        # Insert File CanvasItem
    contextMenu.addSeparator()                          # Project Management
    saveProject = contextMenu.addAction("Save Project As")     # Save Project
    loadProject = contextMenu.addAction("Load Project")     # Load Project
    newProject = contextMenu.addAction("New Project")       # New Project

    action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    if action == copyItem:
        self.CopySelection()

    elif action == pasteItem and self.copyCanvasItemData != None:
        self.PasteSelection(clickPos)

    elif action == deleteItem:
        for item in selected.childItems():
            self.RemoveCanvasItem(item)

    # ----- Insert Canvas Items -----
    elif action == insertImage:         # Insert Image CanvasItem
        imageFiles = QFileDialog.getOpenFileNames(self,"Select Images",".","Images (*.jpg *.png *.gif)")

        if imageFiles[0] != "":
            i = 0
            for filePath in imageFiles[0]:
                position = clickPos + QPointF(10*i, 10*i)
                self.NewImageCanvasItem(filePath, position)
                i += 1

    elif action == insertText:          # Insert Text CanvasItem
        self.NewTextCanvasItem("Text", clickPos, 1)


    elif action == saveProject:
        saveLocation = QFileDialog.getSaveFileName(self, "Save Location", ".", "JSON (*.json)")
        if(saveLocation[0] != ""):
            self.MainContent.SaveProject(saveLocation[0])

    elif action == loadProject:
        dataFile = QFileDialog.getOpenFileName(self, "Select JSON Project", ".", "JSON (*.json)")
        
        if dataFile[0] != "":
            if LoadJSON(dataFile[0], False) != None:   # This is used to validate if the data is valid
                self.MainContent.LoadProject(dataFile[0])
            else:
                print("ERROR")               

    elif action == newProject:
        newProjectLocation = QFileDialog.getSaveFileName(self, "Save Location", ".", "JSON (*.json)")
        
        if newProjectLocation[0] != "":
            self.MainContent.NewProject(newProjectLocation[0])


# ----- Tab Bar Context Menu -----
def TabBarContextMenu(self, event):
    """ Context Menu when the tab bar is right clicked

    Args: 
        event: MouseClick event
    """

    contextMenu = QMenu()
    contextMenu.setStyleSheet(qMenuStyle)

    copyItem = contextMenu.addAction("Copy Tab")            # Copy Tab 
    pasteItem = contextMenu.addAction("Paste Tab")          # Paste Tab
    closeItem = contextMenu.addAction("Delete Tab")         # Delete Tab
    duplicateItem = contextMenu.addAction("Duplicate Tab")  # Duplicate Tab
    contextMenu.addSeparator()
    renameTab = contextMenu.addAction("Rename Tab")         # Rename Tab 

    contextMenu.addSeparator()
    newTabItem = contextMenu.addAction("New Tab")           # Add New Tab
    contextMenu.addSeparator()
    saveProject = contextMenu.addAction("Save Project")     # Save Project
    loadProject = contextMenu.addAction("Load Project")     # Load Project
    newProject = contextMenu.addAction("New Project")       # New Project
    
    
    if type(self).__name__ != "Tab":
        copyItem.setDisabled(True)
        closeItem.setDisabled(True)
        duplicateItem.setDisabled(True)
    
    if self.GetCopy() == None:
        pasteItem.setDisabled(True)

    # Actions
    action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    if action == copyItem and type(self).__name__ == "Tab": # If copy tab, set self to copyTab
        self.SetCopy(self)
    elif action == pasteItem and self.GetCopy() != None:    # If paste item, duplicate copyTab
        if type(self).__name__ == "Tab":
            self.tabContainer.duplicateTab(self.GetCopy() ,self.getIndex())
        elif type(self).__name__ == "MainTopBar":
            self.TabContainer.duplicateTab(self.GetCopy())
    elif action == closeItem:                               # If closeItem, delete selected tab
        self.tabContainer.DeleteTab(self)
    elif action == duplicateItem:                           # If duplicate Tab, Duplicate Tab
        self.tabContainer.duplicateTab(self, self.getIndex())
    elif action == renameTab:                               # if renameTab, enable text selection on tab label, and select all. 
        self.label.setEnabled(True)
        self.label.setFocus()
        self.label.selectAll()
    elif action == newTabItem:                              # If newTabItem, insert a new tab after selected tab
        if type(self).__name__ == "Tab":
            self.tabContainer.createNewTab(self.getIndex())
        else:
            self.tabContainer.createNewTab()
    elif action == saveProject:     # Save Project
        saveLocation = QFileDialog.getSaveFileName(self, "Save Location", ".", "JSON (*.json)")
        if(saveLocation[0] != ""):
            self.MainContent.SaveProject(saveLocation[0])

    elif action == loadProject:     # Load Project
        dataFile = QFileDialog.getOpenFileName(self, "Select JSON Project", ".", "JSON (*.json)")
        
        if dataFile[0] != "":
            if LoadJSON(dataFile[0], False) != None:   # This is used to validate if the data is valid
                self.MainContent.LoadProject(dataFile[0])
            else:
                print("ERROR")

    elif action == newProject:      # New Project
        newProjectLocation = QFileDialog.getSaveFileName(self, "Save Location", ".", "JSON (*.json)")
        
        if newProjectLocation[0] != "":
            self.MainContent.NewProject(newProjectLocation[0])



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