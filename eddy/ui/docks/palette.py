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


from PyQt5.QtCore import Qt, QSize, QMimeData
from PyQt5.QtGui import QIcon, QPainter, QDrag
from PyQt5.QtWidgets import QWidget, QGridLayout, QButtonGroup, QToolButton, QApplication
from PyQt5.QtWidgets import QStyleOption, QStyle

from eddy.core.datatypes import Item
from eddy.core.items import ConceptNode, ComplementNode, DomainRestrictionNode
from eddy.core.items import InputEdge, InclusionEdge, RoleNode, ValueDomainNode
from eddy.core.items import DatatypeRestrictionNode, DisjointUnionNode
from eddy.core.items import PropertyAssertionNode, InstanceOfEdge
from eddy.core.items import IndividualNode, ValueRestrictionNode, AttributeNode
from eddy.core.items import UnionNode, EnumerationNode, IntersectionNode
from eddy.core.items import RangeRestrictionNode, RoleChainNode, RoleInverseNode


class Palette(QWidget):
    """
    This class implements the Graphol palette.
    """
    Padding = 6
    Spacing = 4

    def __init__(self, *args):
        """
        Initialize the Palette.
        """
        super().__init__(*args)
        self.buttonById = {}
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.setExclusive(False)
        self.buttonClicked = self.buttonGroup.buttonClicked
        self.mainLayout = QGridLayout(self)
        self.mainLayout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.mainLayout.setContentsMargins(0, Palette.Padding, 0, Palette.Padding)
        self.mainLayout.setSpacing(Palette.Spacing)
        self.add(ConceptNode, 0, 0)
        self.add(RoleNode, 0, 1)
        self.add(ValueDomainNode, 0, 2)
        self.add(IndividualNode, 1, 0)
        self.add(ValueRestrictionNode, 1, 1)
        self.add(AttributeNode, 1, 2)
        self.add(DomainRestrictionNode, 2, 0)
        self.add(RangeRestrictionNode, 2, 1)
        self.add(IntersectionNode, 2, 2)
        self.add(RoleChainNode, 3, 0)
        self.add(DatatypeRestrictionNode, 3, 1)
        self.add(RoleInverseNode, 3, 2)
        self.add(ComplementNode, 4, 0)
        self.add(EnumerationNode, 4, 1)
        self.add(UnionNode, 4, 2)
        self.add(DisjointUnionNode, 5, 0)
        self.add(PropertyAssertionNode, 5, 1)
        self.add(InclusionEdge, 5, 2)
        self.add(InputEdge, 6, 0)
        self.add(InstanceOfEdge, 6, 1)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(216, 394)

    ####################################################################################################################
    #                                                                                                                  #
    #   DRAWING                                                                                                        #
    #                                                                                                                  #
    ####################################################################################################################

    def paintEvent(self, paintEvent):
        """
        This is needed for the widget to pick the stylesheet.
        :type paintEvent: QPaintEvent
        """
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        style = self.style()
        style.drawPrimitive(QStyle.PE_Widget, option, painter, self)

    ####################################################################################################################
    #                                                                                                                  #
    #   INTERFACE                                                                                                      #
    #                                                                                                                  #
    ####################################################################################################################

    def add(self, item, row, column):
        """
        Add a button to the palette.
        :type item: class
        :type row: int
        :type column: int
        """
        button = PaletteButton(item)
        self.buttonById[item.item] = button
        self.buttonGroup.addButton(button, item.item)
        self.mainLayout.addWidget(button, row, column)

    def button(self, button_id):
        """
        Returns the button matching the given id.
        :type button_id: Item
        :rtype: PaletteButton
        """
        return self.buttonById[button_id]

    def clear(self, *args):
        """
        Clear the palette selection.
        :type args: Item
        """
        for button in self.buttonById.values():
            if button not in args:
                button.setChecked(False)


class PaletteButton(QToolButton):
    """
    This class implements a single palette button.
    """
    def __init__(self, item, parent=None):
        """
        Initialize the palette button.
        :type item: class
        :type parent: QWidget
        """
        super().__init__(parent)
        self.item = item.item
        self.pixmap = item.image(w=60, h=44)
        self.startPos = None
        self.setCheckable(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setIcon(QIcon(self.pixmap))
        self.setIconSize(QSize(60, 44))

    ####################################################################################################################
    #                                                                                                                  #
    #   EVENTS                                                                                                         #
    #                                                                                                                  #
    ####################################################################################################################

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the button..
        :type mouseEvent: QMouseEvent
        """
        if mouseEvent.buttons() & Qt.LeftButton:
            self.startPos = mouseEvent.pos()
        super().mousePressEvent(mouseEvent)

    # noinspection PyArgumentList
    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse if moved while a button is being pressed.
        :type mouseEvent: QMouseEvent
        """
        if mouseEvent.buttons() & Qt.LeftButton:

            # Exclude edges from drag&drop since we need to source and edge to insert it in the diagram.
            if Item.ConceptNode <= self.item <= Item.PropertyAssertionNode:

                distance = (mouseEvent.pos() - self.startPos).manhattanLength()
                if distance >= QApplication.startDragDistance():

                    mimeData = QMimeData()
                    mimeData.setText(str(self.item.value))

                    drag = QDrag(self)
                    drag.setMimeData(mimeData)
                    drag.setPixmap(self.pixmap)
                    drag.setHotSpot(self.startPos - self.rect().topLeft())
                    drag.exec_(Qt.CopyAction)

        super().mouseMoveEvent(mouseEvent)


    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when a mouse button is released.
        :type mouseEvent: QMouseEvent
        """
        super().mouseReleaseEvent(mouseEvent)