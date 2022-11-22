"""
Description:    This python file contains the QGraphicsView and QGraphicsScene that display the canvas items. 

Date Created: 9/27/22 
Date Updated: 10/15/22
"""

# --Imports--
import traceback

from Settings.settings import *

#Components Used:
from UI_Components.Canvas.CanvasItem.baseCanvasItem import *
from UI_Components.Canvas.CanvasItem.image_CanvasItem import *
from UI_Components.Canvas.CanvasItem.text_CanvasItem import TextCanvasItem
from UI_Components.Canvas.CanvasItem.file_CanvasItem import FileCanvasItem
from UI_Components.Canvas.CanvasUtility.SelectionHighlight import *
from UI_Components.Canvas.CanvasUtility.ItemGroup import *
from UI_Components.ContextMenu.contextMenu import *


class MainCanvas(QGraphicsView):
    IsCanvasEmpty = Signal(bool)
    def __init__(self, parent) -> None:
        """This class provides the (QGraphicsView) canvas where all CanvasItems will be placed.

        Args:

        Properties:
            self.CanvasItems (CanvasItem[]) : List of all CanvasItems in scene
            self.mainScene (MainScene) : Main scene in QGraphicsView
        """
        super().__init__(parent)

        # Set Attributes
        self.setObjectName("XYCanvas")
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: transparent; border: none;")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setCacheMode(QGraphicsView.CacheBackground)                    # Used to improve performance
        self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing, False)
        self.setFrameStyle(0)

        # _____ References _____
        self.MainContent = parent
        self.nodeHashTable = None
        self.tabData = None

        # _____ Properties _____
        self.canvasSize = None
        self.canvasItems = []
        self.canvasItemData = [] #Copy of canvas item data. Used for persistent data

        # Temporary Copy variable. When CanvasItems are copied, they are set here. 
        self.copyCanvasItemData = None

        # _____ Rubber Band Selection _____
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)

        # _____ Main Scene _____
        self.mainScene = None   # Main scene is set in SetCanvasData
        self.setScene(self.mainScene)

        # _____ Highlight Selection _____
        self.selectionHighlight = SelectionHighlight(self)

        # _____ Item Group For Selection _____
        self.selectedItemGroup = ItemGroup(mainView=self)
        self.selectedItemGroup.setZValue(9998)

        # _____ Signals _____
        self.IsCanvasEmpty.connect(self.MainContent.setCanvasEmpty)

    def SetCanvasData(self, nodeHashTable, canvasSize):
        self.canvasSize = canvasSize
        self.nodeHashTable = nodeHashTable
        self.mainScene = MainScene(0,0, canvasSize[0], canvasSize[1], self)   # Set main Scene
        self.setScene(self.mainScene)
        self.mainScene.addItem(self.selectionHighlight)
        self.mainScene.addItem(self.selectedItemGroup)


    def TabSelected(self, tabData):
        """Set canvas items on the canvas to a list of canvasItems.
        This removes all pre-existing canvas items on the canvas.
        This function is called when tabs are clicked.

        Args:
            canvasItems (obj[]): contains: nodeID, itemPos, and itemScale 
        """
        self.tabData = tabData

        self.SetZoomScale(tabData["viewportZoom"])

        self.horizontalScrollBar().setValue(tabData["viewportPos"][0])
        self.verticalScrollBar().setValue(tabData["viewportPos"][1])

        self.canvasItemData = tabData["canvasItems"]

        self.RemoveAllSelected()

        for item in self.mainScene.items(): # Only remove CanvasItems
            if issubclass(type(item), CanvasItem): 
                self.mainScene.removeItem(item)

        self.canvasItems.clear()    # Remove all items on canvas

        for canvasItemData in self.canvasItemData:          # Add all canvas items from canvasItems to the canvas. 
            self.InsertCanvasItem(canvasItemData)

        self.SetCanvasItemCount()   # This is needed if no CanvasItems are present, otherwise it will not show the message
        self.StoreZoomAmt()
        
    # ----- ADD, REMOVE, and Copy CanvasItems -----
    def InsertCanvasItem(self, canvasItemData):
        """ Add CanvasItem to the canvas. This will check which type of CanvasItem is passed and create the correct CanvasItem
            On Initialization, this is called from self.TabSelected

        Args:
            CanvasItemData (dict): Data for CanvasItem

        Returns:
            (ImageCanvasItem): returns created CanvasItem
        """
        try:    # IF item is found, get it's data, else raise error
            nodeData = self.nodeHashTable[canvasItemData["nodeID"]]
        except:
            ConsoleLog.error("Item [" + canvasItemData["nodeID"] +"] not found in database.")
            return None

        newCanvasItem = None
        if nodeData["nodeType"] == "Image_Node":
            newCanvasItem = ImageCanvasItem(self, canvasItemData)
        elif nodeData["nodeType"] == "Text_Node":
            newCanvasItem = TextCanvasItem(self, canvasItemData)
        elif nodeData["nodeType"] == "File_Node":
            newCanvasItem = FileCanvasItem(self, canvasItemData)        
        else:   # If type is not valid, do not add to database.
            ConsoleLog.error("Invalid Item Type", "[" + str(nodeData["nodeType"]) + "] is not a valid node type.")
            return None

        self.SetReference(canvasItemData["nodeID"], canvasItemData["canvasItemID"])  # Update Reference

        return self.AddCanvasItemToScene(newCanvasItem)

    def AddCanvasItemToScene(self, canvasItem):
        """This function adds the passed CanvasItem to the scene. 

        Args:
            canvasItem (CanvasItem): _description_

        Returns:
            _type_: _description_
        """

        self.mainScene.addItem(canvasItem)
        self.canvasItems.append(canvasItem)

        self.SetCanvasItemCount()
        self.SetZValues()

        return canvasItem
    
    def RemoveCanvasItem(self, canvasItem: CanvasItem, removeNodeData = True):
        """Remove CanvasItem from Canvas

        Args:
            canvasItem (CanvasItem): Item to be deleted/removed from the canvas
        """

        self.canvasItems.remove(canvasItem)
        self.RemoveSelected(canvasItem)

        self.tabData["canvasItems"].pop(self.tabData["canvasItems"].index(canvasItem.canvasItemData))   # Remove data from canvasItem Database

        if self.RemoveReference(canvasItem.canvasItemData["nodeID"], canvasItem.canvasItemData["canvasItemID"]) == 0:   # If there are no more references to the item in the database, delete from database
            del self.nodeHashTable[canvasItem.nodeID]

        canvasItem.deleteLater()
        self.SetCanvasItemCount()

    def DuplicateCanvasItem(self, nodeID:int, newPos:QPointF = None, scale:int = 1):
        """This function will duplicate a given CanvasItem data at the desired location. 

        Args:
            nodeID (int): _description_
            newPos (QPointF, optional): _description_. Defaults to None.
            scale (int, optional): New location of the canvas Item. Defaults to None.

        Returns:
            _type_: _description_
        """
        newData = CreateCIData(nodeID, newPos, scale)
        self.canvasItemData.append(newData)
        canvasItem = self.InsertCanvasItem(newData)
        
        return canvasItem

    # Insert New CanvasItem
    #   New Image CanvasItem
    def NewImageCanvasItem(self, imagePath: str, position: QPointF, scale = 1):
        """Create a new Image Canvas Item

        Args:
            imagePath (str): path to the image

        Returns:
            CanvasItem: Returns the new Canvas Item
        """
        imageNodeData = CreateImageData(imagePath)
        canvasItemData = CreateCIData(imageNodeData["nodeID"], position, scale)
        imageNodeData["canvasItemReferences"].append(canvasItemData["canvasItemID"])

        self.SetAllData(canvasItemData, imageNodeData)   # Set data to databases
        self.InsertCanvasItem(canvasItemData)   # Insert text node
    #   New Text CanvasItem
    def NewTextCanvasItem(self, text: str, position: QPointF, scale = 1, nodeName = "Text_Node"):
        """ Create a new Text Canvas Item

        Args:
            text (str): Text to be set to the Text CanvasItem
            position (QPointF): initial position of the CanvasItem
            scale (int, optional): scale of the TextCanvasItem. Defaults to 1.

        Returns:
            _type_: _description_
        """
        textNodeData = CreateTextData(text, nodeName)
        newID = textNodeData["nodeID"]
        canvasItemData = CreateCIData(newID, position, scale)

        self.SetAllData(canvasItemData, textNodeData)   # Set data to databases

        canvasItem = self.InsertCanvasItem(canvasItemData)   # Insert text node

        return canvasItem
    
    def NewFileCanvasItem(self, filePath: str, position: QPointF, scale = 1):
        """Create a new File Canvas Item

        Args:
            filePath (str): path to the file

        Returns:
            CanvasItem: Returns the new Canvas Item
        """
        fileNodeData = CreateFileData(filePath)
        canvasItemData = CreateCIData(fileNodeData["nodeID"], position, scale)
        fileNodeData["canvasItemReferences"].append(canvasItemData["canvasItemID"])

        self.SetAllData(canvasItemData, fileNodeData)   # Set data to databases
        self.InsertCanvasItem(canvasItemData)   # Insert text node

    # ________________________________________
    
    # ----- Copy and Paste -----
    def CopySelection(self):
        self.copyCanvasItemData = []
        for item in self.selectedItemGroup.childItems(): 
            offsetPos = item.scenePos() - self.selectedItemGroup.sceneBoundingRect().topLeft()

            nodeID = item.nodeID
            scale = item.GetScale()
            self.copyCanvasItemData.append({"offsetPos":offsetPos,
                                            "containerScenePos": self.selectedItemGroup.sceneBoundingRect().topLeft(),
                                            "nodeID": nodeID,
                                            "scale": scale})

    def PasteSelection(self, clickPos:QPointF):
        self.RemoveAllSelected()
        for item in self.copyCanvasItemData:
            newLocation = clickPos + item["offsetPos"]

            # If not text node, duplicate node, else create new node of type text. This needs to be done so editing text does not overwrite previous text.
            if self.nodeHashTable[item["nodeID"]]["nodeType"] != "Text_Node":   
                newNode =  self.DuplicateCanvasItem(item["nodeID"], newLocation, item["scale"])
                self.AddSelected(newNode)
            else:
                nodeName = self.nodeHashTable[item["nodeID"]]["nodeName"]
                nodeText = self.nodeHashTable[item["nodeID"]]["nodeText"]
                newNode = self.NewTextCanvasItem(nodeText, newLocation, item["scale"], nodeName = nodeName)   
                self.AddSelected(newNode)


    # ________________________________________

    # _______________ Utility _______________
    # ----- Set ------
    def SetAllData(self, canvasItemData, nodeData):
        """Sets data for both the canvasItem and nodeData

        Args:
            canvasItemData (_type_): canvasItemData
            nodeData (_type_): node Data
        """
        self.SetCanvasItemDatabase(canvasItemData)
        self.SetNodeDatabase(nodeData)

    def SetCanvasItemDatabase(self, canvasItemData):
        """ Add CanvasItem Data to database
            This will add the Image, Text, or File node data to the Node database.

        Args:
            nodeData (dict): data that will be added to database
        """
        self.canvasItemData.append(canvasItemData)

    def SetNodeDatabase(self, nodeData):
        """ Add Node Data to database
            This will add the Image, Text, or File node data to the Node database.

        Args:
            nodeData (dict): data that will be added to database
        """
        self.nodeHashTable[nodeData["nodeID"]] = nodeData

    def SetZValues(self):
        """Sets the z-index for every CanvasItem in the self.canvasItems list
        """
        for node in self.canvasItems:
            node.setZValue(self.canvasItems.index(node))
    
    # Manage Node References
    def SetReference(self, nodeID, canvasItemID):
        """Add CanvasItem reference to the node in the node database"""
        if canvasItemID not in self.nodeHashTable[nodeID]["canvasItemReferences"]:
            self.nodeHashTable[nodeID]["canvasItemReferences"].append(canvasItemID)


    def RemoveReference(self, nodeID, canvasItemID):    # Caused too many errors, so I am temporarily removing it.
        # del self.nodeHashTable[nodeID]["canvasItemReferences"][self.nodeHashTable[nodeID]["canvasItemReferences"].index(canvasItemID)]

        # if canvasItemID in self.nodeHashTable[nodeID]["canvasItemReferences"]:
        #     del self.nodeHashTable[nodeID]["canvasItemReferences"][self.nodeHashTable[nodeID]["canvasItemReferences"].index(canvasItemID)]

        return len(self.nodeHashTable[nodeID]["canvasItemReferences"])

    def SaveJSON(self, saveLocation = None):
        self.MainContent.UpdateJSONData()
        SaveJSON(self.MainContent.JSONData, saveLocation) 

    # ---------------

    # ----- Get -----
    def GetNodeData(self, nodeID:str):
        """Gets the data from the nodeHashTable (database of nodes)"""
        return self.nodeHashTable[nodeID]

    def GetCanvasItemsFromList(self, list):
        tempList = []
        for item in list:
            if issubclass(type(item), CanvasItem):
                tempList.append(item)
        return tempList

    def GetZoomScale(self):
        return self.transform().m11()
    # ---------------

    # ----- Other -----
    def SetCanvasItemCount(self):
        """Used to update if prompt to add CanvasItem appears or not in mainContent.py"""

        if len(self.canvasItems) == 0:
            self.IsCanvasEmpty.emit(True)
        else:
            self.IsCanvasEmpty.emit(False)    
   
    def CanvasItemToFront(self, canvasItem):
        """Brings the CanvasItem to the front of the canvas
        Called when CanvasItem is selected 

        Args:
            canvasItem (CanvasItem): The CanvasItem that will be moved to the front.
        """
        self.canvasItems.append(self.canvasItems.pop(self.canvasItems.index(canvasItem)))
        self.canvasItemData.append(self.canvasItemData.pop(self.canvasItemData.index(canvasItem.canvasItemData)))

        self.SetZValues()

    def isItemAtPos(self, pos:QPoint, checkSelectionHighlight = False):
        """Check if an item is under the mouse on the canvas.
        
        Arg:
            pos (QPoint) : check if item is at this position
            checkSelectionHighlight (bool) : If this is true, check if selection highlight is at pos as well.
        """
        itemAtPos = False
        for item in self.items(pos):
            if issubclass(type(item), CanvasItem):
                itemAtPos = True
            if checkSelectionHighlight and issubclass(type(item), SelectionHighlight):
                itemAtPos = True
        return itemAtPos

    def SetSelectionHighlightPos(self):
        self.selectionHighlight.SelectionChanged(self.selectedItemGroup.childItems())
    
    def GetVisibleScreenRect(self):
        """ Returns a QRectF of the visible area in the scene
            From: https://stackoverflow.com/a/17924010
        """
        viewport_rect = QRect(0, 0, self.viewport().width(), self.viewport().height())
        visible_scene_rect = QRectF(self.mapToScene(viewport_rect).boundingRect())

        return visible_scene_rect
    # ---------------

    # ----- Zoom -----
    def StoreZoomAmt(self):
        zoomAmt = self.GetZoomScale()
        self.tabData["viewportZoom"] = zoomAmt
        self.MainContent.zoomChanged(zoomAmt)

    def SetZoomScale(self, m11ZoomScale):
        if m11ZoomScale > minMaxZoom[1]:    # Limit zoom scaling to minMaxZoom
            m11ZoomScale = minMaxZoom[1]
        elif m11ZoomScale < minMaxZoom[0]:
            m11ZoomScale = minMaxZoom[0]

        originalTransform = self.transform()
        transform = QTransform(m11ZoomScale, originalTransform.m12(),originalTransform.m13(),originalTransform.m21(),m11ZoomScale,originalTransform.m23(),originalTransform.m31(),originalTransform.m32(),originalTransform.m33())
        QTransform()
        self.setTransform(transform)
        self.StoreZoomAmt()

    def AddSubtractZoom(self, zoom: float):
        """Add/Subtract from zoom in scene."""
        
        anchor = self.transformationAnchor()    # anchor allows for zoom in on mouse scene position
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        prevTransform = self.transform()
        prevPos = QPoint(self.horizontalScrollBar().value(), self.verticalScrollBar().value())

        self.scale(1+zoom, 1+zoom)
        self.setTransformationAnchor(anchor)

        if self.GetZoomScale() > minMaxZoom[1]:
            self.setTransform(prevTransform)
            self.horizontalScrollBar().setValue(prevPos.x())
            self.verticalScrollBar().setValue(prevPos.y())
        elif self.GetZoomScale() < minMaxZoom[0]:
            self.setTransform(prevTransform)
            self.horizontalScrollBar().setValue(prevPos.x())
            self.verticalScrollBar().setValue(prevPos.y())

        self.SetSelectionHighlightPos()

        # Save changes        
        self.StoreZoomAmt()
        self.tabData["viewportPos"] = [self.horizontalScrollBar().value(), self.verticalScrollBar().value()]


    # _______________ Manage Selected Canvas Nodes _______________
    def SetSelected(self, canvasItem):
        """Set the single canvasItem passed as selected. Removes previous selection
        
        Arg:
            canvasItem: Item to be set as selected
        """
        self.RemoveAllSelected()
        self.AddSelected(canvasItem)

    def SetSelectedItems(self, canvasItems):
        """Set multiple canvasItems passed as selected. Removes previous selection
        
        Arg:
            canvasItems: Items to be set as selected
        """
        self.RemoveAllSelected()
        for item in canvasItems:
            self.AddSelected(item)

    def AddSelected(self, canvasItem):
        """Add node to selection. Does not remove previous selection
        
        Arg:
            canvasItem: Item to be removed from the selection item group
        """
        if self.selectedItemGroup.childItems() == []:  # If it is the only selected item, bring to front.
            self.CanvasItemToFront(canvasItem)

        if canvasItem not in self.selectedItemGroup.childItems():  # Make sure item not already selected
            self.selectedItemGroup.addToGroup(canvasItem)

        canvasItem.SetSelected(True)
        self.SetSelectionHighlightPos()

    def RemoveSelected(self, canvasItem):
        """Removes the selected canvasItem passed
        
        Arg:
            canvasItem: Item to be removed from the selection item group
        """
        if canvasItem in self.selectedItemGroup.childItems():  
            self.selectedItemGroup.removeFromGroup(canvasItem)      

        canvasItem.SetSelected(False)
        self.SetSelectionHighlightPos()
        
    def RemoveAllSelected(self):
        """Removes all selected canvasItems from selectedItemGroup"""
        for item in self.selectedItemGroup.childItems():
            self.RemoveSelected(item)
            # item.SetSelected(False)

        self.selectedItemGroup.resetTransform()

    def GetSelected(self):
        """Get all selected nodes"""
        return self.selectedItemGroup.childItems()


    #_________ Events _________
    def mousePressEvent(self, event):   
        if event.button() == Qt.MouseButton.MiddleButton:
            self.prevMousePos = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            return
        elif event.button() == Qt.MouseButton.RightButton:
            CanvasItemContextMenu(self, event)
            return

        elif event.button() == Qt.MouseButton.LeftButton:
            self.prevMousePos = event.pos()
            self.prevSelectedItems = []
            if not self.isItemAtPos(event.pos(), True):   # If item is at position, show rubber band
                self.rubberBand.setGeometry(QRect(event.pos(), QSize()))
                self.rubberBand.show()

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        #Pan Scene
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.rubberBand.isVisible(): # Rubber Band Selector: If no item was clicked and rubber band is visible.
                rubberBandRect = QRect(self.prevMousePos, event.pos()).normalized()
                self.rubberBand.setGeometry(rubberBandRect)
                selectedItems = self.items(rubberBandRect)
                selectedItems = self.GetCanvasItemsFromList(selectedItems)

                if self.prevSelectedItems != selectedItems:
                    self.prevSelectedItems = selectedItems
                    self.SetSelectedItems(selectedItems)
                # pass
                return
            else:
                return super().mouseMoveEvent(event)
        elif event.buttons() == Qt.MiddleButton:
            offset = self.prevMousePos - event.pos()
            self.prevMousePos = event.pos()

            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
            event.accept()
            return
        else:
            return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.unsetCursor()
        self.tabData["viewportPos"] = [self.horizontalScrollBar().value(), self.verticalScrollBar().value()]
        self.rubberBand.hide()

        return super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        """CTRL + Mousewheel: Zoom in and out, limited by settings.py ( minMaxZoom[] ) 
        
        Zooms in on mouse position on canvas. Code from: https://stackoverflow.com/a/41688654
        """
        if event.angleDelta().y() < 0:
            self.AddSubtractZoom(-.1)
        else:
            self.AddSubtractZoom(.1)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_Left or event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down: # If arrow keys are pressed, disable default functionality and pass event directly to the scene
            self.mainScene.keyPressEvent(event)
            return True        

        if event.matches(QKeySequence.Copy):                                            # Copy selected CanvasItems
            self.CopySelection()       
        elif event.matches(QKeySequence.Paste) and self.copyCanvasItemData != None:     # Paste selected CanvasItems
            cursorScenePos = self.mapToScene(self.mapFromGlobal(QCursor().pos()))
            if self.GetVisibleScreenRect().contains(cursorScenePos):
                self.PasteSelection(cursorScenePos)
            else:
                self.PasteSelection(self.copyCanvasItemData[0]["containerScenePos"])
        elif event.matches(QKeySequence.Cut):                                           # Cut selected CanvasItems
            self.CopySelection()
            for item in self.GetSelected():
                self.RemoveCanvasItem(item, False)

        return super().keyPressEvent(event)
    # ________________________________________


