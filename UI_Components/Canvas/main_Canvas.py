"""
Description: This python file contains the QGraphicsView and QGraphicsScene that display the canvas items. 

Date Created: 9/27/22 
Date Updated: 10/15/22
"""

# --Imports--
import traceback

from sympy import false

from Settings.settings import *

#Components Used:
from UI_Components.Canvas.CanvasItem.baseCanvasItem import *
from UI_Components.Canvas.CanvasItem.image_CanvasItem import *
from UI_Components.Canvas.CanvasUtility.SelectionHighlight import *
from UI_Components.Canvas.CanvasUtility.ItemGroup import *


class MainCanvas(QGraphicsView):
    IsCanvasEmpty = Signal(bool)
    def __init__(self, parent, nodeHashTable, canvasSize = [5000, 5000]) -> None:
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

        self.setCacheMode(QGraphicsView.CacheBackground)        
        self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing, False)
        self.setFrameStyle(0)

        # _____ References _____
        self.MainContent = parent
        self.nodeHashTable = nodeHashTable
        self.tabData = None

        # _____ Properties _____
        self.canvasSize = canvasSize
        self.canvasItems = []
        self.canvasItemData = [] #Copy of canvas item data. Used for persistent data

        # _____ Rubber Band Selection _____
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)

        # _____ Main Scene _____
        self.mainScene = MainScene(0,0, self.canvasSize[0], self.canvasSize[1], self)   # Set main Scene
        self.setScene(self.mainScene)

        # _____ Highlight Selection _____
        self.selectionHighlight = SelectionHighlight(self)
        self.mainScene.addItem(self.selectionHighlight)

        # _____ Item Group For Selection _____
        self.selectedItemGroup = ItemGroup(mainView=self)
        self.selectedItemGroup.setZValue(9998)
        self.mainScene.addItem(self.selectedItemGroup)

        # _____ Signals _____
        self.IsCanvasEmpty.connect(self.MainContent.setCanvasEmpty)



    # _________ ADD/REMOVE CanvasItems _________
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

        canvasItems = tabData["canvasItems"]

        self.canvasItemData = canvasItems
        self.RemoveAllSelected()

        for item in self.mainScene.items(): # Only remove CanvasItems
            if issubclass(type(item), CanvasItem):      #! Remove
                self.mainScene.removeItem(item)

        self.canvasItems.clear()    # Remove all items on canvas

        self.SetCanvasItemCount()

        for canvasItem in canvasItems:          # Add all canvas items from canvasItems to the canvas. 
            self.AddCanvasItem(canvasItem)

        self.StoreZoomAmt()

    def AddNodeToDatabase(self, nodeData: dict):
        """Add Node Data to database

        Args:
            nodeData (dict): data that will be added to database
        """
        self.nodeHashTable[nodeData["nodeID"]] = nodeData

    def AddCanvasItem(self, canvasItemData):
        """Add CanvasItem to the canvas

        Args:
            CanvasItemData (dict): Data for CanvasItem

        Returns:
            (ImageCanvasItem): returns created CanvasItem
        """
        newCanvasItem = ImageCanvasItem(self, canvasItemData)

        self.mainScene.addItem(newCanvasItem)
        self.canvasItems.append(newCanvasItem)
        self.SetCanvasItemCount()
        
        self.SetZValues()

        return newCanvasItem


    def RemoveCanvasItem(self, canvasItem: CanvasItem):
        """Remove CanvasItem from Canvas

        Args:
            canvasItem (CanvasItem): Item to be deleted/removed from the canvas
        """

        self.canvasItems.remove(canvasItem)
        self.RemoveSelected(canvasItem)

        self.tabData["canvasItems"].pop(self.tabData["canvasItems"].index(canvasItem.canvasItemData))   # Remove data from canvasItem Database
        del self.nodeHashTable[canvasItem.nodeID]

        canvasItem.deleteLater()
        self.SetCanvasItemCount()


    def SetCanvasItemCount(self):
        """Used to update if prompt to add CanvasItem appears or not in mainContent.py"""

        if len(self.canvasItems) == 0:
            self.IsCanvasEmpty.emit(True)
        else:
            self.IsCanvasEmpty.emit(False)    
    # ________________________________________


    # _______________ Utility _______________
    def NewCanvasItemData(self, canvasItemData, nodeData):
        self.canvasItemData.append(canvasItemData)
        self.nodeHashTable[nodeData["nodeID"]] = nodeData

    def GetNodeData(self, nodeID:str):
        """Gets the data from the nodeHashTable (database of nodes)"""
        return self.nodeHashTable[nodeID]

    def SetNodeData(self, nodeID: str, nodeData:dict):
        """Sets the node data in nodeHashTable (database of nodes)
        
        Args:
            nodeID: id of node being set
            nodeData: data that is being set to the nodeID
        """
        self.nodeHashTable[nodeID] = nodeData


    def CanvasItemToFront(self, canvasItem):
        """Brings the CanvasItem to the front of the canvas
        Called when CanvasItem is selected 

        Args:
            canvasItem (CanvasItem): The CanvasItem that will be moved to the front.
        """
        self.canvasItems.append(self.canvasItems.pop(self.canvasItems.index(canvasItem)))
        self.canvasItemData.append(self.canvasItemData.pop(self.canvasItemData.index(canvasItem.canvasItemData))) # Move canvasItemData to front of list, so it persists across sessions
        self.SetZValues()

    def SetZValues(self):
        """Sets the z-index for every CanvasItem in the self.canvasItems list
        """
        for node in self.canvasItems:
            node.setZValue(self.canvasItems.index(node))

    def isItemAtPos(self, pos:QPoint, checkSelectionHighlight = false):
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

    def GetCanvasItemsFromList(self, list):
        tempList = []
        for item in list:
            if issubclass(type(item), CanvasItem):
                tempList.append(item)
        return tempList

    def SetSelectionHighlightPos(self):
        self.selectionHighlight.SelectionChanged(self.selectedItemGroup.childItems())

    def GetZoomScale(self):
        return self.transform().m11()

    def StoreZoomAmt(self):
        self.tabData["viewportZoom"] = self.GetZoomScale()

    def SetZoomScale(self, m11ZoomScale):
        originalTransform = self.transform()
        transform = QTransform(m11ZoomScale, originalTransform.m12(),originalTransform.m13(),originalTransform.m21(),m11ZoomScale,originalTransform.m23(),originalTransform.m31(),originalTransform.m32(),originalTransform.m33())
        QTransform()
        self.setTransform(transform)

    # def FormatCanvasItemWithinScene(self):    #! Implement outside of canvas item
        """This function ensures that the canvas item stays within the bounds of the scene."""
        # pass

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
            item.AddSelected(True)

    def AddSelected(self, canvasItem):
        """Add node to selection. Does not remove previous selection
        
        Arg:
            canvasItem: Item to be removed from the selection item group
        """
        if self.selectedItemGroup.childItems() == []:  # If it is the only selected item, bring to front.
            self.CanvasItemToFront(canvasItem)

        if canvasItem not in self.selectedItemGroup.childItems():  # Make sure item not already selected
            self.selectedItemGroup.addToGroup(canvasItem)

        self.SetSelectionHighlightPos()

    def RemoveSelected(self, canvasItem):
        """Removes the selected canvasItem passed
        
        Arg:
            canvasItem: Item to be removed from the selection item group
        """
        if canvasItem in self.selectedItemGroup.childItems():  
            self.selectedItemGroup.removeFromGroup(canvasItem)      

        self.SetSelectionHighlightPos()
        

    def RemoveAllSelected(self):
        """Removes all selected canvasItems from selectedItemGroup"""
        for item in self.selectedItemGroup.childItems():
            item.SetSelected(False)

        self.selectedItemGroup.resetTransform()

    #_________ Events _________
    def mousePressEvent(self, event):   
        if event.button() == Qt.MouseButton.MiddleButton:
            self.prevMousePos = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            return
        elif event.button() == Qt.MouseButton.RightButton:
            return

        elif event.button() == Qt.MouseButton.LeftButton:
            self.prevMousePos = event.pos()
            self.prevSelectedItems = []
            if not self.isItemAtPos(event.pos(), True):   # If item is at position, show rubber band
                self.rubberBand.setGeometry(QRect(event.pos(), QSize()))
                self.rubberBand.show()

        super().mousePressEvent(event)

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
        anchor = self.transformationAnchor()    # anchor allows for zoom in on mouse scene position
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        factor = 1.1            
        if event.angleDelta().y() < 0:
            factor = 0.9

        self.scale(factor, factor)
        self.setTransformationAnchor(anchor)

        # Save changes        
        self.StoreZoomAmt()
        self.tabData["viewportPos"] = [self.horizontalScrollBar().value(), self.verticalScrollBar().value()]


    def keyPressEvent(self, event) -> None:
        
        if event.key() == Qt.Key.Key_Delete:
            for item in self.selectedItemGroup.childItems():
                self.RemoveCanvasItem(item)

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
        

    # https://stackoverflow.com/a/3839127
    def mousePressEvent(self, event) -> None:
        """Mouse clicked on scene"""

        self.prevPos = event.scenePos()
        self.canDrag = True 

        self.pItemUnderMouse = self.items(event.scenePos()) # Detects if theres an item under the mouse click position
        self.topWidgetUnderMouse:CanvasItem = None

        # Set initial data for checking delta changes
        self.mainView.selectedItemGroup.SetInitialPos()
        self.mainView.selectedItemGroup.SetInitialSceneBoundingRect()
        self.mainView.selectedItemGroup.SetInitialSceneRectALL()


        # Get top widget
        for item in self.pItemUnderMouse:
            if issubclass(type(item), CanvasItem):  # Check if item is subclassed from CanvasItem.
                self.topWidgetUnderMouse = item
                break



        # If No item under mouse and and corner handle is under mouse, pass to SelectionHighlight
        if self.pItemUnderMouse != [] and type(self.pItemUnderMouse[0]) == SelectionHighlight:
            if self.pItemUnderMouse[0].isHandleUnderMouse(event.scenePos()):
                self.canDrag = False
                return super().mousePressEvent(event)   

        # No item under mouse click, unselect all items. (i.e. when the user clicks on the canvas)
        if (not self.topWidgetUnderMouse):   
            self.mainView.RemoveAllSelected()
            self.canDrag = False
            return  # Click event has been handled

        # Item is under mouse click.
        if (self.topWidgetUnderMouse != None and self.topWidgetUnderMouse.isEnabled() and not self.topWidgetUnderMouse.IsSelected() and self.topWidgetUnderMouse.flags() and QGraphicsItem.ItemIsSelectable):
            if event.modifiers() and Qt.Modifier.SHIFT: # If Shift held, add item to selection
                self.topWidgetUnderMouse.AddSelected(True)
                self.canDrag = False
            else:                                       # If Shift is not held, set as only selection.
                self.topWidgetUnderMouse.SetSelected(True)


        return super().mousePressEvent(event)   

    def mouseMoveEvent(self, event) -> None:
        """When the mouse moves, if item under mouse and is selected, drag item"""
        if event.buttons() == Qt.MouseButton.LeftButton and len(self.mainView.selectedItemGroup.childItems()) > 0 and self.topWidgetUnderMouse != None and self.canDrag:
            delta = event.scenePos() - self.prevPos

            self.mainView.selectedItemGroup.MoveGroup(delta)
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mainView.selectedItemGroup.SetItemData()
        return super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        """Used to open file when it is double clicked"""
        try:
            # Open File
            pass
        except:
            pass
        return

    
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
                        nodeData = CreateImageNode(url.toLocalFile())   # Do this first to ensure that the file exists.
                        canvasItemData = CreateCanvasItem(nodeData["nodeID"], initPosition, 1)

                        self.mainView.AddNodeToDatabase(nodeData)
                        self.mainView.AddCanvasItem(canvasItemData)
                        self.mainView.NewCanvasItemData(canvasItemData, nodeData)

                        initPosition += QPointF(10,10) # This offsets the dropped images by 10px x and y for each image dropped

                    else: # Is a file type
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

