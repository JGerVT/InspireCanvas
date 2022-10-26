"""
Description:  This file provides the Text Item Canvas Node, which displays text to the Canvas 

Date Created: 10/23/22 
Date Updated: 10/23/22
"""

#Components Used:
from UI_Components.Canvas.CanvasItem.baseCanvasItem import *  

class TextCanvasItem(CanvasItem):
    def __init__(self, parent, canvasItemData) -> None:
        super().__init__(parent, canvasItemData)

        # Set Attributes
        # self.setMinimumSize(QSize(80,40))

        # Properties
        self.isEditable = False

        # 
        self.text = TextBox(self)
        self.text.setPlainText("TEST")

        self.setIsEditable(True)

    def setSize(self, size: QSizeF):
        self.setGeometry(self.pos().x(),self.pos().y(), size.width(),size.height())

    def mouseDoubleClickEvent(self, event) -> None:
        print("TEST")
        return super().mouseDoubleClickEvent(event)

    def setIsEditable(self, isEditable):
        self.isEditable = isEditable

        if isEditable:
            self.text.setTextInteractionFlags(Qt.TextEditable)
        else:
            self.text.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)


    def mousePressEvent(self, event) -> None:
        # print("2")
        return super().mousePressEvent(event)

    def paint(self, painter, option, widget) -> None:


        painter.save()
        painter.setBrush(QBrush("#00000"))
        painter.drawRect(self.boundingRect())
        painter.restore()

        # return super().paint(painter, option, widget)


class TextBox(QGraphicsTextItem):
    def __init__(self, parent, text: str = ""):
        super().__init__(text, parent=parent)

        # References
        self.textCanvasItem = parent

        self.setDefaultTextColor(QColor("White"))

        self.document().contentsChanged.connect(self.ContentChanged)

    def mousePressEvent(self, event) -> None:
        print("TST")
        return super().mousePressEvent(event)

    def ContentChanged(self):
        # print(self.document().toPlainText())
        self.textCanvasItem.setSize(self.boundingRect().size())
        self.textCanvasItem.mainCanvas.SetSelectionHighlightPos()
