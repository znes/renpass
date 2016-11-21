Introduction
============

renpassG!S is an easy-to-use application designed to model energy systems, which is developed and maintained at the Center for Sustainable Energy Systems (Zentrum für nachhaltige Energysysteme (ZNES)) in Flensburg. The application is closely linked to the Open-Energy-Modeling-Framework (oemof). renpassG!S, an application of the broad functionality of oemof provides easy-to-understand energy system scenarios for Europe in a CSV format, optimizing the power plant dispatch for minimum cost and exports results of the optimization process.

The documentation is structured as follows:


.. contents::
    :depth: 2
    :local:
    :backlinks: top
.. sectnum::

Scenario Data
=============

Based on the NEP 2014 scenario sources of parameters of other scenarios are only included if parameters have changed.

NEP 2014
---------------

Regions
~~~~~~~

AT, BE, CH, CZ, DE, DK, FR, LU, NL, NO, PL, SE

Fuel prices & CO2 costs
~~~~~~~~~~~~~~~~~~~~~~~

European Countries
~~~~~~~~~~~~~~~~~~

+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|Fuel        |Fuel price €2014/GJ          |Source         |Emission tCO2/GJ  |Source     |Fuel price including CO2 cost €2014/MWh|
+============+=============================+===============+==================+===========+=======================================+
|gas         |8.0866                       |Kohlenstatistik|0.0559            |UBA2015_   | 30.3012                               |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|hard_coal   |2.4908                       |Ibid.          |0.0934            |Ibid.      | 10.9541                               |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|oil         |10.5433                      |Ibid.          |0.0733            |Ibid.      | 39.5156                               |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|waste       |1.86                         |Ibid.          |0.0917            |IPCC2006_  | 8.6470                                |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|biomass     |5.56                         |PROGNOS2013_   |0.0020            |DEFRA2012_ | 20.0586                               |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|lignite     |1.15                         |ISI2011_       |0.1051            |UBA2015_   | 6.3761                                |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|uranium     |1.11                         |Ibid.          |0.0088            |OEKO2007_  | 4.1832                                |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+
|mixed_fuels |1.86                         |nan            |0.0917            |nan        | 8.6470                                |
+------------+-----------------------------+---------------+------------------+-----------+---------------------------------------+

with CO2 price = 5.91 EUR/tCO2 (EEX)
with 3.6 GJ ~ 1 MWh

Manipulations:
- BMU-DLR2012_: Linear interpolated in the timeframe from 2010 to 2015, inflation - adjusted
- mixed fuels same values as waste

Variable costs
~~~~~~~~~~~~~~

+-----------+----------+---------------+
|Type       | €/MWh    |Source         |
+===========+==========+===============+
|gas        | 2.0      | IER2010_      |
+-----------+----------+---------------+
|hard_coal  | 4.0      | Ibid.         |
+-----------+----------+---------------+
|oil        | 1.5      | DIW2013_      |
+-----------+----------+---------------+
|waste      | 23.0     | Energynet2012_|
+-----------+----------+---------------+
|biomass    | 3.9      | Ibid.         |
+-----------+----------+---------------+
|lignite    | 4.4      | IER2010_      |
+-----------+----------+---------------+
|uranium    | 0.5      | Ibid.         |
+-----------+----------+---------------+
|mixed_fuels| 23.0     | nan           |
+-----------+----------+---------------+

Fixed costs
~~~~~~~~~~~

+-----------+----------+---------------+
|Type       | €/MW     | Source        |
+===========+==========+===============+
|gas        | 19,000   | IER2010_      |
+-----------+----------+---------------+
|hard_coal  | 35,000   | Ibid.         |
+-----------+----------+---------------+
|oil        |  6,000   | DIW2013_      |
+-----------+----------+---------------+
|waste      | 16,500   | Energynet2012_|
+-----------+----------+---------------+
|biomass    | 29,000   | Ibid.         |
+-----------+----------+---------------+
|lignite    | 39,000   | IER2010_      |
+-----------+----------+---------------+
|uranium    | 55,000   | Ibid.         |
+-----------+----------+---------------+
|mixed_fuels| 16,500   | nan           |
+-----------+----------+---------------+

