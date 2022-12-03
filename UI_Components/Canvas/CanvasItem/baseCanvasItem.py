""" 
Description:    This python file provides the base functionality for CanvasItems on the Canvas.
                Image, File, and Text CanvasItems inherit from this class.

Date Created: 10/18/22 
Date Updated: 11/22/22
"""

# Custom Imports
from Utility.UtilityFunctions import *
from Utility.ManageJSON import *
from Settings.settings import *
from Utility import ConsoleLog


class CanvasItem(QGraphicsWidget):
    itemPadding: float = 1
    itemRect = QRectF()
    def __init__(self, parent, canvasItemData) -> None:
        """ Provides the basic functionality for Canvas Items

        Args:
            canvasItemData (dict): CanvasItem data that is parsed and applied to the canvas item. 
        """
        super(CanvasItem, self).__init__()
        
        # Set Attributes
        self.setAcceptHoverEvents(False)
        self.setAcceptTouchEvents(False)

        # References
        self.mainCanvas = parent 
        self.canvasItemData = canvasItemData    # Used to store setting changes for persistent data.

        # CanvasItem Data
        self.nodeID : str = canvasItemData["nodeID"]
        self.itemPos = QPointF(canvasItemData["itemPos"][0], canvasItemData["itemPos"][1])
        self.itemScale : float = canvasItemData["itemScale"]

        # Node Data
        self.nodeData = self.mainCanvas.GetNodeData(self.nodeID) # Get Data by checking database with id
        self.nodeType = self.nodeData["nodeType"]
        self.nodeName = self.nodeData["nodeName"]
        self.creationTime = self.nodeData["creationTime"]

        # Properties
        self.isSelected_ = False
        self.initialSceneRect = self.sceneBoundingRect()
        self.initialScale = self.GetScale()
        self.canDrag = True
        self.initialPos = self.scenePos() # This is the offset used when items are moved

        # INIT
        self.setPos(self.itemPos)
        self.setScale(self.itemScale)

    def setCanDrag(self, canDrag:bool):
        """ This function sets whether self can be moved on the canvas on mouse drag.  

        Args:
            canDrag (bool): If self can be dragged.
        """
        self.canDrag = canDrag

    def setInitialPos(self, initialPos):
        self.initialPos = initialPos

    def setInitialSceneRect(self):
        self.initialSceneRect = self.sceneBoundingRect()
        self.initialScale = self.GetScale()
        
    def SetRect(self, rect:QRectF):
        """ Funciton that sets the size of self.

        Args:
            rect (QRectF): QRectF that will set the size of self
        """
        tempPadding = self.itemPadding/self.scale()/self.GetScale()
        self.itemRect = QRectF(tempPadding/2, tempPadding/2, rect.width() +  -tempPadding, rect.height() -tempPadding)
        self.setGeometry(rect)

    def GetScale(self):
        """ Get and return the scale of this object.

        Returns:
            (float): Returns the scale of this rect.
        """
        if self.boundingRect().width() == 0:
            return 1
        return self.sceneBoundingRect().width() / self.boundingRect().width()

    def paint(self, painter, option, widget) -> None:
        painter.save()

        painter.setRenderHint(painter.Antialiasing, True)

        # If is selected, Draw the border
        if self.isSelected_:   
            borderWidth = 1 / self.mainCanvas.GetZoomScale() / self.GetScale()
            painter.setPen(QPen(QBrush(defaultAccentColor), borderWidth))
            painter.drawRect(self.boundingRect())

        painter.restore()
    
        return super().paint(painter, option, widget)

    def GetIsSelected(self) -> bool:
        """Get if the current item is selected. Returns bool."""
        return self.isSelected_

    def SetSelected(self, selected: bool) -> None:
        """Set if the widget is selected or not

        Args:
            selected (bool): Do you want to select the widget?
        """
        self.isSelected_ = selected
        self.setCanDrag(True)

    def SetData(self):
        """When the user changes data, update the data in the database"""
        self.canvasItemData["itemPos"] = [self.scenePos().x(),self.scenePos().y()]
        self.canvasItemData["itemScale"] = self.GetScale()
