# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Super_Copier
                                 A QGIS plugin
 Copie des objets avec possibilité de personnaliser les champs
                              -------------------
        begin                : 2015-09-21
        git sha              : $Format:%H$
        copyright            : (C) 2015 by HUET Sylvain
        email                : sylvain.huet@sdis81.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4 import QtGui
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
import qgis.utils
# Initialize Qt resources from file resources.py
import resources
#MsgBox :
# Message QGIS
from qgis.gui import QgsMessageBar
from qgis.core import QgsVectorDataProvider, QgsFeature
# Import the code for the dialog
from Super_Copier_dialog import Super_CopierDialog
from Super_Copier_dialog2 import Super_CopierDialog2
import os.path


class Super_Copier:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Super_Copier_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = Super_CopierDialog()
        self.dlg_2 = Super_CopierDialog2()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Super_Copier')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Super_Copier')
        self.toolbar.setObjectName(u'Super_Copier')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Super_Copier', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Super_Copier/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Super_Copier'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Super_Copier'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def msgBarre(self, type, message):
        """ Gestion de la barre des messages
        Appel : self.msgBarre([num du type de message],"[num du message]![texte optionnel]") -> self.msgBarre(0,"0!text")"""
        msgBar = self.iface.messageBar()
        #choix du type
        cxType = {0 : QgsMessageBar.INFO,
                    1 : QgsMessageBar.WARNING,
                    2 : QgsMessageBar.CRITICAL}
        # Evite l'erreur du split
        if len(message) < 3 : message = str(message) + "|a_b"
        #choix du message
        cxMsg = {0 : "Super_Copier : Aucune couche active",
                    1 : u"Super_Copier : Aucun objet sélectionné",
                    2 : "Super_Copier : Erreur de type, la couche d'origine est de type " + message.split("|")[1].split("_")[0] + " et la couche de destination de type " + message.split("|")[1].split("_")[1] + "!",
                    3 : "Super_Copier : " + message.split("|")[1],
                    4 : u"Super_Copier : traitement terminé!"}
        msg = msgBar.createMessage( cxMsg[int(message.split("|")[0])] )
        msgBar.pushWidget( msg, cxType[type], 5 )
        
    def addFieldChoice(self, label, liste, position):
        #add label
        lbl = QtGui.QLabel(label)
        self.dlg_2.gridLayout.addWidget(lbl, position + 2, 0)
        #add comboBox
        cmbox = QtGui.QComboBox()
        if liste[0] != '': liste.insert(0, '')
        cmbox.addItems(liste)
        self.dlg_2.gridLayout.addWidget(cmbox, position + 2, 1)
        #search equality between lbl and cmbox
        if label in ",".join(liste).lower().split(","):
            if label.upper() in liste:
                cmbox.setCurrentIndex(cmbox.findText(label.upper()))
            else:
                cmbox.setCurrentIndex(cmbox.findText(label))
        #add lineEdit
        linedt = QtGui.QLineEdit()
        self.dlg_2.gridLayout.addWidget(linedt, position + 2, 2)
    
    def delFieldChoice(self):
        """Reset form"""
        layout = self.dlg_2.gridLayout
        for i in reversed(range(3, layout.count())):
            layout.itemAt(i).widget().setParent(None)
        
    def prepaData(self, fields):
        """Prepare data for copy"""
        layout = self.dlg_2.gridLayout
        data = []
        sel = 3
        for field in fields:
            data.append(field)
            if len(layout.itemAt(sel + 2).widget().text()) > 1:
                data.append(layout.itemAt(sel + 2).widget().text())
            elif len(layout.itemAt(sel + 1).widget().currentText()) > 1:
                data.append("fld|" + layout.itemAt(sel + 1).widget().currentText())
            else:
                data.append("null")
            sel += 3
        return data
        
    def finalCopy(self, l_orig, l_dest, data):
        """Eléments sélectionnés"""
        selection = l_orig.selectedFeatures()
        """Itération par entité"""
        if l_orig.selectedFeatureCount() < 1: self.msgBarre(2, "1")
        type1 = {0:"point",1:"ligne",2:"polygone",3:"inconnu", 4:u"aucune géométrie"}
        type2 = {0:"inconnu",1:"point",2:"ligne",3:"polygone",4:"point",5:"ligne",6:"polygone",7:u"aucune géométrie"}
        for feature in selection :
            if type1[feature.geometry().type()] == type2[l_dest.wkbType()]:
                """Création des entités"""
                caps = l_dest.dataProvider().capabilities()
                if caps & QgsVectorDataProvider.AddFeatures:
                    feat = QgsFeature(l_dest.pendingFields())
                    for x in range(0, len(data), 2) :
                        if data[x + 1][:3] == "fld":
                            feat.setAttribute(data[x], feature[data[x + 1].split("|")[1]])
                        elif data[x + 1] == "null":
                            pass
                        else:
                            feat.setAttribute(data[x], data[x + 1])
                    feat.setGeometry(feature.geometry())
                    l_dest.startEditing()
                    l_dest.addFeatures([feat], True)
            else:
                self.msgBarre(2, "2|" + type1[feature.geometry().type()] + "_" + type2[l_dest.wkbType()])
                break
        
    def run(self):
        """Run method that performs all the real work"""
        layer_orig = self.iface.activeLayer()
        #Write Active layer in LineEdit
        self.dlg.Active_Layer.clear()
        if str(type(layer_orig)) == "<type 'NoneType'>" :
            aLayer = 'Aucun calque actif'
        else :
            aLayer = layer_orig.name()
        self.dlg.Active_Layer.setText(aLayer)
        #Write visible layers in comboBox
        layers = self.iface.mapCanvas().layers()
        layer_list = []
        self.dlg.LayerChoice.clear()
        num_layer = 0
        for layer in layers:
            layer_list.append(str(num_layer) + "_" + layer.name())
            num_layer += 1
        self.dlg.LayerChoice.addItems(layer_list)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result and self.dlg.Active_Layer.text() != 'Aucun calque actif':
            #Destination layer
            layer_dest = self.iface.mapCanvas().layers()[int(self.dlg.LayerChoice.currentText().split("_")[0])]
            #ajout éléments au formulaire
            x = 0
            ldest_fields = [field.name() for field in layer_dest.pendingFields()]
            lorig_fields = [field.name() for field in layer_orig.pendingFields()]
            for feature in ldest_fields:
                self.addFieldChoice(feature, lorig_fields, x)
                x += 1
            if x < 50:
                for i in range(80 -x): self.dlg_2.gridLayout.addWidget(QtGui.QLabel(''), i + x + 2, 0)
            #Open the second window
            self.dlg_2.show()
            # Run the dialog2 event loop
            result2 = self.dlg_2.exec_()
            if result2:
                self.finalCopy(layer_orig, layer_dest, self.prepaData(ldest_fields))
                self.delFieldChoice()
                if self.dlg.AutoRec.isChecked():
                    layer_dest.commitChanges()
                self.msgBarre(0, "4")
            else:
                self.delFieldChoice()
        else:
            if self.dlg.Active_Layer.text() == 'Aucun calque actif':
                self.msgBarre(2, "0")
