"""
Description:    This python file provides an item group that will contain all selected canvasItems.
                This (QGraphicsItemGroup) makes it easy to move and scale collections of items

Date Created: 10/15/22 
Date Updated: 10/17/22
"""

# Imports
from Settings.settings import *

# https://www.walletfox.com/course/rotategroupqgraphicsitem.php
class ItemGroup(QGraphicsItemGroup):
    def __init__(self, mainView, parent = None) -> None:
        """Class that groups together selected items, to move as a single selected item.

        Args:
            mainView (MainCanvas): MainCanvas that is the parent.
        """
        super().__init__(parent)

        # References
        self.mainView = mainView
        
        # Properties
        self.initialPos = QPointF()
        self.initialSceneRect = QRectF()

    def SetPos(self, scenePos:QPointF):
        """Set the position of the item group (self)
        
        Args:
            scenePos (QPointF) : The location where self should be set.
        """
        sceneRect = self.scene().sceneRect()        
        prevPos = self.pos()    #! Fix this, if mouse moves fast, can have padding on corner. 
        self.setPos(scenePos)
        sceneBoundingRect = self.sceneBoundingRect()

        if sceneBoundingRect.top() < sceneRect.top():   # If items are moved outside bounds, revert to position before move happened
            self.setY(prevPos.y())
        if sceneBoundingRect.bottom() > sceneRect.bottom():
            self.setY(prevPos.y())
        if sceneBoundingRect.left() < sceneRect.left():
            self.setX(prevPos.x())
        if sceneBoundingRect.right() > sceneRect.right():
            self.setX(prevPos.x())

        self.mainView.SetSelectionHighlightPos()

    def SetInitialPos(self):
        """Set the initial position of the object. This is useful for getting the delta of a dragged item. (i.e. DeltaPos = self.initialPos - event.currentPos)"""
        self.initialPos = self.scenePos()

    def SetInitialSceneBoundingRect(self):
        """Sets the initial scene bounding rect"""
        self.initialSceneRect = self.sceneBoundingRect()

    def SetInitialSceneRectALL(self):
        """Sets the initial scene rect for all child items."""
        for item in self.childItems():
            item.setInitialSceneRect()

    def MoveGroup(self, delta:QPointF):
        """Move Group using self.initialPos + delta"""
        self.SetPos(self.initialPos + delta)

    def CalculateScale(self, delta :QPointF, cornerName: str = None):
        """Calculate the desired scale of the group"""
        canScale = True

        if cornerName == "topLeft" or cornerName == "bottomLeft":   # Invert if the left corner is used.
            delta = -delta
        elif cornerName == "leftCenter":
            delta = -delta * 2
        elif cornerName == "center":
            delta = delta * 2

        desiredScale = (self.initialSceneRect.width() + delta.x()) / self.boundingRect().width()

        #! Implement scaling limits

        # for item in self.childItems:
        #     print(item.nodeID, item.boundingRect().height(), item.initialScale, desiredScale, " = ", item.boundingRect().height() * item.initialScale * desiredScale)
        #     if type(item) == CanvasItem and item.boundingRect().height() * item.initialScale * desiredScale < minimumImageSize[1]:
        #         canScale = False

        if canScale:
            self.SetScale(desiredScale, cornerName)


    # https://stackoverflow.com/questions/56564499/how-to-rescale-graphicitems-without-disturbing-the-shape
    def SetScale(self, scale: float, cornerName: str = None):
        """Set the scale of the group of items. 
        
        Arg:
            scale (float) : Desired scale
            cornerName (str) : name of the corner being dragged
        """

        if not scale > .1: # Limit the scaling
            scale = .1

        if cornerName == "topLeft":     # Sets the pivot point based on the corner used.
            corner = self.boundingRect().bottomRight()

        elif cornerName == "topRight":
            corner = self.boundingRect().bottomLeft()
        
        elif cornerName == "bottomLeft":
            corner = self.boundingRect().topRight()

        elif cornerName == "bottomRight":
            corner = self.boundingRect().topLeft()
        
        elif cornerName == "center" or cornerName == "leftCenter": # If no cornerName passed, transform from center
            corner = self.boundingRect().center()


        beforeScale = self.mapToScene(corner)
        self.setScale(scale)
        afterScale = self.mapToScene(corner)
        offset = beforeScale - afterScale
        self.moveBy(offset.x(), offset.y())

        self.mainView.SetSelectionHighlightPos()


    def resetTransform(self) -> None:
        """When itemGroup is deselected, it will reset the scale, and reset the transform."""
        self.setScale(1)
        return super().resetTransform()

    def SetItemData(self):
        """Save data for child items. Used for persistent data between tab switches"""
        for item in self.childItems():
            item.SetData()