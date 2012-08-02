Designing and Defining Summary Result Files
===========================================

Each test result produces files of three types:

1. A common *metadata* file 
2. One or more summary *result* files
3. Any auxiliary files

The first two are in well defined formats following a well defined
organization (schema).  The *metadata* file schema is identical for
all tests.  The *result* file(s) follow a schema that is uniquely
defined for each test.

FITS File Format and How It Relates
-----------------------------------

The underling format for the *metadata* and *results* files is FITS.
These files can be made by any means but must pass the validations
defined by this package.  Files that are valid by construction can be
most easily created by using the code in this package to produce them.
Where that is not practical, conversion/summation programs that
utilize this package should be used.

FITS files are commonly used to store bitmapped image data.  No such
data is expected to be stored directly in the database so neither
*metadata* nor *result* files will contain any.  Auxiliary files are
free to contain such data be they in FITS or other formats.

Instead, FITS notion of "cards" (key/value pairs) and "tables"
(ntuples) are used to store test meta data and results.  These data
types map directly to database constructs.

Designing Test Schema
---------------------

Each test metadata and summary result must follow well schema.  Every
test operator or analyzer must provide details on how their data is
"shaped" (this is what the schema is).  This section gives guidance on
how to design a fitting schema.  

Data types
^^^^^^^^^^

Types can be specified as integer, floating point or string.  Details
on size (16 vs. 32 bit integers, single/double precision floats,
maximum string lengths) may also be needed.  In addition, is a single
value needed?  A fixed array?  A variable array? A more complex
structure?


Unit of Application
^^^^^^^^^^^^^^^^^^^

The part to which a result applies must be specified.  For example,
does a quantity apply to the CCD as a whole or some sub-part
(amplifier, pixel region).  The answer strongly influences how the
schema is to be defined.  


Putting it Together
^^^^^^^^^^^^^^^^^^^

There are three levels of schema that must be specified:

HDUs in a file:

    A file is made of a (standardized) Primary Header Data Unit (HDU)
    and one or more result-specific secondary HDUS.  An HDU consists
    of a header and a table unit.  

Cards in a header:

    Cards are key/value pairs.  Each valid HDU header must provide a
    small number of FITS-standard cards and FITS uses some cards to
    book-keep the table unit (if existing) but the schema designer is
    otherwise free to add any number of additional cards that may be
    needed for each (secondary) HDU.

Columns in a table:

    In addition to or instead of result-specific cards, a secondary
    HDU may contain a table.  A table is formed of named columns each
    of a specific type.  In principle, columns may be unrelated, but
    in order to match database constructs a row is treated as many
    quantities of one aspect.  That is, every table must be rectangular.

What data goes where
^^^^^^^^^^^^^^^^^^^^

How should any given information be organized?

Single quantities that apply to an entire CCD should be stored as a
card.  Related, but low multiplicity quantities can also be handled by
defining a naming convention that includes some enumeration.  For
example, ``LinRangeMin`` and ``LinRangeMax`` cards are used to store
the minimum and maximum ADU where the CCD is still meets the linear
range specification.

If the multiplicity of per-CCD information grows above some convenient
level (say, 3 items) or if it is unknown a'priori then a table can be
specified.  If the multiplicity is fixed then each row can implicitly
hold measurements of each element.  For example, per-amplifier
measurements always produce an ordered list of 16 quantities.  A table
that has N columns, one for each type of measured quantity and 16
ordered rows, one for each amplifier, is well matched.

If the multiplicity is not fixed or is not a simple linear enumeration
then (at least) one column must be dedicated to storing some
identifier of the enumeration.  For example, the cold spot analysis
finds zero or more regions of low response from each of the 16
amplifiers of a CCD.  Each spot is characterized by N quantities.  The
table has then N+1 columns where an extra column is added to store the
amplifier to which the per-spot quantities apply.  The number of rows
is not fixed.


Determining Number Of HDUs
^^^^^^^^^^^^^^^^^^^^^^^^^^

Besides the standardized Primary HDU, the number of secondary HDUs
depends on the type and "shape" of the result data.  It may also
depend on what common HDUs are pre-defined and can be reused.

If tables are needed, each table of a unique shape needs to be in a
separate HDU.  Additionally, separate HDUs can be employed to hold
conceptually distinct information, even if technically the information
could be stored in a single HDU.


Specifying Schema
-----------------

Details for specifying a schema are in the ``lcatr`` reference
documentation.  An overview of the specification is given here:

Cards:

    Cards are specified by their name and a comment.  Each HDU
    specifies a list of required cards in addition to the small number
    of cards required by all HDUs.

Columns:

    Columns are specified by their name, data type and a comment.
    Each HDU that contains a table specifies a list of required
    columns.

HDUs:

    Every file-level schema is specified by an ordered list of HDUs.
    Each HDU is specified by a Python class from the ``lcatr`` package.


