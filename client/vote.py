#!/usr/bin/env python3

from Crypto.Util.number import bytes_to_long
from sage.all import *

msg = b'VOTE FOR PEDRO'
x = var('x')
f = x**3 - bytes_to_long(msg)
print(solve_mod(f, 256**15))
