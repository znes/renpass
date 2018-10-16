from setuptools import find_packages, setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='renpass',
      version='0.3.1',
      author='Simon Hilpert, Cord Kaldemeyer, Martin Söthe, Stephan Günther',
      author_email='simon.hilpert@uni-flensburg.de',
      description='renpass',
      url='https://github.com/znes/renpass',
      long_description=read('README.md'),
      scripts=['bin/renpass'],
      packages=find_packages(),
      package_data={'oemof': [
          os.path.join('tools', 'default_files', '*.ini')]},
      install_requires=['oemof >= git+https://github.com/oemof/oemof/releases/tag/v0.2.2#egg=oemof',
                        'dill',
                        'datapackage',
                        'docopt'])
