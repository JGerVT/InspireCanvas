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
        self.pixmapItem.setCacheMode(self.cacheMode().DeviceCoordinateCache)

        # INIT 
        image = self.getImage(self.imagePath)
        if image != None:
            self.pixmapItem.setPixmap(self.getImage(self.imagePath))    # Set Image to self.pixmapItem
            self.SetRect(QRectF(QPointF(self.itemPos.x(),self.itemPos.y()), QSize(self.imageSize.width(), self.imageSize.height())))

            ConsoleLog.log("Added ImageCanvasItem", "Successfully added Image. canvasItem: " + str(self.canvasItemData) + "  imagePath: " + self.imagePath) 

        else:
            ConsoleLog.error("Unable to add ImageCanvasItem", "imagePath is invalid: " + str(self.canvasItemData) + "  imagePath: " + str(self.imagePath)) 
            
            del self.nodeData   # If unable to create image, delete self and data
            del self.canvasItemData
            self.deleteLater()

    def getImage(self, path):
        """ Returns the converted image from the path.
            This is required to bypass a rendering error.
        """
        if CheckFileExists(path): # If image does not exist, delete self.
            try:
                image = self.loadImage(path)

                pixmap = QPixmap()
                pixmap.convertFromImage(image)
                self.imageSize = pixmap.size()
                return pixmap
            except:
                return None
        else:
            return None 

    def loadImage(self, path):
        """ Loads image if file exists
            If image does not exist, delete self.
        """
        if CheckFileExists(path):
            return ImageQt(path)
        else:
            ConsoleLog.alert("Image File does not exist.")
            self.deleteLater()