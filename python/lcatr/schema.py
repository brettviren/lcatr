#!/usr/bin/env python
'''
Describe the schema for LSST CCD Acceptance Testing Result files.


See the schema.org document for details. 

 - /result/ :: \to (/PrimaryHDU/, /FragmentHDU/, ...)
 - /PrimaryHDU/ :: \to /HDU/
 - /FragmentHDU/ :: \to /HDU/
 - /HDU/ :: \to (/header/, /payload/)
 - /payload/ :: \to either a /table/ or /data/
 - /header/ :: \to (/card/, /card/, ...)
 - /table/ :: \to (/column/, /column/, ...)
 - /data/ :: \to (t.b.d.)
 - /card/ :: \to (/name/, /typeobj/, /comment/, /description/)
 - /column/ :: \to (/name/, /typeobj/, /description/)
 - /name/ :: \to a string, 8 characters or less
 - /typeobj/ :: \to an instance of a Python class representing the type of the element
 - /comment/ :: \to a short FITS comment
 - /description/ :: \to a free form, comprehensive description of the element

'''

import numpy
import hashlib
import pyfits

class Base(object): 
    '''
    Base for schema classes.  
    '''

    def validate(self):
        '''
        Validate the contents of the object.
        '''
        not_implemented()
        return

    def fits(self):
        '''
        Return the pyfits object corresponding to self.
        '''
        return None

    def __str__(self):
        return 'NotImplemented'

    pass

class Result(Base):
    def __init__(self, primary_hdu, fragment_hdu_list):
        self.hdu = [primary_hdu] + fragment_hdu_list
        return
    def __str__(self):
        ret = ['Result: %d HDUS:'%len(self.hdu)] + [str(hdu) for hdu in self.hdu]
        return '\n'.join(ret)
    pass

class HDU(Base):
    def __init__(self, header, payload = None):
        self.header = header
        if payload is None: payload = list()
        self.payload = payload
        return

    def __str__(self):
        ret = ['[0x%x] HDU (%s): ' % (id(self), self.name())]
        ret += [str(self.header)]
        ret += [str(p) for p in self.payload]
        return '\n'.join(ret)

    def name(self):
        '''
        Return the canonical name for this HDU
        '''
        return self.header.name()
        
    def validate(self):
        self.header.validate()
        if self.payload: self.payload.validate()
        return

    pass

class Header(Base):
    required_cards = ['EXTNAME','CHECKSUM','DATASUM','SCHEMAV']

    def __init__(self, cards = None):
        if cards is None: cards = list()
        self.cards = cards
        return

    def __str__(self):
        ret = ['[0x%x] Header: %d cards:' % (id(self),len(self.cards))] 
        ret += [str(c) for c in self.cards]
        return '\n'.join(ret)

    def validate(self):
        cnames = []
        for c in self.cards:
            c.validate()
            cnames.append(c)

        for needed in Header.required_cards:
            if needed not in cnames:
                raise ValueError, 'Lack required card "%s"' % needed
            continue
        return

    def card(self, cardname):
        for c in self.cards:
            if c.name == cardname:
                return c
            continue
        return None

    def name(self):
        'Return name (EXTNAME) of this header'
        nc = self.card('EXTNAME')
        if not nc: return None
        return nc.value

    pass

class Table(Base):
    def __init__(self, columns = None):
        self.set(columns)
        return

    def __str__(self):
        ret = ['[0x%x] Table (%s):' % (id(self),len(self.columns))]
        ret += [str(c) for c in self.columns]
        return '\n'.join(ret)

    def set(self, columns):
        if columns is None: columns = list()
        self.columns = columns
        return

    def validate(self):
        if not self.columns:
            raise ValueError, 'Table: no columns'
        for c in self.columns:
            c.validate()
        return

    pass

class Data(Base):
    def __init__(self):
        return
    pass

class TypeObj():
    '''
    A type.
    '''

    tofits = {
        'int16':'I',
        'int32':'J',
        'int64':'K',
        'sha1':'A64',
        'str':'A64',
        'datetime': 'A86',
        }

    def __init__(self, typestr):
        self.typestr = typestr
        return

    def __str__(self):
        return self.typestr

    def fits(self):
        return TypeObj.tofits(self.typestr)

    def pytype(self):
        if 'sha1' == self.typestr:
            return type(hashlib.sha1())
        if 'str' == self.typestr:
            return str
        return numpy.typeDict.get(self.typestr)


    def istype(self,obj):
        t = self.pytype()
        if not t: return None
        return isinstance(obj,t)
        
    def strval(self, obj):
        if not self.istype(obj): 
            raise TypeError, '%s not of type %s, it is %s' % (str(obj),str(self),type(obj))
        if self.typestr == 'sha1':
            return obj.hexdigest()
        if self.typestr == 'datetime':
            return obj.strftime("%Y-%m-%dT%H:%M:%S")
        return str(obj)
    pass

class Card(Base):
    def __init__(self, name, typestr, comment, description, value = None):
        self.name = name
        self.typeobj = TypeObj(typestr)
        self.comment = comment
        self.description = description
        self.set(value)
        return

    def set(self, value):
        self.value = value
        return

    def __str__(self):
        ret = '[0x%x] Card: %s (%s): %s' % (id(self), self.name, self.typeobj, self.description)
        if not self.value is None: ret += ' = "%s"' % self.typeobj.strval(self.value)
        return ret

    def validate(self):
        if not all((self.name,self.typeobj,self.comment,self.description, self.value)):
            raise ValueError, 'Card not fully formed.'
        if not self.typeobj.istype(self.value):
            raise TypeError, 'type "%s" not compatible with "%s"' % \
                (str(self.typeobj),str(self))
        return


    pass

class Column(Base):
    def __init__(self, name, typeobj, description, array = None):
        self.name = name
        self.typeobj = TypeObj(typeobj)
        self.description = description
        self.set(array)
        return

    def __str__(self):
        ret = '[0x%x] Column: %s %s: %s' % (id(self),self.name, self.typeobj, self.description)
        if self.array: 
            sar = [self.typeobj.strval(a) for a in self.array]
            ret += ' = %s' % sar
        return ret

    def set(self, array):
        self.array = array
        return

    def fits(self):
        'Return a FITS pyfits.Column'
        return pyfits.Column(name = self.name, format = self.typeobj.fits(), array = self.aray)
    
    def validate(self):
        if not all((self.name,self.typeobj,self.description,self.array)):
            raise ValueError, 'Column not fully formed.'
        if not all([self.typeobj.istype(a) for a in self.array]):
            raise ValueError, 'Column "%s" not of type "%s"' % \
                (self.name, self.typeobj)
        return

    pass