# Main Scene in View
class MainScene (QGraphicsScene):
    def __init__(self, x: float, y: float, width: float, height: float, parent = None):
        """Provides the scene where CanvasItems will be placed, as well as the CanvasItem interactions and functionality.

        Args:
            x (float): sets the x coord of the scene
            y (float): sets the y coord of the scene
            width (float): Sets the width of the scene
            height (float): Sets the height of the scene
            parent (_type_, optional): parent of the scene. Defaults to None.
        """
        super().__init__(x, y, width, height, parent=parent)

        # Set Attributes
        self.setItemIndexMethod(self.ItemIndexMethod.NoIndex)   # Improves the performance somewhat https://doc.qt.io/qt-6/qgraphicsscene.html

        # Properties
        self.mainView:QGraphicsView = parent
        self.draggingItem = False
        

    # ------ Utility ------  
    def onlyOneCanvasItemSelected(self):
        """Checks to see if only a textbox is selected
        
        Returns:
            Returns the only selected TextCanvasItem
        """
        topWidget = self.mainView.selectedItemGroup.childItems()[0]
        if len(self.mainView.selectedItemGroup.childItems()) == 1:
            return topWidget
        return None

    def GetTopWidgetAtPos(self, scenePos:QPointF):
        """Get the top widget at the passed scenePos

        Args:
            scenePos (QPointF): position to check for widgets

        Returns:
            CanvasItem: Top widget under mouse 
        """
        itemsUnderMouse = self.items(scenePos)
        for item in itemsUnderMouse:
            if issubclass(type(item), CanvasItem):  # Check if item is subclassed from CanvasItem.
                return item
        return None

    # ------ EVENTS ------
    def mousePressEvent(self, event) -> None:   # https://stackoverflow.com/a/3839127
        """Mouse clicked on scene"""

        self.prevPos = event.scenePos()
        self.canDrag = True 

        # Get top widget
        self.topWidgetUnderMouse = self.GetTopWidgetAtPos(event.scenePos()) 

        # Set initial data for checking delta changes
        self.mainView.selectedItemGroup.SetInitialPos()
        self.mainView.selectedItemGroup.SetInitialSceneBoundingRect()
        self.mainView.selectedItemGroup.SetInitialSceneRectALL()

        #* No Item under mouse, but SelectionHighlight corner IS under mouse
        if self.mainView.selectionHighlight.isHandleUnderMouse(event.scenePos()):
            self.canDrag = False
            self.mainView.selectionHighlight.SetCanDrag(True)
            return super().mousePressEvent(event)   

        #* No Item or SelectionHighlight under mouse on click (i.e. when the user clicks on the canvas) Unselect all items
        elif self.topWidgetUnderMouse == None:
            self.mainView.RemoveAllSelected()
            self.canDrag = False
            return 

        #* Item under mouse on click
        if (self.topWidgetUnderMouse != None and self.topWidgetUnderMouse.isEnabled() and not self.topWidgetUnderMouse.GetIsSelected()):
            if event.modifiers() and Qt.Modifier.SHIFT: # If Shift held, add item to selection
                self.mainView.AddSelected(self.topWidgetUnderMouse)
                self.canDrag = False
            else:                                       # If Shift is not held, set as only selection.
                self.mainView.SetSelected(self.topWidgetUnderMouse)

        # If any items are not set to canDrag, don't allow the user to drag the items
        for item in self.mainView.selectedItemGroup.childItems():
            if not item.canDrag:
                self.canDrag = False

        self.prevTextItem = self.onlyOneCanvasItemSelected()  # This checks if only a textBox is selected

        return super().mousePressEvent(event)   

    def mouseMoveEvent(self, event) -> None:
        """When the mouse moves, if item under mouse and is selected, drag item"""
        if event.buttons() == Qt.MouseButton.LeftButton and len(self.mainView.selectedItemGroup.childItems()) > 0 and self.topWidgetUnderMouse != None and self.canDrag:
            if type(self.prevTextItem) != TextCanvasItem or type(self.prevTextItem) == TextCanvasItem and not self.prevTextItem.isEditable():
                delta = event.scenePos() - self.prevPos
                self.mainView.selectedItemGroup.MoveGroup(delta)
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mainView.selectedItemGroup.SetItemData()
        self.mainView.selectionHighlight.SetCanDrag(False)
        return super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        """Used to open file when it is double clicked"""
        if type(self.topWidgetUnderMouse) == TextCanvasItem:
            self.topWidgetUnderMouse.setIsEditable(True)

        elif type(self.topWidgetUnderMouse) == ImageCanvasItem and self.onlyOneCanvasItemSelected() != None:
            try:
                # print(self.topWidgetUnderMouse.imagePath)
                openFile(self.topWidgetUnderMouse.imagePath)
                # Open File
                pass
            except:
                pass
            return

        elif type(self.topWidgetUnderMouse) == FileCanvasItem and self.onlyOneCanvasItemSelected() != None:
            try:
                openFile(self.topWidgetUnderMouse.filePath)
            except:
                pass
            return
        # return super().mouseReleaseEvent(event)
    
    def keyPressEvent(self, event) -> None:
        try:
            textItem = self.onlyOneCanvasItemSelected()
        except:
            pass

        if event.key() == Qt.Key.Key_Delete:                    # If Delete key is pressed, delete selected items
            if type(textItem) != TextCanvasItem or type(textItem) == TextCanvasItem and not textItem.isEditable():# If there is no text item or the text item is not editable, delete. 
                for item in self.mainView.selectedItemGroup.childItems():
                    self.mainView.RemoveCanvasItem(item)
        return super().keyPressEvent(event)

    # Drag item over scene
    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls() or event.mimeData().hasText(): # Only allow file drags or text drags.
            event.acceptProposedAction()
        else:
            return
        return super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event) -> None:
        """When the user drops a file on the canvas"""
        urlTemp = ""
        try:    
            if event.mimeData().hasUrls():
                event.accept()
                urls = event.mimeData().urls()

                initPosition = event.scenePos()
                for url in urls:
                    # Get File extension to know which type of file was dropped.
                    urlType = GetFileType(url.fileName()).lower()   
                    urlTemp = url.toLocalFile()
                    
                    if urlType in imageFileTypes: # Is an image file type.
                        self.mainView.NewImageCanvasItem(url.toLocalFile(), initPosition)
                        initPosition += QPointF(10,10) # This offsets the dropped images by 10px x and y for each image dropped

                    else: # Is a file type
                        self.mainView.NewFileCanvasItem(url.toLocalFile(), initPosition)
                        initPosition += QPointF(10,10) # This offsets the dropped images by 10px x and y for each image dropped
                        print("Dropped File")

            elif event.mimeData().hasImage():
                print("HAS IMAGE")
                pass

            elif event.mimeData().hasText(): # If text is dragged and dropped on the canvas
                print("Text Dropped: \"" + event.mimeData().text() + "\"")

            else: # Invalid item dropped on canvas.
                event.ignore()

            pass
        except Exception:
            traceback.print_exc()
            print("ERROR")
            ConsoleLog.error("Drop Error", "Could not add Canvas Item: '" + urlTemp + "'")

        return super().dropEvent(event)

