Welcome
=========

To get the repository got to your terminal an do:

```bash
    git clone https://github.com/znes/renpass_gis.git
```

To test, run the example with the commandline tool `renpass.py`:

```bash
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

* Generator
* Demand
* Storage
* Reservoir
* Connection
* Conversion
* Bus
* Backpressure
* ExtractionTurbine

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


How to create an Datapackage
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
    es = EnergySystem.to_datapackage('datapackage.json')
