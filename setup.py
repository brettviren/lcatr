from distutils.core import setup

setup(name = 'lcatr',
      version = '0.0',
      description = 'LSST CCD Acceptance Testing Results',
      long_description = 'Produce and validate files for LSST CCD Acceptance Testing Results',
      author = 'Brett Viren',
      author_email = 'bv@bnl.gov',
      url = 'http://www.phy.bnl.gov/~bviren/lsst/lcatr/',
      packages = ['lcatr','lcatr.schema'],
      package_dir = {'':'python'},
      requires = ['pyfits','numpy']
      )

