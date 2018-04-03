
Introduction
=============

Energy systems modelling requires versatile tools to model systems with
different degree of accuarcy, detail and thus resulting model complexiy.
For example for some countries the lack of data may force energy system
analysts to apply simplistic approaches.

The framework provides a core based on the graph description and a strong
optimization model generator to construct individual and suitable models.
Internally oemof uses abstract terms and own definitions based on an
generic data model.

However, in some cases complexity of this internal logic and full functionality
is neither necessary nor suitable for some model users. Therefore we provide
facade classes that are provide an energy specific and reduced access to the
underlying oemof functionality.

Currentlly we provide the following facades:

* Generator
* Demand
* Storage
* Connection
* Conversion
* Hub
* Bus
* CHP

Modelling energy systems based on these classes is straighfoward. Parametrization
of an energy system can either be done via python scripting or by using the
datapackage structure described below.


Datapackage
============
To construct a scenario based on the datapackage

1. Add the topology of the energy system based on the components and their
  **exogenous model parameters**.
2. Create a python script to construct the energy system and the model from
  that data.
3. Posprocess the data (you may use the `EnergySystem.to_datapackage()`)
   method to store your results in datapackage.

This allows you to simply publish your scenario (input data, assumptions, model
and results) altogether in own consitent set.


How to create an Datapackage
-----------------------------

We adhere to the frictionless [(tabular) datapackage standard](https://frictionlessdata.io/specs/tabular-data-package/).
On top of that structure we add our own logic. We require at least two things:

1. A directory named *data* containting at least one subfolder called *elements*
 (optionally it may contain a directory *sequences* and hubs. Of course you may
 add any other directory, data or other information.)
2. A valid meta-data `.json` file for the datapackage

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


Elements
--------

We recommend using one tabular data resource (i.e. one csv-file) for each
type you want to model. The fields (i.e. columnnames) match the attribute
names specified in the description of the facade classes.

Example for **Demand**:

| name      | type   | amount | profile         | bus             |
|-----------|--------|--------|-----------------|-----------------|
| el-demand | demand | 2000   | demand-profile1 | electricity-bus |
| ...       |  ...   |  ...   |     ...         |     ...         |

Example for **Generator**:

| name  | type      | capacity | investment_cost | bus             | marginal_cost |
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
| 2016-01-01:00:00 |     0.1          |      0.05        |
| 2016-01-01:01:00 |     0.2          |      0.1         |


Create model and compute
-------------------------
Currently the only way to construct a model and compute it is by using the
solph library.

Just read the `.json` file to creat an `solph.EnergySystem` object from the
datapackage. Based on this you can create the model, compute it and process
the results.

.. code-block:: python

    from oemof.solph import EnergySystem, Model
    from oemof.solph.facades import Demand, Generator

    es = EnergySystem.from_datapackage(
        'datapackage.json',
        attributemap={
            Demand: {"demand-profiles": "profile"}},
        typemap={
            'demand': Demand,
            'generator': Generator,
            'bus': Bus})

    m = Model(es)
    m.solve()


**Note**: You may use the `attributemap` to map your your field names to facade
class attributes. In addition you may also use different names for types in your
datapackage and map those to the facade classes (use `typemap` attribute for
this)

Write results
--------------
.. code-block:: python

    from oemof.solph import EnergySystem

    # compute the model and write results back to energy system

    ...

    # write the energy system
    es = EnergySystem.to_datapackage(
        'datapackage.json')
