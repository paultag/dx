#!/usr/bin/env python
import importlib
from dx.handler import decode
import dx.handlers.ascii

for x in decode(
    [int, ...],
    str,
    [72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100]
):
    print(x)
