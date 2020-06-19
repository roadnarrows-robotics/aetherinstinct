"""
Unit test the color module.

\LegalBegin
Copyright 2020 Aether Instinct LLC. All Rights Reserved

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

# import unit test framework
import aetherinstinct.testing.ut as ut

# import system under test 
import aetherinstinct.utils.color as sut

RArrow = ut.UTString.RARROW.value

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utTC(ut.UT):
  """ Unit test TermColors class. """
  def __init__(self, dskey):
    super().__init__("<func>", dskey)
    self.fruit = {
      'apple':        'lightgreen',
      'lemon':        'yellow',
      'pomegranate':  'lightred',
      'apricot':      'brown',
      'fig':          'purple',
    }

  def begin(self, sequencer, datum):
    self.cmd = datum
    return (f"{self.cmd}()", ut.UTState.PASS)

  def test(self, sequencer, datum):
    tc = sequencer['tc']
    output = ut.UTStringIO()
    if self.cmd == 'list':
      self.colorlist(tc, output.stream)
    elif self.cmd == 'enable':
      tc.enable_color()
      print("Colors are enabled.", file=output.stream)
    elif self.cmd == 'disable':
      tc.disable_color()
      print("Colors are disabled.", file=output.stream)
    elif self.cmd in tc:
      self.favcolor(tc, self.cmd, output.stream)
    elif self.cmd in self.fruit:
      tc.synonym(self.fruit[self.cmd], self.cmd)
      self.eatfruit(tc, self.cmd, output.stream)
    else:
      print(f"Yes, '{self.cmd}' is a word.", file=output.stream)
    return ut.UTState.PASS, [f"{RArrow}"] + output.lines()

  def colorlist(self, tc, stream):
    col = 0
    norm = tc['normal']
    for k,v in tc.items():
      print(f"{v}{k:<16}{norm}", end='', file=stream)
      col += 1
      if col == 4:
        print('', file=stream)
        col = 0

  def favcolor(self, tc, color, stream):
    print(f"My favorite color is {tc[color]}{color}{tc['normal']}.\n"
          f"It is {tc[color]}so pretty{tc['normal']}, don't ya think?",
          file=stream)

  def eatfruit(self, tc, fruit, stream):
    print(f"I eat {fruit}s only if they are "
          f"{tc[fruit]}this color{tc['normal']}.", file=stream)

class utCPrint(ut.UT):
  """ Unit test color cprint(). """
  def __init__(self, dskey):
    super().__init__("cprint()", dskey)
    self.color = 'normal'

  def begin(self, sequencer, datum):
    self.color = datum
    return (f"cprint({self.color}, ...)", ut.UTState.PASS)

  def test(self, sequencer, datum):
    output = ut.UTStringIO()
    fox = 'The quick {} fox jumps over the lazy dog.'
    sequencer['tcw'].cprint(self.color, fox.format(self.color),
                            file=output.stream)
    return ut.UTState.PASS, [f"{RArrow}"] + output.lines()

class utNCPrint(ut.UT):
  """ Unit test color ncprint(). """
  def __init__(self, dskey):
    super().__init__("ncprint()", dskey)
    self.text = None

  def begin(self, sequencer, datum):
    self.text = datum
    return (f"ncprint(...)", ut.UTState.PASS)

  def test(self, sequencer, datum):
    output = ut.UTStringIO()
    sequencer['tcw'].ncprint(self.text, file=output.stream)
    return ut.UTState.PASS, [f"{RArrow}"] + output.lines()

class utNotifier(ut.UT):
  """ Unit test color notifiers. """

  def __init__(self, dskey):
    super().__init__("notifiers", dskey)

  def prep(self, sequencer):
    super().prep(sequencer)
    self.notifymap = {
      'debug':    sequencer['tcw'].debug,
      'info':     sequencer['tcw'].info,
      'warning':  sequencer['tcw'].warning,
      'error':    sequencer['tcw'].error,
      'critical': sequencer['tcw'].critical,
      'fatal':    sequencer['tcw'].fatal,
    }

  def begin(self, sequencer, datum):
    self.what = datum[0]
    self.args = datum[1]
    if self.what in self.notifymap:
      return (f"{self.what}(...)", ut.UTState.PASS)
    else:
      return (f"{self.what}(...)", ut.UTState.FAIL)

  def test(self, sequencer, datum):
    output = ut.UTStringIO()
    if self.what in self.notifymap:
      if isinstance(self.args, list) or isinstance(self.args, tuple):
        self.notifymap[self.what](*self.args, file=output.stream)
      else:
        self.notifymap[self.what](self.args, file=output.stream)
      res = ut.UTState.PASS
    else:
      sequencer.fail(f"'{self.what}' is not a valid notification level",
            file=output.stream)
      res = ut.UTState.FAIL
    return res, [f"{RArrow} "] +  output.lines()

class utIONotifier(ut.UT):
  """ Unit test color I/O notifiers. """

  def __init__(self, dskey):
    super().__init__("ionotifiers", dskey)

  def prep(self, sequencer):
    super().prep(sequencer)
    self.notifymap = {
      'iowarning':  sequencer['tcw'].iowarning,
      'ioerror':    sequencer['tcw'].ioerror,
      'iocritical': sequencer['tcw'].iocritical,
      'iofatal':    sequencer['tcw'].iofatal,
    }
    sequencer['tcw'].set_prefix('cmd')

  def begin(self, sequencer, datum):
    self.what   = datum[0]
    self.msgs   = datum[1]
    self.fname  = datum[2]
    self.lnum   = datum[3]
    if self.what in self.notifymap:
      return (f"{self.what}(...)", ut.UTState.PASS)
    else:
      return (f"{self.what}(...)", ut.UTState.FAIL)

  def test(self, sequencer, datum):
    output = ut.UTStringIO()
    if self.what in self.notifymap:
      if isinstance(self.msgs, list) or isinstance(self.msgs, tuple):
        self.notifymap[self.what](*self.msgs, filename=self.fname,
                                  line_num=self.lnum, file=output.stream)
      else:
        self.notifymap[self.what](self.msgs, filename=self.fname,
                                  line_num=self.lnum, file=output.stream)
        res = ut.UTState.PASS
    else:
      print(f"'{self.what}' is not a valid I/O notification level",
            file=output.stream)
      res = ut.UTState.FAIL
    return res, [f"{RArrow} "] +  output.lines()

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
colors = sut.TermColors()

dsTC = ut.UTDataset('ds_tc',
    data=[
      'list', 'cyan', 'apple', 'disable', 'red', 'enable', 'red',
      'apple', 'lemon', 'pomegranate', 'apricot', 'fig', 'mango', 'list',
    ])

dsColors = ut.UTDataset('ds_colors', data=list(colors))

dsNoColor = ut.UTDataset('ds_no_colors',
    data=["""\
