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


from PyQt5.QtCore import pyqtSlot, QSortFilterProxyModel, Qt
from PyQt5.QtGui import QPainter, QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QWidget, QTreeView, QVBoxLayout, QHeaderView
from PyQt5.QtWidgets import QStyleOption, QStyle

from eddy.core.datatypes import Item, Identity
from eddy.core.functions import connect, disconnect, first

from eddy.ui.fields import StringField


class Explorer(QWidget):
    """
    This class implements the diagram predicate node explorer.
    """
    def __init__(self, mainwindow):
        """
        Initialize the Explorer.
        :type mainwindow: MainWindow
        """
        super().__init__(mainwindow)
        self.expanded = {}
        self.searched = {}
        self.scrolled = {}
        self.mainview = None
        self.iconA = QIcon(':/icons/treeview-icon-attribute')
        self.iconC = QIcon(':/icons/treeview-icon-concept')
        self.iconD = QIcon(':/icons/treeview-icon-datarange')
        self.iconI = QIcon(':/icons/treeview-icon-instance')
        self.iconR = QIcon(':/icons/treeview-icon-role')
        self.iconV = QIcon(':/icons/treeview-icon-value')
        self.search = StringField(self)
        self.search.setAcceptDrops(False)
        self.search.setClearButtonEnabled(True)
        self.search.setPlaceholderText('Search...')
        self.search.setFixedHeight(30)
        self.model = QStandardItemModel(self)
        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setDynamicSortFilter(False)
        self.proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy.setSortCaseSensitivity(Qt.CaseSensitive)
        self.proxy.setSourceModel(self.model)
        self.view = ExplorerView(mainwindow, self)
        self.view.setModel(self.proxy)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.search)
        self.mainLayout.addWidget(self.view)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(216)
        self.setMinimumHeight(160)

        connect(self.view.doubleClicked, self.itemDoubleClicked)
        connect(self.view.pressed, self.itemPressed)
        connect(self.view.collapsed, self.itemCollapsed)
        connect(self.view.expanded, self.itemExpanded)
        connect(self.search.textChanged, self.filterItem)

    ####################################################################################################################
    #                                                                                                                  #
    #   EVENTS                                                                                                         #
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
    #   SLOTS                                                                                                          #
    #                                                                                                                  #
    ####################################################################################################################
    
    @pyqtSlot('QGraphicsItem')
    def add(self, item):
        """
        Add a node in the tree view.
        :type item: AbstractItem
        """
        if item.node and item.predicate:
            parent = self.parentFor(item)
            if not parent:
                parent = ParentItem(item)
                parent.setIcon(self.iconFor(item))
                self.model.appendRow(parent)
                self.proxy.sort(0, Qt.AscendingOrder)
            child = ChildItem(item)
            child.setData(item)
            parent.appendRow(child)
            self.proxy.sort(0, Qt.AscendingOrder)

    @pyqtSlot(str)
    def filterItem(self, key):
        """
        Executed when the search box is filled with data.
        :type key: str
        """
        if self.mainview:
            self.proxy.setFilterFixedString(key)
            self.proxy.sort(Qt.AscendingOrder)
            self.searched[self.mainview] = key

    @pyqtSlot('QModelIndex')
    def itemCollapsed(self, index):
        """
        Executed when an item in the tree view is collapsed.
        :type index: QModelIndex
        """
        if self.mainview:
            if self.mainview in self.expanded:
                item = self.model.itemFromIndex(self.proxy.mapToSource(index))
                expanded = self.expanded[self.mainview]
                expanded.remove(item.text())

    @pyqtSlot('QModelIndex')
    def itemDoubleClicked(self, index):
        """
        Executed when an item in the tree view is double clicked.
        :type index: QModelIndex
        """
        item = self.model.itemFromIndex(self.proxy.mapToSource(index))
        node = item.data()
        if node:
            self.selectNode(node)
            self.focusNode(node)

    @pyqtSlot('QModelIndex')
    def itemExpanded(self, index):
        """
        Executed when an item in the tree view is expanded.
        :type index: QModelIndex
        """
        if self.mainview:
            item = self.model.itemFromIndex(self.proxy.mapToSource(index))
            if self.mainview not in self.expanded:
                self.expanded[self.mainview] = set()
            expanded = self.expanded[self.mainview]
            expanded.add(item.text())

    @pyqtSlot('QModelIndex')
    def itemPressed(self, index):
        """
        Executed when an item in the tree view is clicked.
        :type index: QModelIndex
        """
        item = self.model.itemFromIndex(self.proxy.mapToSource(index))
        node = item.data()
        if node:
            self.selectNode(node)

    @pyqtSlot('QGraphicsItem')
    def remove(self, item):
        """
        Remove a node from the tree view.
        :type item: AbstractItem
        """
        if item.node and item.predicate:
            parent = self.parentFor(item)
            if parent:
                child = self.childFor(parent, item)
                if child:
                    parent.removeRow(child.index().row())
                if not parent.rowCount():
                    self.model.removeRow(parent.index().row())

    ####################################################################################################################
    #                                                                                                                  #
    #   AUXILIARY METHODS                                                                                              #
    #                                                                                                                  #
    ####################################################################################################################

    @staticmethod
    def childFor(parent, node):
        """
        Search the item representing this node among parent children.
        :type parent: QStandardItem
        :type node: AbstractNode
        """
        key = ChildItem.key(node)
        for i in range(parent.rowCount()):
            child = parent.child(i)
            if child.text() == key:
                return child
        return None

    def parentFor(self, node):
        """
        Search the parent element of the given node.
        :type node: AbstractNode
        :rtype: QStandardItem
        """
        key = ParentItem.key(node)
        for i in self.model.findItems(key, Qt.MatchExactly):
            n = i.child(0).data()
            if node.item is n.item:
                return i
        return None

    ####################################################################################################################
    #                                                                                                                  #
    #   INTERFACE                                                                                                      #
    #                                                                                                                  #
    ####################################################################################################################

    def browse(self, view):
        """
        Set the widget to inspect the given view.
        :type view: MainView
        """
        self.reset()
        self.mainview = view

        if self.mainview:

            scene = self.mainview.scene()
            connect(scene.index.sgnItemAdded, self.add)
            connect(scene.index.sgnItemRemoved, self.remove)

            for item in scene.index.nodes():
                self.add(item)

            if self.mainview in self.expanded:
                expanded = self.expanded[self.mainview]
                for i in range(self.model.rowCount()):
                    item = self.model.item(i)
                    index = self.proxy.mapFromSource(self.model.indexFromItem(item))
                    self.view.setExpanded(index, item.text() in expanded)

            key = ''
            if self.mainview in self.searched:
                key = self.searched[self.mainview]
            self.search.setText(key)

            if self.mainview in self.scrolled:
                rect = self.rect()
                item = first(self.model.findItems(self.scrolled[self.mainview]))
                for i in range(self.model.rowCount()):
                    self.view.scrollTo(self.proxy.mapFromSource(self.model.indexFromItem(self.model.item(i))))
                    index = self.proxy.mapToSource(self.view.indexAt(rect.topLeft()))
                    if self.model.itemFromIndex(index) is item:
                        break

    def reset(self):
        """
        Clear the widget from inspecting the current view.
        """
        if self.mainview:

            rect = self.rect()
            item = self.model.itemFromIndex(self.proxy.mapToSource(self.view.indexAt(rect.topLeft())))
            if item:
                node = item.data()
                key = ParentItem.key(node) if node else item.text()
                self.scrolled[self.mainview] = key
            else:
                self.scrolled.pop(self.mainview, None)

            try:
                scene = self.mainview.scene()
                disconnect(scene.index.sgnItemAdded, self.add)
                disconnect(scene.index.sgnItemRemoved, self.remove)
            except RuntimeError:
                pass
            finally:
                self.mainview = None

        self.model.clear()

    def flush(self, view):
        """
        Flush the cache of the given mainview.
        :type view: MainView
        """
        self.expanded.pop(view, None)
        self.searched.pop(view, None)
        self.scrolled.pop(view, None)

    def iconFor(self, node):
        """
        Returns the icon for the given node.
        :type node:
        """
        if node.item is Item.AttributeNode:
            return self.iconA
        if node.item is Item.ConceptNode:
            return self.iconC
        if node.item is Item.ValueDomainNode:
            return self.iconD
        if node.item is Item.ValueRestrictionNode:
            return self.iconD
        if node.item is Item.IndividualNode:
            if node.identity is Identity.Instance:
                return self.iconI
            if node.identity is Identity.Value:
                return self.iconV
        if node.item is Item.RoleNode:
            return self.iconR

    def focusNode(self, node):
        """
        Focus the given node in the main view.
        :type node: AbstractNode
        """
        if self.mainview:
            self.mainview.centerOn(node)

    def selectNode(self, node):
        """
        Select the given node in the main view.
        :type node: AbstractNode
        """
        if self.mainview:
            scene = self.mainview.scene()
            scene.clearSelection()
            node.setSelected(True)


