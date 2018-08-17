Welcome
=========

To install you need to get the repository and install. Do:

```bash
    git clone https://github.com/znes/renpass_gis.git
    pip install renpass
```

To test, run the example with the commandline tool `renpass.py`:

```bash
    cd renpass/renpass
    python renpass.py examples/investment/datapackage.json
```

Getting help:

```bash
    renpass.py -h
```
Example usage with another solver (standard is [CBC](https://projects.coin-or.org/Cbc)
and with indiviual start and end timestep:

```bash
    renpass.py -o gurobi --t_start 0 --t_end 24 path/to/datapackage.json
```    

Per default, all result files are written back into the sub-folder */results*.


Background
=============

Energy systems modelling requires versatile tools to model systems with
different levels of accuracy and detail resulting in the complexity of the model.
For example, for some countries the lack of data may force energy system
analysts to apply simplistic approaches. In other cases comprehensive interlinked
models may be applied to analyse energy systems and future pathways.

The Open Energy Modelling Framework is based on graph structure at the core.
In addition it provides an optimization model generator to construct individual
and suitable models. The internal logic, used terminology and software
architecture is abstract and rather designed for model developers and
experienced modellers.

Oemof users / developers can model energy systems with different degrees
of freedom:

1. Modelling based using existing classes
2. Add own classes
3. Add own constraints based on the underlying algebraic modelling library

However, in some cases complexity of this internal logic and full functionality
is neither necessary nor suitable for model users. Therefore we provide
so called facade classes that provide an energy specific and reduced access to
the underlying oemof functionality.

Currently we provide the following facades:

* Dispatchable
* Volatile
* Connection
* Conversion
* Storage
* ExtractionTurbine
* BackpressureTurbine
* Reservoir
* Load

Modelling energy systems based on these classes is straightforward.
Parametrization of an energy system can either be done via python scripting or
by using the datapackage structure described below. Datapackages can then easily
be processed with the command line tool.


Datapackage
============
To construct a scenario based on the datapackage

1. Add the topology of the energy system based on the components and their
  **exogenous model parameters**.
2. Create a python script to construct the energy system and the model from
  that data or simply use the existing command line tool.
3. Post-process the data (you may use the `EnergySystem.to_datapackage()`)
   method to store your results in datapackage.
   **NOTE**: This function has not been implemented in oemof yet.

This allows you to simply publish your scenario (input data, assumptions, model
and results) altogether in one consistent block based on the datapackage
standard.


How to create a Datapackage
-----------------------------

We adhere to the frictionless [(tabular) datapackage standard](https://frictionlessdata.io/specs/tabular-data-package/).
On top of that structure we add our own logic. We require at least two things:

1. A directory named *data* containing at least one sub-folder called *elements*
 (optionally it may contain a directory *sequences* and hubs. Of course you may
 add any other directory, data or other information.)
2. A valid meta-data `.json` file for the datapackage

**NOTE**: You **MUST** provide one file with the buses / hubs called `bus.csv`!

The resulting tree of the datapackage could for example look like this:


      |-- datapackage
          |-- data
              |-- elements
                  |-- demand.csv
                  |-- generator.csv
                  |-- storage.csv
                  |-- bus.csv
              |-- sequences
          |-- scripts
          |-- datapackage.json


To simplifiy the process of creating and processing datapackage you may
also use the [(datapackage-utilities)](https://github.com/znes/datapackage-utilities-utitiles).
The datamodel used for creating facades and examples is also based on the datamodel
described there.

Elements
--------

We recommend using one tabular data resource (i.e. one csv-file) for each
type you want to model. The fields (i.e. column names) match the attribute
names specified in the description of the facade classes.

Example for **Demand**:

| name      | type   | amount | profile         | bus             |
|-----------|--------|--------|-----------------|-----------------|
| el-demand | demand | 2000   | demand-profile1 | electricity-bus |
| ...       |  ...   |  ...   |     ...         |     ...         |

Example for **Generator**:

| name  | type      | capacity | capacity_cost   | bus             | marginal_cost |
|-------|-----------|----------|-----------------|-----------------|---------------|
| gen   | generator | null     | 800             | electricity-bus | 75            |
| ...   |     ...   |    ...   |     ...         |     ...         |  ...          |


Sequences
----------
A resource stored under
*/sequences* should at leat contain the field `timeindex` with the following
standard format ISO 8601, i.e. `YYYY-MM-DDTHH:MM:SS`.

Example:

| timeindex        |  demand-profile1 |  demand-profile2 |
|------------------|------------------|------------------|
| 2016-01-01T00:00 |     0.1          |      0.05        |
| 2016-01-01T01:00 |     0.2          |      0.1         |


Scripting
=========================
Currently the only way to construct a model and compute it is by using the `oemof.solph` library. As described above, you can simply use the command line tool on your created datapackage. However, you may also use the `facades.py` module
and write your on application.

Just read the `.json` file to create an `solph.EnergySystem` object from the
datapackage. Based on this you can create the model, compute it and process
the results.


```python
    from oemof.solph import EnergySystem, Model
    from oemof.solph.facades import Demand, Generator

    es = EnergySystem.from_datapackage(
        'datapackage.json',
        attributemap={
            Demand: {"demand-profiles": "profile"}},
        typemap={
            'load': demand,
            'dispatchable': generator,
            'bus': bus})

    m = Model(es)
    m.solve()
```

**Note**: You may use the `attributemap` to map your your field names to facade
class attributes. In addition you may also use different names for types in your
datapackage and map those to the facade classes (use `typemap` attribute for
this)

Write results
--------------


```python
    from oemof.solph import EnergySystem

    # compute the model and write results back to energy system

    ...

    # write the energy system
    es = EnergySystem.to_datapackage('datapackage.json')
```

Debugging
=============

Debugging can sometimes with tricky, here are some things you might want to
consider:

**Components do not end up in the model**
* Does the data resource (i.e. csv-file) for your components exist in the
`datapackage.json` file.
* Did you set the `attributemap` and `typemap` arguments of the
`EnergySystem.from_datapackge()` method of correctly? Make sure all classes
with their types are present.

**Cast errors when reading a datapackage**
* Does the column order match the order of fields in the (tabular) data
resource?
* Does the type match the types in of the columns (i.e. for integer, obviously
  only integer values should be in the respective column)

**oemof related errors**
If you encounter errors from oemof, the objects are not instantiated correctly
which may happen if something of the following is wrong in your metadata file:

* foreign-keys

**pyomo related errors**

If you encounter an error for writing a lp-file, you might want to check if
your foreign-keys are set correctly. In particular for resources with fk's for
sequences. If this is missing, you will get unsupported operation string and
numeric. This will unfortunately only be happen on the pyomo level currently.



Other ressources
================

* Preceding project [renpass](https://github.com/fraukewiese/renpass).

Related publications
====================

Boysen, C., Grotlüschen, H., Großer, H., Kaldemeyer, C., and Tuschy, I. (2017). *Druckluftspeicherkraftwerk Schleswig-Holstein - Untersuchung zur Eignung Schleswig-Holsteins als Modellstandort für die Energiewende*. Nr. 5 der Reihe Forschungsergebnisse des ZNES Flensburg (elektronisch: ISSN 2196-7164 / Print: ISSN 2195-4925)

Mueller, U. P., Wienholt, L., Kleinhans, D., Cussmann, I., Bunke, W.-D., Pleßmann, G. and Wendiggensen, J. (2018) 'The eGo grid model: An open source approach towards a model of German high and extra-high voltage power grids'. *Journal of Physics: Conference Series*, 977(1), article id. 012003, doi: 10.1088/1742-6596/977/1/012003

Becker, L., Bunke, W., Christ, M., Degel, M., Grünert, J., Söthe, M., Wiese, F. and Wingenbach, C. (2016). VerNetzen: *Sozial-ökologische und technisch-ökonomische Modellierung von Entwicklungspfaden der Energiewende.* Nr. 4 der Reihe Forschungsergebnisse des ZNES Flensburg (elektronisch: ISSN 2196-7164)

Berg, M., Bohm, S., Fink, T., Hauser, M., Komendantova, N. and Soukup, O. (2016). 'Scenario development and multi-criteria analysis for Morocco’s future electricity system in 2050. Summary of workshop results.' *Elaboration et évaluation des différents scénarios du mix électrique futur du Maroc*, 23-24 May 2016, Rabat, Morocco.
