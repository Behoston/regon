# REGON - parser

This library does only one thing: it parses REGON.

It works for old REGON (7 digits) with or without leading zeros, as well as for long REGON (14 digits). 
Ofcourse standard REGON (9 digits) also will be parsed and validated.


## Usage

```python
from regon.regon import parse

parse('123456785')
parse('12345678512347')
```