#!/usr/bin/env python
'''
LSST CCD Acceptance Testing Result (LCATR)
==========================================

This package provides the following:

 - Base classes for describing and documenting the schema for the FITS
   Header Data Units (HDUs) and their collection in the form of an
   HDUList.

 - Specialized sets of subclasses.  One set is for a shared meta data
   file and one each is for the specific results from each test
   station or analysis.

 - Overriding of some elements of the ``pyfits`` module to provide for
   hooks where validation code is run.  There is default validations
   run in the base classes as well as validations specific to each
   test restult.

 - Reference documentation of the LCATR-specific schema.

 - Access to objects that are available under the plain ``pyfits``
   module.

Each LCATR-specific schema provides a module which bundles the schema
elements.  All LCATR tests must also provide information following the
schema defined by ``lcatr.limsmeta``.  Each schema is available in a
manner like:

  >>> import lcatr
  >>> nhdus = len(lcatr.limsmeta.schema)
  >>> print 'There are %d HDUs defined for the meta data file' % nhuds

The specific schema for each file describes and documents:

 - Required HDUs in a file

 - Required cards in an HDU's header

 - Required columns in an HDU's table unit.

Validation is performed by running an HDU's (or HDUList's)
``validate()`` method.  For example:

  >>> from lcatr.schema import PrimaryHDU
  >>> p = PrimaryHDU()
  >>> p.validate()

A full schema for a file is built as a list (HDUlist) containing first
a primary HDU and zero or more secondary HDU classes.  Instances can
be created empty and later filled and writen to file or previously
generated files can be read in for validation:

  >>> import lcatr.schema as pyfits
  >>> fp = pyfits.open("results.fits")
  >>> fp.validate()

the resulting HDUList returned by ``open()`` will contain instances of
the ``lcatr`` schema HDU classes. A ValueError exception will be
raised on failure.

'''

import base
import common
import limsmeta
import ptc
import util
