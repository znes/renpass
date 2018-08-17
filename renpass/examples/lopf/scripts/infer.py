from datapackage import Package

p = Package()
p.infer('data/**/*.csv')

p.save('datapackage.json')
