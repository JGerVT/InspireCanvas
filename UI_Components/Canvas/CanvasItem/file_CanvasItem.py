#Imports
from pathlib import Path
from PIL.ImageQt import ImageQt
import os

#Components Used:
from UI_Components.Canvas.CanvasItem.baseCanvasItem import *  

class FileCanvasItem(CanvasItem):
    def __init__(self, parent, canvasItemData) -> None:
        super().__init__(parent, canvasItemData)

        # Set Attributes
        self.SetRect(QRectF(QPointF(self.itemPos.x(),self.itemPos.y()), QSize(300, 75)))

        # Data/Properties
        self.filePath = self.nodeData["filePath"]
        self.fileName = self.GetFileName(self.filePath)
        self.fileIcon = self.GetFileIcon(self.fileName).pixmap(QSize(50,50),QIcon.Normal,QIcon.On)

        # Icon
        self.icon = QGraphicsPixmapItem(self)
        self.scaled = QPixmap(self.fileIcon).scaled(50,50,Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.icon.setPixmap(self.scaled)
        self.icon.setPos(12, self.boundingRect().height()/2 - self.icon.boundingRect().height()/2)


    def paint(self, painter, option, widget) -> None:
        painter.setRenderHint(painter.Antialiasing, True)

        painter.save()

        # Draw Background
        painter.setBrush(QBrush("black"))
        painter.drawRoundedRect(self.boundingRect(), 5,5)


        # Draw Text
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)

        painter.setPen(QPen("White"))
        painter.drawText(QRect(72,0, self.boundingRect().width() - 80 - 12, self.boundingRect().height()), Qt.AlignmentFlag.AlignVCenter, self.fileName)


        painter.restore()
        return super().paint(painter, option, widget)

    def GetFileIcon(self, filePath) -> QIcon:

        fileInfo = QFileInfo(filePath)
        iconProvider = QFileIconProvider()
        icon = iconProvider.icon(fileInfo)
        return icon

    def GetFileName(self, filePath):
        return os.path.basename(filePath)