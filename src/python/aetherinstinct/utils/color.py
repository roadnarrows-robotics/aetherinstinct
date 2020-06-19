"""
ANSI colors classes.

AI Author: Robin Knight

\LegalBegin
Copyright 2019-2020 Aether Instinct LLC. All Rights Reserved

Licensed under the MIT License (the "License").

You may not use this file except in compliance with the License. You may
obtain a copy of the License at:

  https://opensource.org/licenses/MIT

The software is provided "AS IS", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. in no event shall the
authors or copyright holders be liable for any claim, damages or other
liability, whether in an action of contract, tort or otherwise, arising from,
out of or in connection with the software or the use or other dealings in the
software.
\LegalEnd
"""

import os
import sys
from pprint import pprint

# -----------------------------------------------------------------------------
# Class TermColors
# -----------------------------------------------------------------------------
class TermColors(dict):
  """
  Gives easy access to ANSI color codes. Falls back to no color for certain
  TERM values.

  For now, only 16 foreground colors are supported.
  """

  # pre and post color sequences
  ANSI_COLOR_PRE    = '\033['
  ANSI_COLOR_POST   = 'm'
  SCREEN_COLOR_PRE  = '\001'
  SCREEN_COLOR_POST = '\002'

  # color code components
  CODE_SEP            = ';'
  CODE_NORM_INTENSITY = '0'
  CODE_BOLD_INTENSITY = '1'
  CODE_FG_PRE         = '3'
  CODE_BG_PRE         = '4'
  CODE_COLOR_BLACK    = '0'
  CODE_COLOR_RED      = '1'
  CODE_COLOR_GREEN    = '2'
  CODE_COLOR_YELLOW   = '3'
  CODE_COLOR_BLUE     = '4'
  CODE_COLOR_MAGENTA  = '5'
  CODE_COLOR_CYAN     = '6'
  CODE_COLOR_WHITE    = '7'

  # foreground color templates (name, code)
  COLOR_TEMPLATES = (
        ('black'       , '0;30'),
        ('red'         , '0;31'),
        ('green'       , '0;32'),
        ('brown'       , '0;33'),
        ('blue'        , '0;34'),
        ('purple'      , '0;35'),
        ('cyan'        , '0;36'),
        ('lightgray'   , '0;37'),
        ('darkgray'    , '1;30'),
        ('lightred'    , '1;31'),
        ('lightgreen'  , '1;32'),
        ('yellow'      , '1;33'),
        ('lightblue'   , '1;34'),
        ('lightpurple' , '1;35'),
        ('lightcyan'   , '1;36'),
        ('white'       , '1;37'),
        ('normal'      , '0'),
  )

  NO_COLOR = ''

  def __init__(self):
    """ Initializer. """
    self._bu          = {}
    self._color_avail = False
    self._coloring    = False

    self.termcolors()
    self.default_synonyms()

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return "TermColors"

  def termcolors(self):
    """ Fixe color escape sequences based on terminal type. """
    term = os.environ.get('TERM')
    if term in ('linux', 'screen', 'screen-256color',
                'screen-bce', 'screen.xterm-256color'):
      self._pre  = TermColors.SCREEN_COLOR_PRE + TermColors.ANSI_COLOR_PRE
      self._post = TermColors.ANSI_COLOR_POST + TermColors.SCREEN_COLOR_POST
      fmt = self._pre + "{}" + self._post
      self.update(dict([(k, fmt.format(v)) for k,v in self.COLOR_TEMPLATES]))
      self._color_avail = True
      self._coloring = True
    elif term in ('xterm', 'xterm-color', 'xterm-256color'):
      self._pre  = TermColors.ANSI_COLOR_PRE
      self._post = TermColors.ANSI_COLOR_POST
      fmt = self._pre + "{}" + self._post
      self.update(dict([(k, fmt.format(v)) for k,v in self.COLOR_TEMPLATES]))
      self._color_avail = True
      self._coloring = True
    else:
      self._pre  = ''
      self._post = ''
      self.update(dict([(k, NO_COLOR) for k,v in self.COLOR_TEMPLATES]))
      self._color_avail = False
      self._coloring = False

  def default_synonyms(self):
    """ Set default color synonms. """
    self.synonym('darkgray',    'debug') 
    self.synonym('green',       'info') 
    self.synonym('brown',       'warning')
    self.synonym('lightred',    'error')
    self.synonym('lightpurple', 'critical')
    self.synonym('lightpurple', 'fatal')

  def enable_color(self):
    """ Enable color output if available. """
    if self._color_avail and not self._coloring:
      self.update(self._bu)
      self._bu.clear()
      self._coloring = True

  def disable_color(self):
    """ Disable color output. """
    if self._coloring:
      self._bu.update(self)
      for k in list(self):
        self[k] = TermColors.NO_COLOR
      self._coloring = False

  def is_color_available(self):
    """ Returns True if terminal supports color, False otherwise. """
    return self._color_avail

  def is_coloring(self):
    """ Returns True if color output enabled, False otherwise. """
    return self._coloring

  def synonym(self, color, syn):
    """
    Set a color synonym.

    Parameters:
      color   Color name.
      syn     New synonym.
    """
    self[syn] = self[color]

  def color_names(self):
    """ Return list of terminal supported color names. """
    return [t[0] for t in COLOR_TEMPLATES]

  def make_esc_seq(self, *codes):
    if self.is_color_available():
      return self._pre + TermColors.CODE_SEP.join(codes) + self._post
    else:
      return ''

  def plen(self, s):
    """
    Calculate the print length of text string sans terminal escape sequences.

    Parameters:
      s     Text string.

    Return:
      Print length of text.
    """
    rawlen  = len(s)

    if not self.is_color_available():
      return rawlen

    prelen  = len(self._pre)
    postlen = len(self._post)
    txtlen  = rawlen

    start = 0
    while start < rawlen:
      i = s.find(self._pre, start)
      if i == -1:
        break;
      dlen = prelen + self._codelen(s[i+prelen:]) + postlen
      txtlen -= dlen
      if txtlen <= 0:
        txtlen = 0
        break
      start = i + dlen

    return txtlen

  def _codelen(self, s):
    """
    Calculate the length of color code(s). Assumes s is between the pre and
    post escape control sequences.

    Parameters:
      s     Text string.

    Return:
      Print length of code sequence.
    """
    m = s.find(TermColors.ANSI_COLOR_POST)
    if m < 0:
      return 0
    else:
      return m