class ExplorerView(QTreeView):
    """
    This class implements the explorer tree view.
    """
    def __init__(self, mainwindow, parent=None):
        """
        Initialize the explorer view.
        :type mainwindow: MainWindow
        :type parent: QWidget
        """
        super().__init__(parent)
        self.setAnimated(True)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setEditTriggers(QTreeView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHeaderHidden(True)
        self.setHorizontalScrollMode(QTreeView.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setSelectionMode(QTreeView.SingleSelection)
        self.setSortingEnabled(True)
        self.setWordWrap(True)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(False)
        self.mainwindow = mainwindow

    ####################################################################################################################
    #                                                                                                                  #
    #   EVENTS                                                                                                         #
    #                                                                                                                  #
    ####################################################################################################################

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the tree view
        :type mouseEvent: QMouseEvent
        """
        self.clearSelection()
        # We call super after clearing the selection so that we click off an
        # item it will be deselected by clearSelection here above and the default
        # mousePressEvent will not emit the clicked signal that will select the item.
        super().mousePressEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the tree view
        :type mouseEvent: QMouseEvent
        """
        if mouseEvent.button() == Qt.RightButton:
            index = first(self.selectedIndexes())
            if index:
                model = self.model().sourceModel()
                index = self.model().mapToSource(index)
                item = model.itemFromIndex(index)
                node = item.data()
                if node:
                    menu = self.mainwindow.menuFactory.create(self.mainwindow, node.scene(), node)
                    menu.exec_(mouseEvent.screenPos().toPoint())
        super().mouseReleaseEvent(mouseEvent)


class ParentItem(QStandardItem):
    """
    This class implements the single predicate section of the treeview.
    """
    def __init__(self, node):
        """
        Initialize the predicate section.
        :type node: AbstractNode
        """
        super().__init__(ParentItem.key(node))
        self.setFlags(self.flags() & ~Qt.ItemIsEditable)

    @classmethod
    def key(cls, node):
        """
        Returns the key used to index the given node.
        :type node: AbstractNode
        :rtype: str
        """
        return node.text().replace('\n', '')


class ChildItem(QStandardItem):
    """
    This class implements the single node of the treeview.
    """
    def __init__(self, node):
        """
        Initialize the node item.
        :type node: AbstractNode
        """
        super().__init__(ChildItem.key(node))

    @classmethod
    def key(cls, node):
        """
        Returns the key used to index the given node.
        :type node: AbstractNode
        :rtype: str
        """
        return '{} ({})'.format(node.text().replace('\n', ''), node.id)