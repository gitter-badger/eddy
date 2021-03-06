# -*- coding: utf-8 -*-

##########################################################################
#                                                                        #
#  Eddy: a graphical editor for the specification of Graphol ontologies  #
#  Copyright (C) 2015 Daniele Pantaleone <danielepantaleone@me.com>      #
#                                                                        #
#  This program is free software: you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by  #
#  the Free Software Foundation, either version 3 of the License, or     #
#  (at your option) any later version.                                   #
#                                                                        #
#  This program is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
#  GNU General Public License for more details.                          #
#                                                                        #
#  You should have received a copy of the GNU General Public License     #
#  along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
#  #####################                          #####################  #
#                                                                        #
#  Graphol is developed by members of the DASI-lab group of the          #
#  Dipartimento di Ingegneria Informatica, Automatica e Gestionale       #
#  A.Ruberti at Sapienza University of Rome: http://www.dis.uniroma1.it  #
#                                                                        #
#     - Domenico Lembo <lembo@dis.uniroma1.it>                           #
#     - Valerio Santarelli <santarelli@dis.uniroma1.it>                  #
#     - Domenico Fabio Savo <savo@dis.uniroma1.it>                       #
#     - Marco Console <console@dis.uniroma1.it>                          #
#                                                                        #
##########################################################################


from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QPolygonF, QPainterPath, QPixmap, QPainter, QPen, QColor, QBrush

from eddy.core.datatypes import Item, Special, Identity
from eddy.core.functions import snapF
from eddy.core.items.nodes.common.base import AbstractResizableNode
from eddy.core.items.nodes.common.label import Label
from eddy.core.qt import Font


