#Imports
from pathlib import Path
from PIL.ImageQt import ImageQt

#Components Used:
from UI_Components.Canvas.CanvasItem.baseCanvasItem import *  

class ImageCanvasItem(CanvasItem):
    def __init__(self, parent, canvasItemData) -> None:
        super().__init__(parent, canvasItemData)

        # Properties/Data
        self.imagePath = self.nodeData["imagePath"]
        self.imageSize = QSize()

        self.pixmapItem = QGraphicsPixmapItem(parent=self)  # Image Data

        # Initiation 
        self.setImage(self.imagePath)
        self.SetRect(QRectF(QPointF(self.itemPos.x(),self.itemPos.y()), QSize(self.imageSize.width(), self.imageSize.height())))

    def setImage(self, path):
        """Sets the image to self.pixmapItem"""
        image = self.loadImage(path)

        pixmap = QPixmap()
        pixmap.convertFromImage(image)
        self.imageSize = pixmap.size()

        self.pixmapItem.setPixmap(pixmap) 

    def loadImage(self, path):
        """Loads image if file exists"""
        if Path(path).is_file():
            return ImageQt(path)
        else:
            ConsoleLog.alert("Image File does not exist.")
            self.deleteLater()


    def isWithinBounds(self):   #! Move to main canvas
        """Checks if self is within the bounds of the scene."""

        boundingRect = self.sceneBoundingRect()
        sceneRect = self.mainCanvas.scene().sceneRect()

        if boundingRect.topLeft().x() < sceneRect.topLeft().x():
            return False
        elif boundingRect.topLeft().y() < sceneRect.topLeft().y():
            return False
        elif boundingRect.bottomRight().x() > sceneRect.bottomRight().x():
            return False
        elif boundingRect.bottomRight().y() > sceneRect.bottomRight().y():
            return False
        
        return True

    def isLandscape(self, size: QSizeF):
        """If the width is longer than height, return true. If portrait, return false"""
        return size.width() > size.height()
