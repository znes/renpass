from datapackage_utilities import building

building.infer_metadata(package_name='renpass-foreignkeys-examples',
                        foreign_keys={
                            'bus': ['component'],
                            'profile': ['component'],
                            'from_to_bus': [],
                            'chp': []
                            }
                        )