Efficiencies
~~~~~~~~~~~~

+-----------+-------+----------------+
|Type       |eta    |Source          |
+===========+=======+================+
|gas        | 42.5  |ENTSOE2014c     |
+-----------+-------+----------------+
|hard_coal  | 38.0  | Ibid.          |
+-----------+-------+----------------+
|oil        | 34.0  | Ibid.          |
+-----------+-------+----------------+
|waste      | 26.0  | Ibid.          |
+-----------+-------+----------------+
|biomass    | 38.0  | Ibid.          |
+-----------+-------+----------------+
|lignite    | 38.0  | Ibid.          |
+-----------+-------+----------------+
|uranium    | 32.5  | Ibid.          |
+-----------+-------+----------------+
|mixed_fuels| 26.0  | Ibid.          |
+-----------+-------+----------------+

- Based on efficiency classes provided by ENTSOE2014c_ average values are assumed
- Mixed fuels same values as waste

Installed capacities
~~~~~~~~~~~~~~~~~~~~

- Source: ENTSOE2014a_
- Description: 19:00pm values, Scenario B (Best estimate) based on the expectations of the TSO, See "Source". Original Data has been provided by ENTSO-E.
- Year: 2014
- Manipulations: None

Availability
~~~~~~~~~~~~

The availability of thermal power plants is 85 %.

- Source: VGB PowerTech. Verfügbarkeit von Wärmekraftwerken 2003-2012,“ Essen, 2013.

Demand
~~~~~~

- Source: http://data.open-power-system-data.org/time_series/2016-03-18/
- Description: See "Source". Original Data has been provided by ENTSO-E.
- Year: 2014
- Manipulations: Normalised by dividing the values of the respective country by their annual maximum.

