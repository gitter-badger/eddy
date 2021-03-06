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


from eddy.core.functions.system import expandPath
from eddy.core.functions.system import homePath
from eddy.core.functions.system import modulePath
from eddy.core.functions.system import openPath
from eddy.core.functions.system import resourcesPath
from eddy.core.functions.system import rootPath

from eddy.core.functions.geometry import angle
from eddy.core.functions.geometry import distanceL
from eddy.core.functions.geometry import distanceP
from eddy.core.functions.geometry import intersection
from eddy.core.functions.geometry import midpoint

from eddy.core.functions.graph import bfs
from eddy.core.functions.graph import dfs
from eddy.core.functions.graph import identify

from eddy.core.functions.misc import clamp
from eddy.core.functions.misc import cutL
from eddy.core.functions.misc import cutR
from eddy.core.functions.misc import first
from eddy.core.functions.misc import isEmpty
from eddy.core.functions.misc import isQuoted
from eddy.core.functions.misc import partition
from eddy.core.functions.misc import rangeF
from eddy.core.functions.misc import shaded
from eddy.core.functions.misc import snap
from eddy.core.functions.misc import snapF
from eddy.core.functions.misc import uncapitalize

from eddy.core.functions.owl import OWLAnnotationText
from eddy.core.functions.owl import OWLText

from eddy.core.functions.signals import connect
from eddy.core.functions.signals import disconnect