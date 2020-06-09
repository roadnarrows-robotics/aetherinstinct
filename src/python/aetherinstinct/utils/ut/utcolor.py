#
# Unit test the color module.
#
# File: utcolor.py
#
# Author: Robin Knight
#
# Copyright 2020 Aether Instinct LLC. All Rights Reserved
#
# Licensed under the MIT License (the "License").
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at:
#
#   https://opensource.org/licenses/MIT
#
# The software is provided "AS IS", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. in no event shall the
# authors or copyright holders be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising from,
# out of or in connection with the software or the use or other dealings in the
# software.
#

import io

import aetherinstinct.testing.ut as ut
import aetherinstinct.utils.color as sut

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utCPrint(UT):
  """ Unit test color cprint(). """
  def __init__(self, dskey):
    UT.__init__(self, "cprint()", dskey)

  def begin(self, sequencer, datum):
    self.colors = sequencer['tcw'].colors()
    return (f"cprint(...)", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      i = 1
      for color in self.colors:
        sequencer['tcw'].cprint(
          'normal', f"{i:>2}. ",
          color, f"The quick {color} fox jumps over the lazy dog.",
          file=output)
        i += 1
      olines = output.getvalue().split('\n')
    if not olines[-1]:
      olines = olines[:-1]
    return UTState.PASS, [f"{uRArrow} output with color"] + olines

class utNCPrint(UT):
  """ Unit test color ncprint(). """
  def __init__(self, dskey):
    UT.__init__(self, "ncprint()", dskey)

  def begin(self, sequencer, datum):
    return (f"ncprint(...)", UTState.PASS)

  def test(self, sequencer, datum):
    ncprint = sequencer['tcw'].ncprint
    with io.StringIO() as output:
      ncprint("Boy: Look Ma! No hands.", file=output, end=' ')
      ncprint("(crash, bam, ouch)", file=output)
      ncprint(" Ma: Get a job boy!",file=output,  flush=True)
      olines = output.getvalue().split('\n')
    if not olines[-1]:
      olines = olines[:-1]
    return UTState.PASS, [f"{uRArrow} output with no color"] + olines

class utNotifier(UT):
  """ Unit test color notifier. """
  Notifiers = ['debug', 'info', 'warn', 'error', 'critical']

  def __init__(self, dskey):
    UT.__init__(self, "notifier", dskey)

  def begin(self, sequencer, datum):
    self.what = datum
    if self.what in utNotifier.Notifiers:
      return (f"{self.what}(...)", UTState.PASS)
    else:
      return (f"{self.what}(...)", UTState.FAIL)

  def test(self, sequencer, datum):
    if self.what == 'debug':
      self.notifier = sequencer['tcw'].debug
    elif self.what == 'info':
      self.notifier = sequencer['tcw'].info
    elif self.what == 'warn':
      self.notifier = sequencer['tcw'].warn
    elif self.what == 'error':
      self.notifier = sequencer['tcw'].error
    elif self.what == 'critical':
      self.notifier = sequencer['tcw'].critical
    else:
      return (UTState.FAIL, f"{self.what!r} is an unknown notifier")

    with io.StringIO() as output:
      self.notifier(f"This is a {self.what} notifier. That is all.",
                    file=output)
      notice = output.getvalue().split('\n')
    if not notice[-1]:
      notice = notice[:-1]
    res = UTState.PASS
    ans = [f"{uRArrow} output"] +  notice
    return res, ans

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------

# termcolorwriter notifiers plus unknown
dsNotifiers = UTDataset('ds_notifiers',
                data=['debug', 'info', 'warn', 'error', 'critical', 'wtf'])

# the database of datasets
db = UTDsDb('db', ds=[dsBoilOne, dsNotifiers])

suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('TermColorWriter', "Test terminal color writer class.",
      unittests=[
        utCPrint(dsBoilOne),
        utNCPrint(dsBoilOne),
        utNotifier(dsNotifiers),
      ]
    ),
  ],
)

utseq = UTSequencer('color', suite, db, tcw=sut.TermColorWriter())

#utmain = lambda: UTMainTemplate(utseq, "Unit test color module.")
def utmain():
  return UTMainTemplate(utseq, "Unit test color module.")