Transshipment - Net Transfer Capacities (NTC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Source: MARTINEZ-ANIDO2013_, p.149 ff
- Description: See "Source". Original Data has been provided by ENTSO-E (NTC Matrix)
- Year: 2010
- Manipulations: None

Wind Timeseries
~~~~~~~~~~~~~~~

- Source: https://beta.renewables.ninja/downloads
- Description: See "Source" and respective journal articles on the dataset. Original Data has been provided by MERRA.
- Year: 2014
- Manipulations: None

Solar Timeseries
~~~~~~~~~~~~~~~~

- Source: https://beta.renewables.ninja/downloads
- Description: See "Source" and respective journal articles on the dataset. Original Data has been provided by MERRA-2.
- Year: 2014
- Manipulations: None

NEP 2025
--------

Fuel prices & CO2 costs
~~~~~~~~~~~~~~~~~~~~~~~

+----------------+-----------------+-------------------+-----------------------+-----------------------+------------------+-------------------------------------+
|Fuel            | Original        | Fuel price €/GJ   | Source                |Fuel price €/MWh       |Emission tCO2/GJ  |Fuel price including CO2 cost €/MWh  |
+================+=================+===================+=======================+=======================+==================+=====================================+
| hard_coal      | 83.50 €/t SKE   | 2.8490            | NEP2015_, p. 32       | 10.2564               | 0.0934           | 17.3174                             |
+----------------+-----------------+-------------------+-----------------------+-----------------------+------------------+-------------------------------------+
| lignite        | 1.50 €/MWh th   | 0.4167            | NEP2015_, p. 32       | 1.50                  | 0.1051           | 9.4457                              |
+----------------+-----------------+-------------------+-----------------------+-----------------------+------------------+-------------------------------------+
| gas            | 3.19 Cent/kWh   | 8.8610            | NEP2015_, p. 32       | 31.8996               | 0.0559           | 36.1256                             |
+----------------+-----------------+-------------------+-----------------------+-----------------------+------------------+-------------------------------------+
| oil            | 116.00 $/bbl    | 14.89             | NEP2015_, p. 32       | 53.6040               | 0.0733           | 59.1455                             |
+----------------+-----------------+-------------------+-----------------------+-----------------------+------------------+-------------------------------------+
| waste          |                 | 1.86              | IRENA2015_, p.125     | 6.696                 | 0.0917           | 13.6285                             |
+----------------+-----------------+-------------------+-----------------------+-----------------------+------------------+-------------------------------------+
| mixed_fuels    |                 | 1.86              | IRENA2015_, p.125     | 6.696                 | 0.0917           | 13.6285                             |
+----------------+-----------------+-------------------+-----------------------+-----------------------+------------------+-------------------------------------+
| biomass        |                 | 7.58              | PROGNOS2013_, p. 31   | 27.288                | 0.0020           | 27.4392                             |
+----------------+-----------------+-------------------+-----------------------+-----------------------+------------------+-------------------------------------+
| uranium        |                 | 1.11              | ISI2011_, p.94        | 3.996                 | 0.0088           | 4.6613                              |
+----------------+-----------------+-------------------+-----------------------+-----------------------+------------------+-------------------------------------+

with CO2 price = 21.00 €/t  NEP2015_, p. 32

Calculation factors:

+-------+---------------+---------------+-----------+------------+
|1      |GJ             |0.0341208424   |t SKE      |            |
+-------+---------------+---------------+-----------+------------+
|1      |t SKE          |29.3076        |GJ         |            |
+-------+---------------+---------------+-----------+------------+
|1      |EURO_2014      |1.3285         |US $ _ 2014|Bundesbank_ |
+-------+---------------+---------------+-----------+------------+
|1      |Mwh            |3.6            |GJ         |            |
+-------+---------------+---------------+-----------+------------+
|1      |bbl            |5.86152        |GJ         |            |
+-------+---------------+---------------+-----------+------------+

NEP 2035 B2 Scenario
--------------------

Fuel prices & CO2 costs
~~~~~~~~~~~~~~~~~~~~~~~

+----------------+-----------------+-----------------+-----------------------+-----------------------+------------------+-----------------------------------+
|Fuel            |Original         |Fuel price €/GJ  |Source                 |Fuel price €/MWh       |Emission tCO2/GJ  |Fuel price including CO2 cost €/MWh|
+================+=================+=================+=======================+=======================+==================+===================================+
|hard_coal       |84.27 €/t SKE    |2.88             |  NEP2015_, p.32       |10.3680                |0.0934            |20.7914                            |
+----------------+-----------------+-----------------+-----------------------+-----------------------+------------------+-----------------------------------+
|lignite         |1.50 €/MWh th    |0.42             |  NEP2015_, p.32       |1.5120                 |0.1051            |13.2412                            |
+----------------+-----------------+-----------------+-----------------------+-----------------------+------------------+-----------------------------------+
|gas             |3.37 Cent/kWh    |9.36             |  NEP2015_, p.32       |33.6960                |0.0559            |39.9344                            |
+----------------+-----------------+-----------------+-----------------------+-----------------------+------------------+-----------------------------------+
|oil             |128.00 $/bbl     |16.44            |  NEP2015_, p.32       |59.1840                |0.0733            |67.3643                            |
+----------------+-----------------+-----------------+-----------------------+-----------------------+------------------+-----------------------------------+
|waste           |                 |1.86             |  IRENA2015_, p.125    |6.6960                 |0.0917            |16.9297                            |
+----------------+-----------------+-----------------+-----------------------+-----------------------+------------------+-----------------------------------+
|mixed_fuels     |                 |1.86             |  IRENA2015_, p.125    |6.6960                 |0.0917            |16.9297                            |
+----------------+-----------------+-----------------+-----------------------+-----------------------+------------------+-----------------------------------+
|biomass         |                 |7.58             |  PROGNOS2013_, p. 31  |27.2880                |0.0020            |27.5112                            |
+----------------+-----------------+-----------------+-----------------------+-----------------------+------------------+-----------------------------------+
|uranium         |                 |1.11             |  ISI2011_, p.94       |3.9960                 |0.0088            |4.9781                             |
+----------------+-----------------+-----------------+-----------------------+-----------------------+------------------+-----------------------------------+

with CO2 price = 31.00 €/t  NEP2015_, p. 32

Installed capacities
~~~~~~~~~~~~~~~~~~~~

- Source: ENTSOE2014a_
- Description: 19:00pm values, Version 3 based on the EU longterm goals, See "Source". Original Data has been provided by ENTSO-E.
- Year: 2030 values assumed for  2035
- Manipulations: None

Transshipment - Net Transfer Capacities (NTC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Source: ENTSOE2014b_
- Description:
- Year: 2030
- Manipulations: None


..  * "BMWI Energie Daten - Factors, Sheet 0.2 and 0.3":https://www.bmwi.de/BMWi/Redaktion/Binaer/energie-daten-gesamt,property=blob,bereich=bmwi2012,sprache=de,rwb=true.xls
..  * "DIW2013":https://www.diw.de/documents/publikationen/73/diw_01.c.424566.de/diw_datadoc_2013-068.pdf




.. _MARTINEZ-ANIDO2013 : http://ses.jrc.ec.europa.eu/sites/ses.jrc.ec.europa.eu/files/documents/thesis_brancucci_electricity_without_borders.pdf
.. _ISI2011: http://www.isi.fraunhofer.de/isi-wAssets/docs/x/de/publikationen/Final_Report_EU-Long-term-scenarios-2050_FINAL.pdf
.. _UBA2015: https://www.umweltbundesamt.de/themen/klima-energie/treibhausgas-emissionen
.. _IPCC2006: http://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf
.. _DEFRA2012: https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/69554/pb13773-ghg-conversion-factors-2012.pdf
.. _OEKO2007: http://www.oeko.de/oekodoc/318/2007-008-de.pdf
.. _PROGNOS2013: http://www.prognos.com/uploads/tx_atwpubdb/131010_Prognos_Belectric_Studie_Freiflaechen_Solarkraftwerke_02.pdf
.. _ECOFYS2014: http://www.ecofys.com/files/files/ecofys-2014-international-comparison-fossil-power-efficiency.pdf
.. _IER2010: http://www.ier.uni-stuttgart.de/publikationen/arbeitsberichte/downloads/Arbeitsbericht_08.pdf
.. _DIW2013: https://www.diw.de/documents/publikationen/73/diw_01.c.424566.de/diw_datadoc_2013-068.pdf
.. _Energynet2012: https://www.energinet.dk/SiteCollectionDocuments/Danske%20dokumenter/Forskning/Technology_data_for_energy_plants.pdf
.. _BMU-DLR2012: http://www.dlr.de/dlr/Portaldata/1/Resources/bilder/portal/portal_2012_1/leitstudie2011_bf.pdf
.. _NEP2015: http://www.netzentwicklungsplan.de/NEP_2025_1_Entwurf_Kap_1_bis_3.pdf
.. _IRENA2015: http://www.irena.org/DocumentDownloads/Publications/IRENA_REmap_Germany_report_2015.pdf
.. _ENTSOE2014a: https://www.entsoe.eu/Documents/SDC%20documents/SOAF/140602_SOAF%202014_dataset.zip
.. _ENTSOE2014b: https://www.entsoe.eu/major-projects/ten-year-network-development-plan/maps-and-data/Pages/default.aspx
.. _ENTSOE2014c: https://www.entsoe.eu/major-projects/ten-year-network-development-plan/tyndp-2014/Documents/TYNDP2014%20market%20modelling%20data.xlsx
.. _Bundesbank: https://www.bundesbank.de/Redaktion/DE/Downloads/Statistiken/Aussenwirtschaft/Devisen_Euro_Referenzkurs/stat_eurefd.pdf?__blob=publicationFile

