The application renpassG!S stands for (r)enewable (en)ergy (pa)thway (s)imulation (s)ystem capable of working with (GIS) data.
It is based on the original idea of `renpass <http://www.renpass.eu>`_ and closely linked to
the `Open Energy Modelling Framework (oemof) <https://github.com/oemof/oemof>`_.

This documentation is meant to explain the basic functionality and structured as follows:

.. contents::
    :depth: 1
    :local:
    :backlinks: top
.. sectnum::

Overview
=============

renpassG!S is an easy-to-use application designed to model energy systems, which is developed and maintained at
the Center for Sustainable Energy Systems (Zentrum für nachhaltige Energysysteme (ZNES)) in Flensburg.
Making use of the broad functionality of `oemof <https://github.com/oemof/oemof>`_, the application provides easy-to-understand energy system scenarios
for different regions in a CSV format, optimizing the power plant dispatch at minimum cost.
Results are exported into a CSV structure as well an can be easily accessed using spreadsheet software such as LibreOffice Calc or Microsoft Excel.

The general functionality can be derived from the following figure:

.. image:: /documents/model_overview_renpass_gis_en.png
    :alt: renpassG!S model model overview
    :align: center    
    :width: 100%


As there are currently some licensing issues concerning the scenario data, this repository only provides the application code.
If you are interested in using or contributuing to the app, feel free to contact us.

Installation
=============

renpassG!S is build within _oemof and works with the current stable version (v.0.1).
Please follow the current installation guidelines in the `documentation <https://github.com/oemof/oemof#documentation>`_.

Contact
=============

If you have any questions or want to contribute, feel free to contact us!

* Flensburg University of Applied Sciences: <cord.kaldemeyer(at)hs-flensburg.de>

* University of Flensburg: <martin.soethe(at)uni-flensburg.de>
