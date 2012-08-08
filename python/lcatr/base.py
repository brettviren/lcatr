#!/usr/bin/env python
'''
Modify pyfits to support LCATR schema.
======================================

This module modifies the ``pyfits`` module and provides a set of base
HDU classes that supports the LCATR schema.  

Importing
---------

The ``lcatr.base`` module (or just ``lcatr`` which imports ``base``)
must be imported before any ``pyfits`` objects are used:

  >>> import lcatr
  >>> import pyfits

It imports all of ``pyfits`` so strictly speaking one does not need to
``import pyfits`` explicitly as one can reference all ``pyfits`` object via the
``base`` module.  Or one can get familiar looking code via:

  >>> import lcatr.base as pyfits

Defining Schema
---------------

To define specific schema for an HDU one must:

1) inherit from one of the ``lcatr.base.*HDU`` classes,

2) define any cards and/or columns the schema requires

3) implement any specific validation code.

Beyond what cards a specific schema requires, every HDU must contain
two standard FITS cards which are used to persist information about
what schema the HDU follows.  They are:

``EXTNAME``
    
    The canonical, case insensitive name of the schema which is taken
    as the name of the implementing class.  This is set automatically
    by the base classes.

``EXTVER``

    The version of the schema that the data follows.  This default to
    0 (zero).  Each change to the schema must include an increment of
    this number and code that can read older files into the newer
    schema.

'''

import pyfits
import numpy
import util


# Some quantities and methods shared by all HDU classes.

#: All HDUs must supply these cards.  In addition each specific HDU
#: class may set a class variable ``required_cards`` to a similar list
#: in order to specify additional cards.
required_cards = [
    ('EXTNAME','FITS name of the HDU'),
    ('EXTVER' ,'Version of the HDU'),
    ]


class BaseHDU(object):
    '''
    Base HDU class.
    
    This is a mixin class that adds LCATR-specific methods to all HDU
    classes.  It is multiply-inherited along with a ``pyfits`` HDU
    class in order to replace the ``pyfits`` version.  Only these HDU
    classes are supported:

    * ``PrimaryHDU``
    * ``TableHDU``
    * ``BinTableHDU``
    '''

    #: Specific HDU sub classes should set this to the list of cards required.  These are cards beyond and listed in the same manner as the standard ones listed above in ``base.required_cards``.
    required_cards = None

    def required_card_desc(self):
        '''
        Return the list of required card descriptions built from the
        common set ``base.required_card`` and the ones specific to the
        subclasses ``.required_cards`` list.  This is used internally.
        '''
        mycards = self.required_cards or list()
        return required_cards + mycards

    def initialize_cards(self, **kwds):
        '''
        This method should be called by the HDU class constructor.

        Keyword arguments are interpreted as names of required cards
        (lower cased and with '-' replaced by '_') and are used to
        provided card values.  After construction cards may be set in the
        usual ``pyfits`` manner:

          >>> import datetime, time
          >>> from lcatr.base import PrimaryHDU
          >>> now = datetime.datetime(*time.gmtime()[:6])
          >>> hdu = PrimaryHDU(testname='TheTestName', date_obs=now)
          >>> hdu.header['extver'] = 1 # set schema version after construction

        ``EXTNAME`` is the implementing class name
        ``EXTVER`` will default to 0
        '''

        schema_name = self.__class__.__name__
        schema_ver = kwds.get('version',0)

        self.update_ext_name(schema_name)
        self.update_ext_version(schema_ver)

        for name, comment in self.required_card_desc():
            if not self.header.has_key(name):
                self.header.update(name, '', comment)
                pass
            key = util.keywordify(name)
            val = kwds.get(key)
            if val is None: continue
            val = util.wash_card_value(val)
            self.header[name] = val
            continue
        return

    def validate(self):
        '''
        Basic validation of an HDU.

        This will run pyfits verify() method and then check for required
        cards.

        ValueError is raise if validation fails.
        '''
        try:
            self.verify("exception")
        except VerifyError,msg:
            #msg = 'HDU "%s/%s": verify failed: %s' % (self.schema_name, self.name, msg)
            msg = 'HDU "%s/%s": verify failed: %s' % (self.__class__.__name__, self.name, msg)
            raise ValueError,msg

        for name, comment in self.required_card_desc():
            value = self.header.get(name)
            if value is None:
                raise ValueError, '%s: required card: "%s" not set' % \
                    (self.__class__.__name__,name)
            if value == '':
                raise ValueError, '%s: required card: "%s" is empty string' % \
                    (self.__class__.__name__,name)
            continue
        return

    def update_self(self, doppel = None):
        '''
        If doppel is given, steal its header
        '''
        if not doppel: return
        self.header = doppel.header
        return

    pass

