""" 
Description:  This python file provides the functionality for ImageCanvasItems on the Canvas

Date Created: 10/18/22 
Date Updated: 11/22/22
"""

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

        # INIT 
        self.image = self.getImage(self.imagePath)
        self.SetRect(QRectF(QPointF(self.itemPos.x(),self.itemPos.y()), QSize(self.imageSize.width(), self.imageSize.height())))

        if self.image == None:
            ConsoleLog.error("Unable to add ImageCanvasItem", "imagePath is invalid: " + str(self.canvasItemData) + "  imagePath: " + str(self.imagePath)) 
            
            del self.nodeData   # If unable to create image, delete self and data
            del self.canvasItemData
            self.deleteLater()


    def paint(self, painter, option, widget) -> None:

        painter.save()

        painter.setRenderHint(QPainter.Antialiasing,True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform,True)
        painter.setRenderHint(QPainter.LosslessImageRendering,True)

        painter.setClipRect(self.mapFromScene(self.mainCanvas.GetVisibleScreenRect()).boundingRect())

        painter.drawImage(self.image.rect(), self.image, self.image.rect())

        painter.restore()

        return super().paint(painter, option, widget)


    def getImage(self, path):
        """ Returns the converted image from the path.
            This is required to bypass a rendering error.
        """
        if CheckFileExists(path): # If image does not exist, delete self.
            try:
                pixmap = QImage()
                pixmap.load(path)
                self.imageSize = pixmap.size()
                return pixmap
            except:
                return None
        else:
            return None 