# -----------------------------------------------------------------------------
# Class Colorize
# -----------------------------------------------------------------------------
class Colorize:
  """ Colorized output class. """

  def __init__(self, prefix='', colors=None):
    """
    Initializer.
    
    Parameters:
      prefix    Notifier optional string prefix.
      colors    TermColors object to bind with. If None, new TermColors is 
                created.
    """
    self._prefix  = prefix
    self._muted = False
    if colors is None:
      self._colors = TermColors()
    else:
      self._colors = colors
    self._colors.synonym('green',     'premsg')
    self._colors.synonym('green',     'num')
    self._colors.synonym('lightblue', 'sep')

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self._colors!r})"

  def __str__(self):
    return "Colorize"

  def __call__(self, color):
    """ Return ANSI color escape sequence string for given color. """
    return self._colors[color]

  def set_prefix(self, prefix):
    """ Set prefix string. """
    self._prefix = str(prefix)

  def mute(self):
    """ Mute terminal writing. """
    self._muted = True

  def unmute(self):
    """ Unmute terminal writing. """
    self._muted = False

  def is_muted(self):
    """ is_muted() -> True or False """
    return self._muted

  def termcolors(self):
    """ Return bound TermColors object. """
    return self._colors

  def colors(self):
    """ Return list of all color tags. """
    return list(self._colors.keys())

  def reset(self):
    """ Reset terminal back to normal (all attributes off) """
    print(self._colors['normal'])

  def debug(self, what, *objs, **kwargs):
    """
    Debug print objects.

    Parameters:
      what    What object(s) are being debugged string.
      objs    Debug objects to pretty print.
      kwargs  Keyword arguments to python3 print and pprint.pprint functions.
    """
    if self._muted:
      return
    prargs = {}
    if 'stream' in kwargs:
      prargs['file'] = kwargs['stream']
    for arg in ['file', 'sep', 'end', 'flush']:
      if arg in kwargs:
        prargs[arg] = kwargs.pop(arg)
        if arg == 'file':
          kwargs['stream'] = prargs[arg]
    self.cprint('lightgray', 'DBG: ', 'lightgray', what, **prargs)
    self.start_color('debug', **prargs)
    for obj in objs:
      pprint(obj, **kwargs)
    self.end_color(**prargs)

  def info(self, *msgs, **kwargs):
    """
    Print information message.

    Parameters:
      msgs    Information message(s).
      kwargs  Keyword arguments to python3 print function.
    """
    if not self._muted:
      self.cprint('info', ' '.join([f"{m}" for m in msgs]), **kwargs)

  def warning(self, *msgs, **kwargs):
    """
    Print warning message.

    Parameters:
      msgs    Warning message(s).
      kwargs  Keyword arguments to python3 print function.
    """
    if not self._muted:
      self._notify('warning', *msgs, **kwargs)

  def error(self, *msgs, **kwargs):
    """
    Print error message.

    Parameters:
      msgs    Error message(s).
      kwargs  Keyword arguments to python3 print function.
    """
    if not self._muted:
      self._notify('error', *msgs, **kwargs)

  def critical(self, *msgs, **kwargs):
    """
    Print critical error message.

    Parameters:
      msgs    Critical error message(s).
      kwargs  Keyword arguments to python3 print function.
    """
    if not self._muted:
      self._notify('critical', *msgs, **kwargs)

  def fatal(self, *msgs, **kwargs):
    """
    Print fatal error message.

    Parameters:
      msgs    Fatal error message(s).
      kwargs  Keyword arguments to python3 print function.
    """
    if not self._muted:
      self._notify('fatal', *msgs, **kwargs)

  def iowarning(self, *msgs, filename=None, line_num=0, **kwargs):
    """
    Print I/O warning message.

    Parameters:
      msgs      Warning message(s).
      filename  Optional filename associated with I/O.
      line_num  Optional line number of filename.
      kwargs    Keyword arguments to python3 print function.
    """
    if not self._muted:
      self._notify('warning', *msgs,
                   filename=filename, line_num=line_num, **kwargs)

  def ioerror(self, *msgs, filename=None, line_num=0, **kwargs):
    """
    Print I/O error message.

    Parameters:
      msgs      Error message(s).
      filename  Optional filename associated with I/O.
      line_num  Optional line number of filename.
      kwargs    Keyword arguments to python3 print function.
    """
    if not self._muted:
      self._notify('error', *msgs,
                   filename=filename, line_num=line_num, **kwargs)

  def iocritical(self, *msgs, filename=None, line_num=0, **kwargs):
    """
    Print I/O critical error message.

    Parameters:
      msgs      Critical message(s).
      filename  Optional filename associated with I/O.
      line_num  Optional line number of filename.
      kwargs    Keyword arguments to python3 print function.
    """
    if not self._muted:
      self._notify('critical', *msgs,
                   filename=filename, line_num=line_num, **kwargs)

  def iofatal(self, *msgs, filename=None, line_num=0, **kwargs):
    """
    Print I/O fatal error message.

    Parameters:
      msgs      Fatal message(s).
      filename  Optional filename associated with I/O.
      line_num  Optional line number of filename.
      kwargs    Keyword arguments to python3 print function.
    """
    if not self._muted:
      self._notify('fatal', *msgs,
                   filename=filename, line_num=line_num, **kwargs)

  def _notify(self, tag, *msgs, filename=None, line_num=0, **kwargs):
    """
    Notifier workhorse function.

    Parameters:
      tag         Notifier color tag synonym.
      msgs        Iterable message segments.
      filename    Optional filename associated with I/O.
      line_num    Optional line number of filename.
      kwargs      Keyword arguments to python3 print function.
    """
    level = tag.capitalize()
    msg = ': '.join([f"{m}" for m in msgs])
    if 'end' in kwargs:
      del kwargs['end']
    if self._prefix:
      self.cprint('premsg', f"{self._prefix}", 'sep', ': ', end='', **kwargs)
    if filename:
      self.cprint('premsg', f"{filename}", end='', **kwargs)
      if line_num > 0:
        self.cprint('sep', ':', 'num', f"{line_num}", end='', **kwargs)
      self.cprint('sep', ': ', end='', **kwargs)
    self.cprint(tag, f"{level}", 'sep', ': ', tag, msg, **kwargs)

  def cprint(self, *args, **kwargs):
    """
    Color print message sequence.

    Note: The flush keyword is now available in python 3.6+.

    Parameters:
      args    Iterable object of a sequence of color,message pairs.
      kwargs  Keyword arguments to python3 print function.
    """
    if not self._muted:
      concat = ''
      for i in range(0,len(args),2):
        concat += "{}{}{}".format(self._colors[args[i]],
                                  args[i+1],
                                  self._colors['normal'])
      flush = kwargs.pop('flush', False)
      print("{}".format(concat), **kwargs)
      if flush:
        sys.stdout.flush()
      
  def ncprint(self, msg, **kwargs):
    """
    No color print message sequence.

    Note: Not all print_function imports support the flush keyword.
          this routine uses sys.stdout flush.

    Parameters:
      msg     Plain messge.
      kwargs  Keyword arguments to python3 print function.
    """
    if not self._muted:
      flush = kwargs.pop('flush', False)
      print("{}".format(msg), **kwargs)
      if flush:
        sys.stdout.flush()

  def start_color(self, tag, **kwargs):
    """
    Start an output block with the given color. Terminate with end_color().

    Parameters:
      tag     Color name or synonym.
      kwargs  Keyword arguments to python3 print function.
    """
    kwargs['end'] = ''
    print(self._colors[tag], **kwargs)

  def end_color(self, **kwargs):
    """ End current color settings and return to default terminal color.

    Parameters:
      kwargs  Keyword arguments to python3 print function.
    """
    kwargs['end'] = ''
    print(self._colors['normal'], **kwargs)

  def plen(self, s):
    """
    Calculate the print length of text string sans terminal escape sequences.

    Parameters:
      s     Text string.

    Return:
      Print length of text.
    """
    return self._colors.plen(s)

  def ul(self, s):
    """ Underline string s with unicode combining diacritic. """
    t = ''
    for c in s:
      t += c
      t += '\u0332'
    return t

  def hr(self, n=80, dline=False, color='normal'):
    """
    Output horizontal rule with unicode line code.

    Parameters:
      n       Length of rule in characters.
      dline   Create double line. Default: single.
      color   Color (synonym) of rule.
    """
    if dline:
      line = '\u2550' * n
    else:
      line = '\u2500' * n
    self.cprint(color, line)
