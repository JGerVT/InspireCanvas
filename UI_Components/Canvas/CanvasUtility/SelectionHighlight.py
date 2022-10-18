"""
Description:    This python file provides the selection border and corner resize buttons when items are selected. 
                This is not visible when there are no selected items on the canvas.

Date Created: 10/3/22 
Date Updated: 10/17/22
"""

# --Imports--
#PySide
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

# Custom Imports
from Utility.UtilityFunctions import *
from Settings.settings import *
from Utility import ConsoleLog


class SelectionHighlight(QGraphicsWidget):
    def __init__(self, parent) -> None:
        """Provides the SelectionHighlight/corner buttons when items are selected."""
        super(SelectionHighlight, self).__init__()        

        # References
        self.MainCanvas = parent

        # Property
        self.currentDrag = None
        self.cornerButtons = {"topLeft": QRect(), "topRight": QRect(),"bottomLeft": QRect(), "bottomRight": QRect()} # QRects for each corner to check if mouse is under.
        self.itemPadding: float = cornerResizeButtonRadius * 2 
        self.itemRect = QRectF()    # Size of the inner itemRect. Provides padding, so corner resize circular buttons do are not painted outside of self

        self.initialSize = self.size()

        # Set Attributes
        self.setAcceptHoverEvents(True)
        self.setZValue(9999) #Always on Top
        self.hide()

    def SetRect(self, rect:QRectF):
        """Sets the rect, as well as padding wo allow for corner resize buttons."""
        tempPadding = self.itemPadding/self.MainCanvas.GetZoomScale() # Divide by Zoom scale to ensure that it's always within the bounds
        self.itemRect = QRectF(tempPadding, tempPadding, rect.width(), rect.height())
        self.setGeometry(QRectF(rect.x() - tempPadding, rect.y() - tempPadding, rect.width() + tempPadding * 2, rect.height() + tempPadding * 2))

        # Update drawing to screen
        self.SetCornerButtons()
        self.update()

    def SelectionChanged(self, selectedItems):
        """Called when the selection is changed.

        Args:
            selectedItems (CanvasItem[]): list of all CanvasItems selected
        """
        if selectedItems == []: # Hide self if no items selected.
            self.hide()
        else:
            self.show()

        rect = self.MainCanvas.selectedItemGroup.sceneBoundingRect()
        self.SetRect(rect)


    def isHandleUnderMouse(self, eventPos):
        for handle in self.cornerButtons:
            if self.mapToScene(self.cornerButtons[handle]).boundingRect().contains(eventPos):
                return True

        return False

    def SetCornerButtons(self):
        """Set the position of each corner button to each corner of self.itemRect"""
        self.cornerButtons = {
            "topLeft": self.FormatCornerButton(self.itemRect.topLeft()), 
            "topRight": self.FormatCornerButton(self.itemRect.topRight()),
            "bottomLeft": self.FormatCornerButton(self.itemRect.bottomLeft()), 
            "bottomRight": self.FormatCornerButton(self.itemRect.bottomRight())  
        }

    def paint(self, painter, option, widget) -> None:
        """Used to draw border and corner resize buttons on item"""
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the border
        borderWidth = 2/self.MainCanvas.GetZoomScale()
        painter.setPen(QPen(QBrush(defaultAccentColor), borderWidth))
        painter.drawRect(self.itemRect)

        # Draw CornerResizeDots
        tempCornerSize = cornerResizeButtonRadius / self.MainCanvas.GetZoomScale()
        painter.setBrush(QBrush(defaultAccentColor))
        painter.drawEllipse(self.itemRect.topLeft(),      tempCornerSize, tempCornerSize)       # QPoint() adds offset for each corner
        painter.drawEllipse(self.itemRect.topRight(),     tempCornerSize, tempCornerSize)
        painter.drawEllipse(self.itemRect.bottomLeft(),   tempCornerSize, tempCornerSize)
        painter.drawEllipse(self.itemRect.bottomRight(),  tempCornerSize, tempCornerSize)



        painter.restore()
    
        return super().paint(painter, option, widget)

    def FormatCornerButton(self, point: QPoint):
        """This function formats the qpoint to return a QRect of the corner button"""
        tempCornerSize = cornerResizeButtonRadius / self.MainCanvas.GetZoomScale()
        return QRectF(point - QPoint(tempCornerSize, tempCornerSize),   # -QPoint() is offset, since drawEllipse draws around the QPoint
               QSize(tempCornerSize * 2, tempCornerSize * 2))           # QSize() * 2, because the tempCornerSize is radius, not diameter.


    # Events
    def mousePressEvent(self, event) -> None:
        self.initialDragPos = event.scenePos()

        self.initialSize = self.sceneBoundingRect().size()


        # Checks if corner re-size drag button is clicked. If button rect contains mouse position.
        if event.modifiers() and Qt.ShiftModifier and (self.cornerButtons["topLeft"].contains(event.pos()) or self.cornerButtons["bottomLeft"].contains(event.pos())):
            self.currentDrag = "leftCenter"
        elif event.modifiers() and Qt.ShiftModifier and (self.cornerButtons["topRight"].contains(event.pos()) or self.cornerButtons["bottomRight"].contains(event.pos())):
            self.currentDrag = "center"
        elif self.cornerButtons["topLeft"].contains(event.pos()):
            self.currentDrag = "topLeft"
        elif self.cornerButtons["topRight"].contains(event.pos()):
            self.currentDrag = "topRight"
        elif self.cornerButtons["bottomLeft"].contains(event.pos()):
            self.currentDrag = "bottomLeft"
        elif self.cornerButtons["bottomRight"].contains(event.pos()):
            self.currentDrag = "bottomRight"

        if self.currentDrag != None:    # Don't pass mouse event if mouse event is handled
            return None         
            
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.currentDrag = None
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        deltaDragPos = event.scenePos() - self.initialDragPos
        newSize = self.initialSize.width() + deltaDragPos.x()
        newScale = newSize / self.initialSize.width()
        
        if self.currentDrag != None:
            self.MainCanvas.selectedItemGroup.CalculateScale(deltaDragPos, self.currentDrag)

        return super().mouseMoveEvent(event)

    def hoverMoveEvent(self, event) -> None:
        # Set Mouse cursor depending on corner hovering over
        if self.cornerButtons["topLeft"].contains(event.pos()) or self.cornerButtons["bottomRight"].contains(event.pos()):
            self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        elif self.cornerButtons["topRight"].contains(event.pos()) or self.cornerButtons["bottomLeft"].contains(event.pos()):
            self.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        else:
            self.unsetCursor()
        return super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        self.unsetCursor()
        return super().hoverLeaveEvent(event)