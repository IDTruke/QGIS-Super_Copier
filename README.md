QGIS-Super\_Copier ![icone](icon.png "Super\_Copier")
=================
QGIS Plugin to choose the fields when copying geometries.
The selection of source and destination layers can bring the common fields.
Otherwise there is the possibility of a link between two fields or to impose a value.

Installation from github
-------------------------------

    cd .qgis2/python/plugins/
    git clone https://github.com/IDTruke/QGIS-Super_Copier

Using the plugin
---------------------

* Ensure the plugin is enabled in the Extension menu
* Select the layer with the objects to duplicate
* Go to Vector -> Super\_Copier -> Super\_Copier
* Select the destination layer in the first dialogue box

![Dialog1](img/dialog1.jpg)

* Check the option 'Auto save' if you want the changes to be applied directly from
* Validate
* Check the connection between each field in the second dialog box

![Dialog2](img/dialog2.jpg)

* If you want to force a value, fill the fields 'Forced value'