class RoleNode(AbstractResizableNode):
    """
    This class implements the 'Role' node.
    """
    indexL = 0
    indexB = 1
    indexT = 3
    indexR = 2
    indexE = 4

    identities = {Identity.Role}
    item = Item.RoleNode
    minheight = 50
    minwidth = 70

    def __init__(self, width=minwidth, height=minheight, brush=None, **kwargs):
        """
        Initialize the node.
        :type width: int
        :type height: int
        :type brush: QBrush
        """
        super().__init__(**kwargs)
        w = max(width, self.minwidth)
        h = max(height, self.minheight)
        s = self.handleSize
        self.brush = brush or QBrush(QColor(252, 252, 252))
        self.pen = QPen(QColor(0, 0, 0), 1.1, Qt.SolidLine)
        self.polygon = self.createPolygon(w, h)
        self.background = self.createBackground(w + s, h + s)
        self.selection = self.createSelection(w + s, h + s)
        self.label = Label('role', parent=self)
        self.label.updatePos()
        self.updateHandles()

    ####################################################################################################################
    #                                                                                                                  #
    #   PROPERTIES                                                                                                     #
    #                                                                                                                  #
    ####################################################################################################################

    @property
    def asymmetric(self):
        """
        Tells whether the Role is defined as asymmetric.
        :rtype: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        return meta.asymmetry

    @asymmetric.setter
    def asymmetric(self, value):
        """
        Set the Role asymmetry property.
        :type value: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        meta.asymmetry = bool(value)
        scene.meta.add(self.item, self.text(), meta)

    @property
    def functional(self):
        """
        Tells whether the Role is defined as functional.
        :rtype: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        return meta.functionality

    @functional.setter
    def functional(self, value):
        """
        Set the Role functionality property.
        :type value: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        meta.functionality = bool(value)
        scene.meta.add(self.item, self.text(), meta)

    @property
    def identity(self):
        """
        Returns the identity of the current node.
        :rtype: Identity
        """
        return Identity.Role

    @identity.setter
    def identity(self, identity):
        """
        Set the identity of the current node.
        :type identity: Identity
        """
        pass

    @property
    def inverseFunctional(self):
        """
        Tells whether the Role is defined as inverse functional.
        :rtype: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        return meta.inverseFunctionality

    @inverseFunctional.setter
    def inverseFunctional(self, value):
        """
        Set the Role inverse functionality property.
        :type value: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        meta.inverseFunctionality = bool(value)
        scene.meta.add(self.item, self.text(), meta)

    @property
    def irreflexive(self):
        """
        Tells whether the Role is defined as irreflexive.
        :rtype: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        return meta.irreflexivity

    @irreflexive.setter
    def irreflexive(self, value):
        """
        Set the Role irreflexivity property.
        :type value: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        meta.irreflexivity = bool(value)
        scene.meta.add(self.item, self.text(), meta)

    @property
    def reflexive(self):
        """
        Tells whether the Role is defined as reflexive.
        :rtype: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        return meta.reflexivity

    @reflexive.setter
    def reflexive(self, value):
        """
        Set the Role reflexivity property.
        :type value: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        meta.reflexivity = bool(value)
        scene.meta.add(self.item, self.text(), meta)

    @property
    def special(self):
        """
        Returns the special type of this node.
        :rtype: Special
        """
        return Special.forValue(self.text())

    @property
    def symmetric(self):
        """
        Tells whether the Role is defined as symmetric.
        :rtype: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        return meta.symmetry

    @symmetric.setter
    def symmetric(self, value):
        """
        Set the Role symmetry property.
        :type value: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        meta.symmetry = bool(value)
        scene.meta.add(self.item, self.text(), meta)

    @property
    def transitive(self):
        """
        Tells whether the Role is defined as transitive.
        :rtype: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        return meta.transitivity

    @transitive.setter
    def transitive(self, value):
        """
        Set the Role transitivity property.
        :type value: bool
        """
        scene = self.scene()
        meta = scene.meta.metaFor(self.item, self.text())
        meta.transitivity = bool(value)
        scene.meta.add(self.item, self.text(), meta)

    ####################################################################################################################
    #                                                                                                                  #
    #   INTERFACE                                                                                                      #
    #                                                                                                                  #
    ####################################################################################################################

    def copy(self, scene):
        """
        Create a copy of the current item.
        :type scene: DiagramScene
        """
        kwargs = {
            'id': self.id,
            'brush': self.brush,
            'height': self.height(),
            'width': self.width(),
        }
        node = scene.factory.create(item=self.item, scene=scene, **kwargs)
        node.setPos(self.pos())
        node.setText(self.text())
        node.setTextPos(node.mapFromScene(self.mapToScene(self.textPos())))
        return node
    
    @staticmethod
    def createBackground(width, height):
        """
        Returns the initialized background polygon according to the given width/height.
        :type width: int
        :type height: int
        :rtype: QPolygonF
        """
        return QPolygonF([
            QPointF(-width / 2, 0),
            QPointF(0, +height / 2),
            QPointF(+width / 2, 0),
            QPointF(0, -height / 2),
            QPointF(-width / 2, 0)
        ])
    
    @staticmethod
    def createPolygon(width, height):
        """
        Returns the initialized polygon according to the given width/height.
        :type width: int
        :type height: int
        :rtype: QPolygonF
        """
        return QPolygonF([
            QPointF(-width / 2, 0),
            QPointF(0, +height / 2),
            QPointF(+width / 2, 0),
            QPointF(0, -height / 2),
            QPointF(-width / 2, 0)
        ])

    def height(self):
        """
        Returns the height of the shape.
        :rtype: int
        """
        return self.polygon[self.indexB].y() - self.polygon[self.indexT].y()

    def interactiveResize(self, mousePos):
        """
        Handle the interactive resize of the shape.
        :type mousePos: QPointF
        """
        scene = self.scene()
        snap = scene.mainwindow.snapToGrid
        size = scene.GridSize
        offset = self.handleSize + self.handleMove
        moved = self.label.moved
        
        R = QRectF(self.boundingRect())
        D = QPointF(0, 0)

        minBoundW = self.minwidth + offset * 2
        minBoundH = self.minheight + offset * 2

        self.prepareGeometryChange()

        if self.mousePressHandle == self.handleTL:

            fromX = self.mousePressBound.left()
            fromY = self.mousePressBound.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            toX = snapF(toX, size, -offset, snap)
            toY = snapF(toY, size, -offset, snap)
            D.setX(toX - fromX)
            D.setY(toY - fromY)
            R.setLeft(toX)
            R.setTop(toY)

            ## CLAMP SIZE
            if R.width() < minBoundW:
                D.setX(D.x() - minBoundW + R.width())
                R.setLeft(R.left() - minBoundW + R.width())
            if R.height() < minBoundH:
                D.setY(D.y() - minBoundH + R.height())
                R.setTop(R.top() - minBoundH + R.height())
            
            self.selection.setLeft(R.left())
            self.selection.setTop(R.top())
            
            self.background[self.indexT] = QPointF(R.left() + R.width() / 2, R.top())
            self.background[self.indexB] = QPointF(R.left() + R.width() / 2, self.background[self.indexB].y())
            self.background[self.indexL] = QPointF(R.left(), R.top() + R.height() / 2)
            self.background[self.indexE] = QPointF(R.left(), R.top() + R.height() / 2)
            self.background[self.indexR] = QPointF(self.background[self.indexR].x(), R.top() + R.height() / 2)
            
            self.polygon[self.indexT] = QPointF(R.left() + R.width() / 2, R.top() + offset)
            self.polygon[self.indexB] = QPointF(R.left() + R.width() / 2, self.polygon[self.indexB].y())
            self.polygon[self.indexL] = QPointF(R.left() + offset, R.top() + R.height() / 2)
            self.polygon[self.indexE] = QPointF(R.left() + offset, R.top() + R.height() / 2)
            self.polygon[self.indexR] = QPointF(self.polygon[self.indexR].x(), R.top() + R.height() / 2)

        elif self.mousePressHandle == self.handleTM:

            fromY = self.mousePressBound.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            toY = snapF(toY, size, -offset, snap)
            D.setY(toY - fromY)
            R.setTop(toY)

            ## CLAMP SIZE
            if R.height() < minBoundH:
                D.setY(D.y() - minBoundH + R.height())
                R.setTop(R.top() - minBoundH + R.height())
            
            self.selection.setTop(R.top())
            
            self.background[self.indexT] = QPointF(self.background[self.indexT].x(), R.top())
            self.background[self.indexL] = QPointF(self.background[self.indexL].x(), R.top() + R.height() / 2)
            self.background[self.indexE] = QPointF(self.background[self.indexE].x(), R.top() + R.height() / 2)
            self.background[self.indexR] = QPointF(self.background[self.indexR].x(), R.top() + R.height() / 2)
            
            self.polygon[self.indexT] = QPointF(self.polygon[self.indexT].x(), R.top() + offset)
            self.polygon[self.indexL] = QPointF(self.polygon[self.indexL].x(), R.top() + R.height() / 2)
            self.polygon[self.indexE] = QPointF(self.polygon[self.indexE].x(), R.top() + R.height() / 2)
            self.polygon[self.indexR] = QPointF(self.polygon[self.indexR].x(), R.top() + R.height() / 2)

        elif self.mousePressHandle == self.handleTR:

            fromX = self.mousePressBound.right()
            fromY = self.mousePressBound.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            toX = snapF(toX, size, +offset, snap)
            toY = snapF(toY, size, -offset, snap)
            D.setX(toX - fromX)
            D.setY(toY - fromY)
            R.setRight(toX)
            R.setTop(toY)

            ## CLAMP SIZE
            if R.width() < minBoundW:
                D.setX(D.x() + minBoundW - R.width())
                R.setRight(R.right() + minBoundW - R.width())
            if R.height() < minBoundH:
                D.setY(D.y() - minBoundH + R.height())
                R.setTop(R.top() - minBoundH + R.height())
            
            self.selection.setRight(R.right())
            self.selection.setTop(R.top())
            
            self.background[self.indexT] = QPointF(R.right() - R.width() / 2, R.top())
            self.background[self.indexB] = QPointF(R.right() - R.width() / 2, self.background[self.indexB].y())
            self.background[self.indexL] = QPointF(self.background[self.indexL].x(), R.top() + R.height() / 2)
            self.background[self.indexE] = QPointF(self.background[self.indexE].x(), R.top() + R.height() / 2)
            self.background[self.indexR] = QPointF(R.right(), R.top() + R.height() / 2)
            
            self.polygon[self.indexT] = QPointF(R.right() - R.width() / 2, R.top() + offset)
            self.polygon[self.indexB] = QPointF(R.right() - R.width() / 2, self.polygon[self.indexB].y())
            self.polygon[self.indexL] = QPointF(self.polygon[self.indexL].x(), R.top() + R.height() / 2)
            self.polygon[self.indexE] = QPointF(self.polygon[self.indexE].x(), R.top() + R.height() / 2)
            self.polygon[self.indexR] = QPointF(R.right() - offset, R.top() + R.height() / 2)

        elif self.mousePressHandle == self.handleML:

            fromX = self.mousePressBound.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toX = snapF(toX, size, -offset, snap)
            D.setX(toX - fromX)
            R.setLeft(toX)

            ## CLAMP SIZE
            if R.width() < minBoundW:
                D.setX(D.x() - minBoundW + R.width())
                R.setLeft(R.left() - minBoundW + R.width())
            
            self.selection.setLeft(R.left())
            
            self.background[self.indexL] = QPointF(R.left(), self.mousePressBound.top() + self.mousePressBound.height() / 2)
            self.background[self.indexE] = QPointF(R.left(), self.mousePressBound.top() + self.mousePressBound.height() / 2)
            self.background[self.indexT] = QPointF(R.left() + R.width() / 2, self.background[self.indexT].y())
            self.background[self.indexB] = QPointF(R.left() + R.width() / 2, self.background[self.indexB].y())
            
            self.polygon[self.indexL] = QPointF(R.left() + offset, self.mousePressBound.top() + self.mousePressBound.height() / 2)
            self.polygon[self.indexE] = QPointF(R.left() + offset, self.mousePressBound.top() + self.mousePressBound.height() / 2)
            self.polygon[self.indexT] = QPointF(R.left() + R.width() / 2, self.polygon[self.indexT].y())
            self.polygon[self.indexB] = QPointF(R.left() + R.width() / 2, self.polygon[self.indexB].y())

        elif self.mousePressHandle == self.handleMR:

            fromX = self.mousePressBound.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toX = snapF(toX, size, +offset, snap)
            D.setX(toX - fromX)
            R.setRight(toX)

            ## CLAMP SIZE
            if R.width() < minBoundW:
                D.setX(D.x() + minBoundW - R.width())
                R.setRight(R.right() + minBoundW - R.width())
            
            self.selection.setRight(R.right())
            
            self.background[self.indexR] = QPointF(R.right(), self.mousePressBound.top() + self.mousePressBound.height() / 2)
            self.background[self.indexT] = QPointF(R.right() - R.width() / 2, self.background[self.indexT].y())
            self.background[self.indexB] = QPointF(R.right() - R.width() / 2, self.background[self.indexB].y())
            
            self.polygon[self.indexR] = QPointF(R.right() - offset, self.mousePressBound.top() + self.mousePressBound.height() / 2)
            self.polygon[self.indexT] = QPointF(R.right() - R.width() / 2, self.polygon[self.indexT].y())
            self.polygon[self.indexB] = QPointF(R.right() - R.width() / 2, self.polygon[self.indexB].y())

        elif self.mousePressHandle == self.handleBL:

            fromX = self.mousePressBound.left()
            fromY = self.mousePressBound.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            toX = snapF(toX, size, -offset, snap)
            toY = snapF(toY, size, +offset, snap)
            D.setX(toX - fromX)
            D.setY(toY - fromY)
            R.setLeft(toX)
            R.setBottom(toY)

            ## CLAMP SIZE
            if R.width() < minBoundW:
                D.setX(D.x() - minBoundW + R.width())
                R.setLeft(R.left() - minBoundW + R.width())
            if R.height() < minBoundH:
                D.setY(D.y() + minBoundH - R.height())
                R.setBottom(R.bottom() + minBoundH - R.height())
            
            self.selection.setLeft(R.left())
            self.selection.setBottom(R.bottom())
            
            self.background[self.indexT] = QPointF(R.left() + R.width() / 2, self.background[self.indexT].y())
            self.background[self.indexB] = QPointF(R.left() + R.width() / 2, R.bottom())
            self.background[self.indexL] = QPointF(R.left(), R.bottom() - R.height() / 2)
            self.background[self.indexE] = QPointF(R.left(), R.bottom() - R.height() / 2)
            self.background[self.indexR] = QPointF(self.background[self.indexR].x(), R.bottom() - R.height() / 2)
            
            self.polygon[self.indexT] = QPointF(R.left() + R.width() / 2, self.polygon[self.indexT].y())
            self.polygon[self.indexB] = QPointF(R.left() + R.width() / 2, R.bottom() - offset)
            self.polygon[self.indexL] = QPointF(R.left() + offset, R.bottom() - R.height() / 2)
            self.polygon[self.indexE] = QPointF(R.left() + offset, R.bottom() - R.height() / 2)
            self.polygon[self.indexR] = QPointF(self.polygon[self.indexR].x(), R.bottom() - R.height() / 2)

        elif self.mousePressHandle == self.handleBM:

            fromY = self.mousePressBound.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            toY = snapF(toY, size, +offset, snap)
            D.setY(toY - fromY)
            R.setBottom(toY)

            ## CLAMP SIZE
            if R.height() < minBoundH:
                D.setY(D.y() + minBoundH - R.height())
                R.setBottom(R.bottom() + minBoundH - R.height())
            
            self.selection.setBottom(R.bottom())
            
            self.background[self.indexB] = QPointF(self.background[self.indexB].x(), R.bottom())
            self.background[self.indexL] = QPointF(self.background[self.indexL].x(), R.top() + R.height() / 2)
            self.background[self.indexE] = QPointF(self.background[self.indexE].x(), R.top() + R.height() / 2)
            self.background[self.indexR] = QPointF(self.background[self.indexR].x(), R.top() + R.height() / 2)
            
            self.polygon[self.indexB] = QPointF(self.polygon[self.indexB].x(), R.bottom() - offset)
            self.polygon[self.indexL] = QPointF(self.polygon[self.indexL].x(), R.top() + R.height() / 2)
            self.polygon[self.indexE] = QPointF(self.polygon[self.indexE].x(), R.top() + R.height() / 2)
            self.polygon[self.indexR] = QPointF(self.polygon[self.indexR].x(), R.top() + R.height() / 2)

        elif self.mousePressHandle == self.handleBR:

            fromX = self.mousePressBound.right()
            fromY = self.mousePressBound.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            toX = snapF(toX, size, +offset, snap)
            toY = snapF(toY, size, +offset, snap)
            D.setX(toX - fromX)
            D.setY(toY - fromY)
            R.setRight(toX)
            R.setBottom(toY)

            ## CLAMP SIZE
            if R.width() < minBoundW:
                D.setX(D.x() + minBoundW - R.width())
                R.setRight(R.right() + minBoundW - R.width())
            if R.height() < minBoundH:
                D.setY(D.y() + minBoundH - R.height())
                R.setBottom(R.bottom() + minBoundH - R.height())

            self.selection.setRight(R.right())
            self.selection.setBottom(R.bottom())

            self.background[self.indexT] = QPointF(R.right() - R.width() / 2, self.background[self.indexT].y())
            self.background[self.indexB] = QPointF(R.right() - R.width() / 2, R.bottom())
            self.background[self.indexL] = QPointF(self.background[self.indexL].x(), R.bottom() - R.height() / 2)
            self.background[self.indexE] = QPointF(self.background[self.indexE].x(), R.bottom() - R.height() / 2)
            self.background[self.indexR] = QPointF(R.right(), R.bottom() - R.height() / 2)
            
            self.polygon[self.indexT] = QPointF(R.right() - R.width() / 2, self.polygon[self.indexT].y())
            self.polygon[self.indexB] = QPointF(R.right() - R.width() / 2, R.bottom() - offset)
            self.polygon[self.indexL] = QPointF(self.polygon[self.indexL].x(), R.bottom() - R.height() / 2)
            self.polygon[self.indexE] = QPointF(self.polygon[self.indexE].x(), R.bottom() - R.height() / 2)
            self.polygon[self.indexR] = QPointF(R.right() - offset, R.bottom() - R.height() / 2)

        self.updateHandles()
        self.updateTextPos(moved=moved)
        self.updateAnchors(self.mousePressData, D)

    def width(self):
        """
        Returns the width of the shape.
        :rtype: int
        """
        return self.polygon[self.indexR].x() - self.polygon[self.indexL].x()

    ####################################################################################################################
    #                                                                                                                  #
    #   GEOMETRY                                                                                                       #
    #                                                                                                                  #
    ####################################################################################################################

    def boundingRect(self):
        """
        Returns the shape bounding rectangle.
        :rtype: QRectF
        """
        return self.selection

    def painterPath(self):
        """
        Returns the current shape as QPainterPath (used for collision detection).
        :rtype: QPainterPath
        """
        path = QPainterPath()
        path.addPolygon(self.polygon)
        return path

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        :rtype: QPainterPath
        """
        path = QPainterPath()
        path.addPolygon(self.polygon)
        for shape in self.handleBound:
            path.addEllipse(shape)
        return path

    ####################################################################################################################
    #                                                                                                                  #
    #   LABEL SHORTCUTS                                                                                                #
    #                                                                                                                  #
    ####################################################################################################################

    def textPos(self):
        """
        Returns the current label position in item coordinates.
        :rtype: QPointF
        """
        return self.label.pos()

    def text(self):
        """
        Returns the label text.
        :rtype: str
        """
        return self.label.text()

    def setTextPos(self, pos):
        """
        Set the label position.
        :type pos: QPointF
        """
        self.label.setPos(pos)

    def setText(self, text):
        """
        Set the label text.
        :type text: str
        """
        self.label.editable = Special.forValue(text) is None
        self.label.setText(text)

    def updateTextPos(self, *args, **kwargs):
        """
        Update the label position.
        """
        self.label.updatePos(*args, **kwargs)

    ####################################################################################################################
    #                                                                                                                  #
    #   DRAWING                                                                                                        #
    #                                                                                                                  #
    ####################################################################################################################

    @classmethod
    def image(cls, **kwargs):
        """
        Returns an image suitable for the palette.
        :rtype: QPixmap
        """
        # INITIALIZATION
        pixmap = QPixmap(kwargs['w'], kwargs['h'])
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        polygon = cls.createPolygon(46, 34)
        # ITEM SHAPE
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(0, 0, 0), 1.1, Qt.SolidLine))
        painter.setBrush(QColor(252, 252, 252))
        painter.translate(kwargs['w'] / 2, kwargs['h'] / 2)
        painter.drawPolygon(polygon)
        # TEXT WITHIN SHAPE
        painter.setFont(Font('Arial', 11, Font.Light))
        painter.drawText(polygon.boundingRect(), Qt.AlignCenter, 'role')
        return pixmap

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the diagram scene.
        :type painter: QPainter
        :type option: QStyleOptionGraphicsItem
        :type widget: QWidget
        """
        # SET THE RECT THAT NEEDS TO BE REPAINTED
        painter.setClipRect(option.exposedRect)
        # SELECTION AREA
        painter.setPen(self.selectionPen)
        painter.setBrush(self.selectionBrush)
        painter.drawRect(self.selection)
        # SYNTAX VALIDATION
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.backgroundPen)
        painter.setBrush(self.backgroundBrush)
        painter.drawPolygon(self.background)
        # ITEM SHAPE
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPolygon(self.polygon)
        # RESIZE HANDLES
        painter.setRenderHint(QPainter.Antialiasing)
        for i in range(self.handleNum):
            painter.setBrush(self.handleBrush[i])
            painter.setPen(self.handlePen[i])
            painter.drawEllipse(self.handleBound[i])