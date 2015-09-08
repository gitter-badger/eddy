# -*- coding: utf-8 -*-

##########################################################################
#                                                                        #
#  pyGraphol: a python design tool for the Graphol language.             #
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
##########################################################################
#                                                                        #
#  Graphol is developed by members of the DASI-lab group of the          #
#  Dipartimento di Informatica e Sistemistica "A.Ruberti" at Sapienza    #
#  University of Rome: http://www.dis.uniroma1.it/~graphol/:             #
#                                                                        #
#     - Domenico Lembo <lembo@dis.uniroma1.it>                           #
#     - Marco Console <console@dis.uniroma1.it>                          #
#     - Valerio Santarelli <santarelli@dis.uniroma1.it>                  #
#     - Domenico Fabio Savo <savo@dis.uniroma1.it>                       #
#                                                                        #
##########################################################################


from copy import deepcopy
from pygraphol.datatypes import RestrictionType
from pygraphol.functions import isEmpty
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QUndoCommand


class CommandNodeAdd(QUndoCommand):
    """
    This command is used to add nodes to the graphic scene.
    """
    def __init__(self, scene, node):
        """
        Initialize the command.
        :param scene: the graphic scene where this command is being performed.
        :param node: the node being added.
        """
        super().__init__('add %s node' % node.name)
        self.scene = scene
        self.node = node

    def redo(self):
        """redo the command"""
        self.scene.itemList.append(self.node)
        self.scene.addItem(self.node.shape)

    def undo(self):
        """undo the command"""
        self.scene.itemList.remove(self.node)
        self.scene.removeItem(self.node.shape)


class CommandNodeSetZValue(QUndoCommand):
    """
    This command is used to change the Z value of the graphic scene nodes.
    """
    def __init__(self, scene, node, zValue):
        """
        Initialize the command.
        :param scene: the graphic scene where this command is being performed.
        :param node: the node whose zValue is changing.
        :param zValue: the new zValue.
        """
        super().__init__('change %s node Z value' % node.name)
        self.scene = scene
        self.node = node
        self.old = node.shape.zValue()
        self.new = zValue

    def redo(self):
        """redo the command"""
        self.node.shape.setZValue(self.new)

    def undo(self):
        """undo the command"""
        self.node.shape.setZValue(self.old)


class CommandNodeRezize(QUndoCommand):
    """
    This command is used to resize nodes.
    """
    def __init__(self, node):
        """
        Initialize the command
        :param node: the node whose resizing operation we want to Undo.
        """
        super().__init__('resize %s node' % node.name)
        self.node = node
        self.old = deepcopy(node.shape.rect()) if hasattr(node.shape, 'rect') else QPolygonF(node.shape.polygon())
        self.new = None

    def redo(self):
        """redo the command"""
        if self.new:
            try:
                self.node.shape.setRect(self.new)
            except AttributeError:
                self.node.shape.setPolygon(self.new)
            self.node.shape.updateHandlesPos()
            self.node.shape.updateLabelPos()
            self.node.shape.updateEdges()
            self.node.shape.update()

    def undo(self):
        """undo the command"""
        try:
            self.node.shape.setRect(self.old)
        except AttributeError:
            self.node.shape.setPolygon(self.old)
        self.node.shape.updateHandlesPos()
        self.node.shape.updateLabelPos()
        self.node.shape.updateEdges()
        self.node.shape.update()


class CommandNodeMove(QUndoCommand):
    """
    This command is used to move nodes (1 or more).
    """
    def __init__(self, old, new):
        """
        Initialize the command
        :param old: a dictionary containing shapes old position data.
        :param new: a dictionary containing shapes new position data.
        """
        self.old = old
        self.new = new

        if len(old['nodes']) != 1:
            params = 'move %s nodes' % len(old['nodes'])
        else:
            params = 'move %s node' % next(iter(old['nodes'].keys())).node.name

        super().__init__(params)

    def redo(self):
        """redo the command"""
        # update edges breakpoints
        for edge, breakpoints in self.new['edges'].items():
            for i in range(len(breakpoints)):
                edge.breakpoints[i] = breakpoints[i]
        # update nodes positions
        for shape, pos in self.new['nodes'].items():
            shape.setPos(pos)
            shape.updateEdges()

    def undo(self):
        """undo the command"""
        # update edges breakpoints
        for edge, breakpoints in self.old['edges'].items():
            for i in range(len(breakpoints)):
                edge.breakpoints[i] = breakpoints[i]
        # update nodes positions
        for shape, pos in self.old['nodes'].items():
            shape.setPos(pos)
            shape.updateEdges()


class CommandNodeLabelMove(QUndoCommand):
    """
    This command is used to move nodes labels.
    """
    def __init__(self, node, moved):
        """
        Initialize the command
        :param node: the node whose label is being moved.
        :param moved: whether the label was moved already or not
        """
        super().__init__('move %s node label' % node.name)
        self.moved = moved
        self.node = node
        self.old = node.shape.label.pos()
        self.new = None

    def redo(self):
        """redo the command"""
        if self.new:
            self.node.shape.label.setPos(self.new)
            self.node.shape.label.moved = not self.moved

    def undo(self):
        """undo the command"""
        self.node.shape.label.setPos(self.old)
        self.node.shape.label.moved = self.moved


