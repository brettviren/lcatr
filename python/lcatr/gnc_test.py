#!/usr/bin/env python

import schema  
import cards
import tables
import hdus

result = schema.Result(
    hdus.PrimaryHDU('GainNoiseCold'),
    [hdus.FileRefHDU([__file__])]
)

if __name__ == '__main__':
    print result