Color had not been invented yet during the first few years after
World War II. It was a simpler time.
Everything was black and white."""])

# termcolorwriter notifiers plus unknown
dsNotifiers = ut.UTDataset('ds_notifiers',
  data=[
    ('debug',
      ['similes',
        { 'brave': 'as a lion',
          'fought': 'like cats and dogs',
          'funny': 'as a barrel of monkeys',
          'clear': 'as mud'
        }
      ]
    ),
    ('info', 'it is none of your business'),
    ('warning', 'moving sidewalk is coming to an end'),
    ('error', 'is human, vengence demonic'),
    ('critical', 'thinking is welcome'),
    ('fatal', [42, 'is not the question']),
    ('wtf', 'not a valid level'),
  ])

dsIONotifiers = ut.UTDataset('ds_io_notifiers',
  data=[
    ('iowarning', 'a file warning', 'fake.txt', 5),
    ('ioerror', 'a file error', 'fake.txt', 20),
    ('iocritical', 'a file critical error', 'fake.txt', 40),
    ('iofatal', 'a file open fatal error', 'fake.txt', 0),
  ])

# the database of datasets
db = ut.UTDsDb('db',
               ds=[dsTC, dsColors, dsNoColor, dsNotifiers, dsIONotifiers])

# test suite
suite = ut.UTSuite('testsuite',
  subsystems=[
    ut.UTSubsys('TermColors', "Test TermColors class.",
      unittests=[
        utTC(dsTC.name),
      ]
    ),
    ut.UTSubsys('Colorize', "Test Colorize class.",
      unittests=[
        utCPrint(dsColors.name),
        utNCPrint(dsNoColor.name),
        utNotifier(dsNotifiers.name),
        utIONotifier(dsIONotifiers.name),
      ]
    ),
  ],
)

# unit test sequencer
utseq = ut.UTSequencer('color', suite, db, tc=colors, tcw=sut.Colorize())

# required entry point function for unittest.py script
def utmain():
  return ut.UTMainTemplate(utseq, "Unit test utils.color module.")