class PrimaryHDU(pyfits.PrimaryHDU, BaseHDU):
    '''
    Extension to pyfits.PrimaryHDU.
    
    The intial arguments to the constructor are the same as
    ``pyfits.PrimaryHDU``.

      >>> hdu = PrimaryHDU(testname = 'TheTestName')
      >>> hdu.header['extver'] = 0 # the schema version

    see the ``BaseHDU.initialize_cards`` method for details.
    '''

    def __init__(self, data=None, header=None, do_not_scale_image_data=False, uint=False, **kwds):
        super(PrimaryHDU,self).__init__(data,header,do_not_scale_image_data,uint)
        self.initialize_cards(**kwds)
        return

    pass


class TableBaseHDU(BaseHDU):
    '''
    Base class for all Table HDUs.

Each subclass should define a ``.required_columns`` class data member which holds a li
    '''
    
    #: The list of descriptions of required columns in the form of a list of (name,type) doubles:
    #:  >>> required_columns = [('Col1Name','I'),...]
    required_columns = None

    # Internal, intialize the table base class.  Called by constructor.
    def initialize_table_base(self,**kwds):
        self.initialize_cards(**kwds)
        self.initialize_columns(**kwds)
        self.update_self()
        return

    def initialize_columns(self, **kwds):
        '''
        Intialized the required columns.  

        This method is called by the constructor and any kwds that
        match column names (first made lower case and ``-`` replaced by
        ``_``) will have their values treated as a column array.
        Otherwise the column will be created empty.
        '''
        if not self.required_columns: return
        cols = []
        for count,(name,typestr,comment) in enumerate(self.required_columns):
            kwname = name.lower().replace('-','_')
            array = kwds.get(kwname,list())
            #col = pyfits.Column(name=name, format=typestr, array=array, start=count+1)
            # fitsverify complains about "TBCOLn is not allowed in the Binary table."
            # if start= is specified.
            col = pyfits.Column(name=name, format=typestr, array=array)
            cols.append(col)
            continue
        self.columns = pyfits.ColDefs(cols)
        return

            

    def validate(self):
        '''
        Validate a table HDU.

        This adds to basic validity checking by requiring the table data to exist.
        '''
        super(TableBaseHDU,self).validate()
        if not len(self.data):
            raise ValueError,'TableHDU "%s": no table data' % self.name
        return

    def get_column(self, column):
        '''
        Return column by name or (1-based) index.

        ValueError is raised if column not found.
        '''
        if isinstance(column,int):
            index = column - 1
        else:
            index = [c.name.lower() for c in self.columns].index(column.lower())
            pass

        try:
            col = self.columns[index]
        except IndexError:
            raise ValueError, 'TableHDU "%s": no column %s at index %s' % (column, index+1)
        return col

    def update_self(self, doppel = None):
        '''
        Update self.

        To stay consistent this must be called any time a column's array
        is modified directly.

        If another HDU is given its contents will be used instead of self's.
        '''
        # pyfits doesn't have a way to say "update my data" so we make a
        # temporary new table HDU and steal its guts as our own.
        if not doppel:
            doppel = new_table(self.columns, self.header)
        self.header = doppel.header
        self.columns = doppel.columns
        self.data = doppel.data
        return

    def set_column_array(self, column, array):
        '''
        Set a column's array.  
        
        The column is specified either by its index (1-based) or name.
        
        The array can be either a list or a numpy.array.
        
        ValueError is raised if column is not found.
        
        This triggers an ``update_self()``.
        '''
        col = self.get_column(column)
        if isinstance(array,list):
            array = numpy.array(array)
            pass
        col.array = array
        self.update_self()
        return

    def append_column_array(self, column, entry):
        '''
        Append entry to given column
        
        The column is specified either by its index (1-based) or name.
        
        This triggers an ``update_self()``.
        '''
        col = self.get_column(column)
        numpy.append(col.array, entry)
        self.update_self()
        return

    pass                        # TableBaseHDU

