# Custom Imports
from Utility.UtilityFunctions import *
from Utility.ManageJSON import *
from Settings.settings import *
from Utility import ConsoleLog


class CanvasItem(QGraphicsWidget):
    itemPadding: float = 1
    itemRect = QRectF()
    def __init__(self, parent, canvasItemData) -> None:
        """_summary_

        Args:
            parent (_type_): _description_
        """
        super(CanvasItem, self).__init__()
        
        # Set Attributes
        self.setAcceptHoverEvents(False)
        self.setAcceptTouchEvents(False)
        # self.installEventFilter(self)

        # References
        self.mainCanvas = parent 
        self.canvasItemData = canvasItemData    # Used to store setting changes for persistent data.

        # Data
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

        # Init
        self.setPos(self.itemPos)
        self.setScale(self.itemScale)

        defaultSize = QSize(720,480)
        self.SetRect(QRectF(QPointF(self.itemPos.x(),self.itemPos.y()),defaultSize))

    def setCanDrag(self, canDrag):
        self.canDrag = canDrag

    def setInitialPos(self, initialPos):
        self.initialPos = initialPos

    def setInitialSceneRect(self):
        self.initialSceneRect = self.sceneBoundingRect()
        self.initialScale = self.GetScale()
        
    def SetRect(self, rect:QRectF):
        tempPadding = self.itemPadding/self.scale()/self.GetScale()
        self.itemRect = QRectF(tempPadding/2, tempPadding/2, rect.width() +  -tempPadding, rect.height() -tempPadding)
        self.setGeometry(rect)

    def GetScale(self):
        if self.boundingRect().width() == 0:
            return 1
        return self.sceneBoundingRect().width() / self.boundingRect().width()

    def paint(self, painter, option, widget) -> None:
        """Used to draw border of item, when selected"""
        painter.save()

        painter.setRenderHint(painter.Antialiasing, True)

        if self.isSelected_:   # If is selected, Draw the border
            borderWidth = 1 / self.mainCanvas.GetZoomScale() / self.GetScale()
            painter.setPen(QPen(QBrush(defaultAccentColor), borderWidth))
            painter.drawRect(self.boundingRect())

        painter.restore()
    
        return super().paint(painter, option, widget)

    def IsSelected(self) -> bool:
        return self.isSelected_

    def SetSelected(self, selected: bool) -> None:
        """Set if the widget is selected or not

        Args:
            selected (bool): Do you want to select the widget?
        """
        self.isSelected_ = selected
        self.setCanDrag(True)

    def itemChange(self, change, value):
        if (change == QGraphicsItem.ItemPositionChange and self.scene() or change == QGraphicsItem.ItemScenePositionHasChanged):
            self.mainCanvas.SetSelectionHighlightPos()

        return super().itemChange(change, value)

    def SetData(self):
        """When the user changes data, set the data in the database."""
        self.canvasItemData["itemPos"] = [self.scenePos().x(),self.scenePos().y()]
        self.canvasItemData["itemScale"] = self.GetScale()
