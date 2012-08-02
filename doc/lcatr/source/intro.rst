Intro to LCATR
==============

The LSST CCDs undergo acceptance testing at BNL.  This testing is of
the form of a variety of measurements at test stations and offline
analyses of these measurements (collectively "tests").  The collection
of test data and its analysis are carefully controlled and documented.
The test results are collected in the form of a variety of files.
These are archived in an organized filesystem.  Some specially
formatted summary result files are parsed into a database for
subsequent query.  

The LSST CCD Acceptance Testing Results (LCATR) package assists in
producing and validating these specially formatted files that are to
be parsed into the database.  The rest of this documentation describes
how to design, define, produce, validate and document the schema
and its compliant files for these summary result files.