# note: need to do cut-and-paste programming here to retain the pyfits
# table HDU class dichotomy

class TableHDU(pyfits.TableHDU, TableBaseHDU):
    '''
    Extension to pyfits.TableHDU.

    Named arguments are passed to ``pyfits.TableHDU``.  Additional
    keyword arguments are treated as initial values for either
    required cards or columns.

    This is an ASCII table and probably you want to use
    ``BinTableHDU``.  See ``TableBaseHDU`` for more details.
    '''
    def __init__(self, data=None, header=None, name=None, **kwds):
        super(TableHDU,self).__init__(data,header,name)
        self.initialize_table_base(**kwds)
        return
    pass

class BinTableHDU(pyfits.BinTableHDU, TableBaseHDU):
    '''
    Extension to pyfits.BinTableHDU.

    Named arguments are passed to ``pyfits.BinTableHDU``.  Additional
    keyword arguments are treated as initial values for either
    required cards or columns.

    See ``TableBaseHDU`` for more details.
    '''
    def __init__(self, data=None, header=None, name=None, **kwds):
        super(BinTableHDU,self).__init__(data,header,name)
        self.initialize_table_base(**kwds)
        return
    pass


pyfitsPrimaryHDU  = pyfits.PrimaryHDU
pyfitsTableHDU    = pyfits.TableHDU
pyfitsBinTableHDU = pyfits.BinTableHDU

pyfits.PrimaryHDU  = PrimaryHDU
pyfits.TableHDU    = TableHDU
pyfits.BinTableHDU = BinTableHDU



# This is just a simple bolt-on
def HDUList_validate(self):
    '''
    Validate a list of HDUs.  

    This method is bolted on to ``pyfits.HDUList``.
    '''
    self.verify()
    for hdu in self:
        hdu.validate()
    return
pyfits.HDUList.validate = HDUList_validate


def hdu_pyfits2lcatr(hdu):
    '''
    Return an ``lcatr`` version of the plain pyfits HDU.
    '''
    import lcatr
    module = type(lcatr)

    schema_name = hdu.header['EXTNAME']

    for thing in dir(lcatr):
        mod = lcatr.__dict__[thing]
        if not isinstance(mod,module): 
            continue

        try:
            schema = mod.schema
        except AttributeError:
            continue
        for klass in schema:
            if schema_name.lower() != klass.__name__.lower():
                continue

            # got a hit
            new = klass()
            new.update_self(hdu)
            return new
        continue
    raise ValueError, 'No known class for HDU "%s"' % schema_name


pyfitsopen = pyfits.open
def lcatr_open(*args, **kwds):
    '''
    An LCATR-specific file reader.

    This will return lcatr versions of the HDU classes.

    After loading this module, this method is available as the
    familiar ``pyfits.open()``.
    '''

    hl = pyfitsopen(*args,**kwds)
    return pyfits.HDUList([hdu_pyfits2lcatr(hdu) for hdu in hl])
pyfits.open = lcatr_open
    

# import all of pyfits so users need not include pyfits 
from pyfits import *
