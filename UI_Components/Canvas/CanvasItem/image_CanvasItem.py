""" 
Description:  This python file provides the functionality for ImageCanvasItems on the Canvas

Date Created: 10/18/22 
Date Updated: 11/22/22
"""

#Imports
from pathlib import Path
from PIL.ImageQt import ImageQt

#Components Used:
from UI_Components.Canvas.CanvasItem.baseCanvasItem import *  

class ImageCanvasItem(CanvasItem):
    def __init__(self, parent, canvasItemData) -> None:
        """ Provides the functionality for Image Canvas Items

        Args:
            canvasItemData (dict): CanvasItem data that is parsed and applied to the canvas item. 
        """
        super().__init__(parent, canvasItemData)

        # Node Data
        self.imagePath = self.nodeData["imagePath"]

        # Properties
        self.imageSize = QSize()
        self.pixmapItem = QGraphicsPixmapItem(parent=self)  # Image Data

        # INIT 
        self.pixmapItem.setPixmap(self.getImage(self.imagePath))    # Set Image to self.pixmapItem
        self.SetRect(QRectF(QPointF(self.itemPos.x(),self.itemPos.y()), QSize(self.imageSize.width(), self.imageSize.height())))

    def getImage(self, path):
        """ Returns the converted image from the path.
            This is required to bypass a rendering error.
        """
        image = self.loadImage(path)

        pixmap = QPixmap()
        pixmap.convertFromImage(image)
        self.imageSize = pixmap.size()

        return pixmap

    def loadImage(self, path):
        """ Loads image if file exists
            If image does not exist, delete self.
        """
        if Path(path).is_file():
            return ImageQt(path)
        else:
            ConsoleLog.alert("Image File does not exist.")
            self.deleteLater()