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


from abc import abstractmethod, ABCMeta

from PyQt5.QtCore import QObject


class AbstractExporter(QObject):
    """
    Base class for DiagramScene exporters.
    """
    __metaclass__ = ABCMeta

    def __init__(self, scene):
        """
        Initialize the DiagramScene exporter.
        :type scene: DiagramScene
        """
        super().__init__()
        self.scene = scene

    @abstractmethod
    def export(self, *args, **kwargs):
        """
        Export the coverted ontology using the provided syntax.
        :rtype: str
        """
        pass

    ####################################################################################################################
    #                                                                                                                  #
    #   ONTOLOGY GENERATION                                                                                            #
    #                                                                                                                  #
    ####################################################################################################################

    @abstractmethod
    def run(self):
        """
        Perform DiagramScene export.
        """
        pass