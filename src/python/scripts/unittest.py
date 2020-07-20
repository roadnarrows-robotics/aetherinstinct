#!/usr/bin/env python3
#
# File:
#   unittest.py
#
# Usage:
#   unittest.py [OPTIONS] [SUT[.SSUT]]...
#   unittest.py [OPTIONS] all
#   unittest.py --help
#
# Description:
#
# \LegalBegin
# MIT
# \LegalEnd

import os
import sys
import getopt
import importlib
from collections import OrderedDict
from pprint import pprint

# bootstrap environment
WS = os.environ.get('AI_WORKSPACE')
if not WS:
  raise NameError("'AI_WORKSPACE' environment variable not defined")
WsPyDir = os.path.join(WS, 'src', 'python')
AIDir   = 'aetherinstinct'
sys.path.insert(0, WsPyDir)

# unit test framework
import aetherinstinct.testing.ut as ut

# -----------------------------------------------------------------------------
class UsageError(Exception):
  """ Command-Line Options UsageError Exception Class. """
  def __init__(self, msg):
    self.msg = msg

# -----------------------------------------------------------------------------
class UnitTestEngine:
  """ Unit test engine application class. """

  def __init__(self):
    """ Initializer. """
    self.colorize   = ut.UTColorize()
    self.mod_names  = []
    self.suts       = OrderedDict()
    self._dummy     = ut.UTSequencer('dummy', None, None)

  def run(self):
    """ Run unit tests. """
    if not self.suts:
      self.import_suts()
    if self.kwargs['sut'] == 'all':
      self.run_all_tests()
    else:
      self.run_selected_tests()

  def run_all_tests(self):
    """ Run all unit tests for all SUTs. """
    stats = ut.UTStats()
    for sut, data in self.suts.items():
      utseq = data['utseq']
      utseq.coloring = self.kwargs['color']
      stats += utseq.run(testnames=data['ssuts'])
      self.hr()
    self.print_stats('Grand Total', stats)

  def run_selected_tests(self):
    """ Run command-line selected unit tests. """
    stats = ut.UTStats()
    for arg in self.kwargs['sut']:    # SUT[.SSUT]
      tst = arg.split('.', 1)
      sut = tst[0]
      if len(tst) == 2:
        ssuts = [tst[1]]
      else:
        ssuts = []
      stats += self.run_sut_tests(sut, ssuts)
      self.hr()
    self.print_stats('Grand Total', stats)

  def run_sut_tests(self, sut, ssuts):
    """
    Run SUT unit test(s).

    Parameters:
      sut     System under test.
      ssuts   List of subsystem unit tests.

    Return:
      Return test statistics.
    """
    stats = ut.UTStats()
    if sut not in self.suts:
      self.error(f"'{sut}'", 'system under test does not exist')
      return stats
    utseq = self.suts[sut]['utseq']
    utseq.coloring = self.kwargs['color']
    avail_ssuts = self.suts[sut]['ssuts']
    if not ssuts:
      ssuts = avail_ssuts
    else:
      good_ssuts = []
      for ssut in ssuts:
        if ssut in avail_ssuts:
          good_ssuts.append(ssut)
        else:
          self.error(f"'{ssut}'",
                     f"subsystem unit test does not exist for '{sut}'")
      ssuts = good_ssuts
    if ssuts:
      stats += utseq.run(testnames=ssuts)
    return stats

  def list_suts(self):
    """ List all available unit tests. """
    if not self.suts:
      self.import_suts()
    c1w = 1
    for sut in self.suts:
      if len(sut) > c1w:
        c1w = len(sut)
    c1w += 2
    indent = c1w + 1
    maxw = self.columns - indent - 1
    c1 = f"{'SUT':<{c1w}}"
    c2 = "SSUTs"
    print(f"{self.colorize(c1,'brown')} {self.colorize(c2, 'cyan')}")
    print(f"{'---':<{c1w}} -----")
    for sut, data in self.suts.items():
      c1 = f"{sut:<{c1w}}"
      print(f"{self.colorize(c1,'brown')} ", end='')
      c2w = 0
      for ssut in data['ssuts']:
        c2w += len(ssut) + 1
        if c2w <= maxw:
          print(f"{self.colorize(ssut,'cyan')} ", end='')
        else:
          print(f"\n{' ':<{indent}}{self.colorize(ssut,'cyan')} ", end='')
          c2w = len(ssut)
      print()

  def import_suts(self):
    """ Import SUTs. """
    if not self.mod_names:
      self.mod_names = self.find_modules()
    for m in self.mod_names:
      try:
        utmod = importlib.import_module(m)
      except ImportError:
        self.fatal(8, m, 'cannot import')
      try:
        utseq   = utmod.utseq
        utname  = utseq.name
        ssuts   = utseq.get_avail_tests()
      except AttributeError as e:
        self.error(m, f"{e}")
      else:
        self.suts[utname] = {
          'mod_name': m, 'import': utmod, 'utseq': utseq, 'ssuts': ssuts
        }

  def find_modules(self):
    """ Find all unit test modules by file name. """
    topdir = os.path.join(WsPyDir, AIDir)
    paths = []
    for root, dirs, files in os.walk(topdir):
      if os.path.basename(root) in ['ut', 'rut']:
        for f in files:
          if f.startswith('ut') and f.endswith('.py'):
            paths.append(os.path.join(root, f))
    names = []
    for p in paths:
      p = p[len(WsPyDir)+1:-len('.py')]
      names.append(p.replace('/', '.'))
    return names

  def print_stats(self, name, stats):
    """ Print statistics. """
    self._dummy.print_stats(name, stats)

  @property
  def columns(self):
    """ Terminal column width. """
    return self._dummy.columns

  def hr(self):
    """ Draw horizontal rule. """
    self._dummy.hr(self.columns, dline=True, color='lightblue')

  def debug(self, what, *objs):
    """ Debug. """
    if self.kwargs['debug']:
      print(self.colorize(f"DBG: {what}", 'lightgray'))
      for obj in objs:
        pprint(obj)

  def error(self, *emsgs):
    """
    Print error message.

    Parameters:
      emsgs     Arguments to the message.
    """
    pre = 'Error: '
    msg = ': '.join([m for m in emsgs])
    print(self.colorize(pre+msg, 'lightred'))

  def fatal(self, ec, *emsgs, filename=None, line_num=0):
    """
    Print fatal message and exit.

    Parameters:
      ec        Exit code.
      emsgs     Arguments to the message.
      filename  Optional filename associated with I/O.
      line_num  Option line number of filename.
    """
    pre = 'Fatal:'
    msg = ': '.join([m for m in emsgs])
    if filename:
      pre += f" {filename}:"
    if line_num > 0:
      pre += f"{line_num}:"
    pre += ' '
    print(self.colorize(pre+msg, 'lightpurple'))
    sys.exit(ec)

  def turn_off_color(self):
    """ Disable color output. """
    self.colorize.disable()

  def print_usage_error(self, *args):
    """ Print error usage message. """
    emsg = ': '.join([f"{a}" for a in args])
    if emsg:
      print(f"{self.argv0}: error: {emsg}")
    else:
      print(f"{self.argv0}: error")
    print(f"Try '{self.argv0} --help' for more information.")
  
  def print_help(self):
    """ Print command-line help. """
    print(f"""\
Usage: {self.argv0} [OPTIONS] [SUT[.SSUT]]...
       {self.argv0} [OPTIONS] all
       {self.argv0} --help

Run the unit test engine to test the given list of Systems Under Test (SUT) and
Subsystem Unit Tests (SSUT).

Options:
      --debug         Enable debugging.

      --no-color      Disable color output.

      --list          List available unit tests.
  
  -h, --help          Display this help and exit.

Description:
Each System Under Test (SUT) contains one or more subsystem unit tests. The
syntax SUT.SSUT informs the unit test engine to run unit tests on that SSUT.
If SSUT is omitted, then all SUT unit tests are ran. The keyword 'all' will
run the unit test engine on all found SUT's.
""")

  def get_options(self, argv):
    """ Get main options and arguments. """
    self.argv0 = os.path.basename(argv[0])

    # option defaults
    kwargs = {}
    kwargs['color'] = True
    kwargs['debug'] = False
    kwargs['list']  = False
    kwargs['sut']   = []

    shortopts = "?h"
    longopts  = ['help', 'debug', 'no-color', 'list']

    # parse command-line options
    try:
      try:
        opts, args = getopt.getopt(argv[1:], shortopts, longopts=longopts)
      except getopt.error as msg:
        raise UsageError(msg)
      for opt, optarg in opts:
        if opt in ('-h', '--help', '-?'):
          self.print_help()
          sys.exit(0)
        elif opt in ('--no-color',):
          kwargs['color'] = False
          self.turn_off_color()
          self._dummy.coloring = kwargs['color']
        elif opt in ('--debug'):
          kwargs['debug'] = True
        elif opt in ('--list'):
          kwargs['list'] = True
    except UsageError as err:
      self.print_usage_error(err.msg)
      sys.exit(2)

    if 'all' in args:
      kwargs['sut'] = 'all'
    else:
      kwargs['sut'] = args

    return kwargs

  def main(self, argv):
    """ main unit """
    self.kwargs = self.get_options(argv)

    self.debug('kwargs =', self.kwargs)

    self.mod_names = self.find_modules()

    self.debug('mod_names =', self.mod_names)

    if self.kwargs['list']:
      self.list_suts()

    if len(self.kwargs['sut']) > 0:
      self.run()

    return 0

# -----------------------------------------------------------------------------
app = UnitTestEngine()
sys.exit( app.main(sys.argv) )
