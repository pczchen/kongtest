from setuptools import setup, find_packages
#from distutils.core import setup

setup(
      name='kongtest',
      version='0.0.1',
      description='test kong & api status',
      author='pczchen',
      author_email='chunzhi.chen@pcitc.com',
      url='http://future.com/chunzhi',
      py_modules=['testkong'],
      packages=['httpreq','httpobj','util'],
      package_data={'':['*.*']},
      data_files=[('',['kongdata.txt'])]
    )