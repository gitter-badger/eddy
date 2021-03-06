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


from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QIcon
from PyQt5.QtWidgets import QDialog, QProgressBar, QVBoxLayout


class BusyProgressDialog(QDialog):
    """
    This class implements a dialog showing a busy progress bar.
    """
    def __init__(self, title='', parent=None):
        """
        Initialize the form dialog.
        :type title: str
        :type parent: QWidget
        """
        super().__init__(parent)
        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignHCenter)
        self.progressBar.setRange(0, 0)
        self.progressBar.setFixedSize(300, 30)
        self.progressBar.setTextVisible(True)
        self.progressBar.setFormat(title or 'Busy ...')
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.progressBar)
        self.setWindowIcon(QIcon(':/images/eddy'))
        self.setWindowTitle(title or 'Busy ...')
        self.setFixedSize(self.sizeHint())

    ####################################################################################################################
    #                                                                                                                  #
    #   CONTEXT MANAGER                                                                                                #
    #                                                                                                                  #
    ####################################################################################################################

    def __enter__(self):
        """
        Draw the dialog.
        """
        self.show()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the dialog.
        """
        self.close()
