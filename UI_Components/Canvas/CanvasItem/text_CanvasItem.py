"""
Description:  This python file provides the functionality for Text CanvasItems on the Canvas 

Date Created: 10/23/22 
Date Updated: 11/22/22
"""

#Components Used:
from UI_Components.Canvas.CanvasItem.baseCanvasItem import *
from UI_Components.Canvas.CanvasUtility.ItemGroup import ItemGroup  

class TextCanvasItem(CanvasItem):
    def __init__(self, parent, canvasItemData) -> None:
        """ Provides the functionality for Text Canvas Items

        Args:
            canvasItemData (dict): CanvasItem data that is parsed and applied to the canvas item. 
        """
        super().__init__(parent, canvasItemData)

        # Set Attributes
        self.setMinimumWidth(35)
        self.text = TextBox(self)

        # Set Properties
        self.canEdit = False
        self.nodeData = self.mainCanvas.GetNodeData(self.nodeID) # Get Data by checking database with id

        # Node Data
        self.nodeText = self.nodeData["nodeText"]

        # INIT
        self.text.setPlainText(self.nodeText)

    # ----- Utility ----- 
    def isEditable(self):
        """Get if the text box can be edited."""
        return self.canEdit

    def setSize(self, size: QSizeF):
        """Sets the size of self. This is used when the TextBox's content has changed"""
        self.setGeometry(self.pos().x(),self.pos().y(), size.width(),size.height())

    def setIsEditable(self, canEdit:bool):
        """Sets if the text box can be edited.
        
        Args:
            canEdit (bool): If the text can be edited pass True
        
        """
        self.canEdit = canEdit
        if canEdit:
            self.text.setTextInteractionFlags(Qt.TextEditorInteraction)
            self.text.setFocus()
        else:
            self.text.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            self.text.ResetSelection()

    def setCanDrag(self, canDrag):
        """Sets if the canvasItem can be dragged or not."""
        self.setIsEditable(not canDrag)
        return super().setCanDrag(canDrag)

    def updateParentSize(self):
        """Used to update the geometry of the parent item group"""
        parent = self.parentItem()

        if type(parent) == ItemGroup:
            parent.removeFromGroup(self)
            parent.addToGroup(self)

    # ----- Events ----- 
    def mouseDoubleClickEvent(self, event) -> None:
        return super().mouseDoubleClickEvent(event)


    def mousePressEvent(self, event) -> None:
        return super().mousePressEvent(event)

    def paint(self, painter, option, widget) -> None:
        # Paint Background.
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)        
        painter.setBrush(QColor(0,0,0,150))
        painter.drawRoundedRect(self.boundingRect() + QMarginsF(-.5,-.5,-.5,-.5), 1, 1) # Margins are needed to keep border within selectionBorder
        painter.restore()
        return 

    def SetData(self):
        self.nodeData["nodeText"] = self.text.GetText()
        return super().SetData()

class TextBox(QGraphicsTextItem):
    def __init__(self, parent, text: str = ""):
        """Provides extended functionality for the QGraphicsTextItem"""
        super().__init__(text, parent=parent)

        # References
        self.textCanvasItem = parent

        # Set Attributes
        self.setDefaultTextColor(QColor("White"))

        # Signals
        self.document().contentsChanged.connect(self.ContentChanged)

    def GetText(self):
        return self.document().toPlainText()

    def ResetSelection(self):
        """Remove the selection of the text"""
        cursor = self.textCursor()
        cursor.setPosition(0, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

    # ----- Events -----
    def ContentChanged(self):
        """When content has changed, update the size of the parent"""
        self.textCanvasItem.setSize(self.boundingRect().size())
        self.textCanvasItem.updateParentSize()
        self.textCanvasItem.mainCanvas.SetSelectionHighlightPos()
        self.textCanvasItem.SetData()