class CommandNodeLabelEdit(QUndoCommand):
    """
    This command is used to edit nodes labels.
    """
    def __init__(self, node):
        """
        Initialize the command
        :param node: the node whose label is being moved.
        """
        super().__init__('edit %s node label' % node.name)
        self.node = node
        self.old = node.shape.labelText()
        self.new = None

    def redo(self):
        """redo the command"""
        if self.new:
            text = self.node.shape.label.defaultText if isEmpty(self.new) else self.new
            self.node.shape.setLabelText(text)

    def undo(self):
        """undo the command"""
        text = self.node.shape.label.defaultText if isEmpty(self.old) else self.old
        self.node.shape.setLabelText(text)


class CommandNodeValueDomainSelectDatatype(QUndoCommand):
    """
    This command is used to change the datatype of a value-domain node.
    """
    def __init__(self, node, datatype):
        """
        Initialize the command
        :param node: the node whose datatype is being changed.
        :param datatype: the new datatype.
        """
        super().__init__('change %s datatype' % node.name)
        self.node = node
        self.old = node.datatype
        self.new = datatype

    def redo(self):
        """redo the command"""
        self.node.datatype = self.new
        self.node.shape.label.setText(self.node.datatype.value)
        self.node.shape.updateShape()
        self.node.shape.updateEdges()

    def undo(self):
        """undo the command"""
        self.node.datatype = self.old
        self.node.shape.label.setText(self.node.datatype.value)
        self.node.shape.updateShape()
        self.node.shape.updateEdges()


class CommandNodeHexagonSwitchTo(QUndoCommand):
    """
    This command is used to change the class of hexagon based constructor nodes.
    """
    def __init__(self, scene, old, new):
        """
        Initialize the command
        :param scene: the scene where this command is being executed.
        :param old: the node being replaced.
        :param new: the replacement node.
        """
        super().__init__('switch %s to %s' % (old.name, new.name))
        self.scene = scene
        self.old = old
        self.new = new

    def redo(self):
        """redo the command"""
        for edge in self.old.edges:
            if edge.source == self.old:
                edge.source = self.new
            else:
                edge.target = self.new
            self.new.addEdge(edge)

        self.scene.itemList.append(self.new)
        self.scene.addItem(self.new.shape)
        self.scene.itemList.remove(self.old)
        self.scene.removeItem(self.old.shape)

    def undo(self):
        """undo the command"""
        for edge in self.new.edges:
            if edge.source == self.new:
                edge.source = self.old
            else:
                edge.target = self.old
            self.old.addEdge(edge)
        self.scene.itemList.append(self.old)
        self.scene.addItem(self.old.shape)
        self.scene.itemList.remove(self.new)
        self.scene.removeItem(self.new.shape)


class CommandNodeSquareChangeRestriction(QUndoCommand):
    """
    This command is used to change the restriction of square based constructor nodes.
    """
    def __init__(self, node, restriction, cardinality=None):
        """
        Initialize the command
        :param node: the node whose restriction is being changed.
        :param restriction: the new restriction type.
        """
        self.node = node
        self.old_restriction = self.node.restriction
        self.old_cardinality = self.node.cardinality
        self.new_restriction = restriction
        self.new_cardinality = dict(min=None, max=None) if not cardinality else cardinality

        label = restriction.label
        if restriction is RestrictionType.cardinality:
            label = label % (self.s(cardinality['min']), self.s(cardinality['max']))

        super().__init__('change %s restriction to %s' % (node.name, label))

    @staticmethod
    def s(x):
        """
        Return a valid string representation for the cardinality value.
        :param x: the value to represent.
        """
        return str(x) if x is not None else '-'

    def redo(self):
        """redo the command"""
        if self.new_restriction is RestrictionType.cardinality:
            self.node.restriction = self.new_restriction
            self.node.cardinality = self.new_cardinality
            self.node.shape.label.setText(self.node.restriction.label % (self.s(self.node.cardinality['min']),
                                                                         self.s(self.node.cardinality['max'])))
        else:
            self.node.restriction = self.new_restriction
            self.node.cardinality = dict(min=None, max=None)
            self.node.shape.label.setText(self.node.restriction.label)

    def undo(self):
        """undo the command"""
        if self.old_restriction is RestrictionType.cardinality:
            self.node.restriction = self.old_restriction
            self.node.cardinality = self.old_cardinality
            self.node.shape.label.setText(self.node.restriction.label % (self.s(self.node.cardinality['min']),
                                                                         self.s(self.node.cardinality['max'])))
        else:
            self.node.restriction = self.old_restriction
            self.node.cardinality = dict(min=None, max=None)
            self.node.shape.label.setText(self.node.restriction.label)