#!/usr/bin/env python

import schema  
import cards

result = schema.Result(
    schema.HDU(
        schema.Header([
                cards.ExtnameCard('GainNoiseCold'),
                cards.SchemaVersionCard(0),
                ]),
        None
        ),
    list()
)

if __name__ == '__main__':
    print result
