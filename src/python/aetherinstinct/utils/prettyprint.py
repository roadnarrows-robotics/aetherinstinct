"""
Pretty print routines.

\LegalBegin
  MIT
\LegalEnd
"""

import sys
from io import (StringIO)

##-
def print2cols(obj, indent=0, c1width='auto', sep=':', spacing=1,
                      **print_kwargs):
  """
  Print lines in two columns.

  Parameters:
    obj           An iterable object proviiding tuples of length 2+ per
                  iteration cycle (e.g. dict.items(), [(v1, v2),...]).
    indent        Line left indentation.
    c1width       Column one width. If 'auto', then it is determined by the 
                  widest name in lines.
    sep           Separator succeeding end of column 1 values.
    spacing       Spacing between column one separator and column two.
    print_kwargs  Any python3 print() keyword arguments.
  """
  if c1width == 'auto':
    c1width = 1
    for u,v in obj:
      if len(u) > c1width:
        c1width = len(u)
    c1width += len(sep)
  for u,v in obj:
    u += sep
    print(f"{'':<{indent}}{u:<{c1width}}{'':<{spacing}}{v}", **print_kwargs)

##-
def print_to_str(fn, *fn_args, **fn_kwargs):
  """
  Capture print output from a print function to a string.

  Parameters:
    fn          Print function.
    fn_args     Positional arguments to print function.
    fn_kwargs   Keyword arguments to print function.

  Returns:
    Captured output as a string. Newlines may be included in string.
  """
  lines = ''
  with StringIO() as output:
    filearg = fn_kwargs.get('file', sys.stdout)
    fn_kwargs['file'] = output
    fn(*fn_args, **fn_kwargs)
    lines = output.getvalue()
    fn_kwargs['file'] = filearg
  if lines[-1] == '\n':
    lines = lines[:-1]
  return lines
