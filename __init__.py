# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Super_Copier
                                 A QGIS plugin
 Copie des objets avec possibilité de personnaliser les champs
                             -------------------
        begin                : 2015-09-21
        copyright            : (C) 2015 by HUET Sylvain
        email                : sylvain.huet@sdis81.fr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Super_Copier class from file Super_Copier.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Super_Copier import Super_Copier
    return Super_Copier(iface)
