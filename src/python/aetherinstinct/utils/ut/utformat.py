"""
Unit test the format module.

Package:
  RoadNarrows elemenpy python package.

\LegalBegin
  MIT
\LegalEnd
"""

import io
import random
from enum import Enum

from aetherinstinct.utils.common import (enumfactory)

# import unit test framework
import aetherinstinct.testing.ut as ut

# import system under test 
import aetherinstinct.utils.format as sut

RArrow  = ut.UTString.RARROW.value
Ok      = ut.UTString.OK.value
Nok     = ut.UTString.NOK.value
Maybe   = ut.UTState.WARN.value

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utParser(ut.UT):
  """ Unit test EncoderParser class. """
  def __init__(self, dskey, encoder=sut.default_encoder):
    self.encoder = encoder
    super().__init__(f"EncoderParser({self.encoder})", dskey)

  def begin(self, sequencer, datum):
    self.expr = datum[0]
    self.pf   = datum[1]
    if self.pf == Maybe:
      if self.encoder.parser.strict:
        self.pf = Nok
      else:
        self.pf = Ok
    return (f"{self.expr!r}", enumfactory(ut.UTState, self.pf))

  def test(self, sequencer, datum):
    try:
      encode = self.encoder.parse(self.expr)
    except sut.EncoderParseError as e:
      res = ut.UTState.FAIL
      elines = str(e).split('\n')
      ans = [f"{RArrow}", sequencer.failstr("parse")] + elines
    else:
      res = ut.UTState.PASS
      ans = f"{RArrow} {encode}"
    return (res, ans)

class utPrintEncodingTables(ut.UT):
  """ Unit test EncodingTables class. """
  def __init__(self, dskey, encoder=sut.default_encoder, in_ascii=False):
    self.encoder  = encoder
    self.in_ascii = in_ascii
    if self.in_ascii:
      super().__init__(f"{encoder}.print_table(in_ascii)", dskey)
    else:
      super().__init__(f"{encoder}.print_table()", dskey)

  def begin(self, sequencer, datum):
    self.tid = datum
    return f"{self.tid!r}", ut.UTState.PASS

  def test(self, sequencer, datum):
    return ut.UTState.PASS, f"{RArrow}"

  def end(self, sequencer):
    self.encoder.print_table(self.tid, in_ascii=self.in_ascii)

class ut4Some(ut.UT):
  """ Unit test Format4Some class. """
  def __init__(self, dskey):
    super().__init__(f"Format4Some()", dskey)

  def begin(self, sequencer, datum):
    self.expr = datum[0]
    self.pf   = datum[1]
    return (f"{self.expr!r}", enumfactory(ut.UTState, self.pf))

  def test(self, sequencer, datum):
    try:
      fset = sut.Format4Some(self.expr)
    except sut.EncoderParseError as e:
      res = ut.UTState.FAIL
      elines = str(e).split('\n')
      ans = [f"{RArrow}", sequencer.failstr('parser')] + elines
    else:
      output = ut.UTStringIO()
      fset.print4(file=output.stream)
      res = ut.UTState.PASS
      ans = [f"{RArrow}"] + output.lines()
    return (res, ans)

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------

dsHtmlTbls    = ut.UTDataset('ds_html_tbls', data=sut.html_encoder.tid_list())
dsLatexTbls   = ut.UTDataset('ds_latex_tbls', data=sut.latex_encoder.tid_list())
dsPlainTbls   = ut.UTDataset('ds_plain_tbls', data=sut.plain_encoder.tid_list())
dsUnicodeTbls = ut.UTDataset('ds_unicode_tbls',
                             data=sut.unicode_encoder.tid_list())

dsParser = ut.UTDataset('ds_parser',
  data = [
    # good test cases
    ("My plain world.", Ok),
    ("I have \$2 to my name.", Ok),
    ("A$sup(123)", Ok),
    ("I$sub(\(123\))", Ok),
    ("$greek(Omega) man and his dog $greek(phi)do.", Ok),
    ("\$50$math(*)10$sup(9) dollars, ooh baby.", Ok),
    ("To $math(inf) and beyond.", Ok),
    ("Spodumene: LiAlSi$sub(2)O$sub(6)$sup(+)", Ok),
    ("$frac(3,5) is 60%", Ok),
    ("j$math(hat)$math(+-)5", Ok),
    ("$script(ABZN)", Ok),
    ("M$sub($frac(1,2))", Ok),

    # maybe's - depends on parser strict value
    ("reduced Planck constant: $phy(h-bar)", Maybe),
    ("$roman(A)", Maybe),
    ("$greek(tome)", Maybe),

    # bad test cases
    ("$greek Beta)", Nok),
    ("$math(>=", Nok),
    ("$", Nok),
    ("$frac(1,2,3)", Nok),

    # good in a weird way
    ("escape \\", Ok),
    ("$frac(1,apple)", Ok),
  ]
)

dsParser2 = ut.UTDataset('ds_parser2',
  data = [
    ("$math(sum)$sub(x=0)$sup(10)x = $arabic(55)", Ok), 
    ("The $greek(Phi)$greek(Kappa)$greek(Sigma) Frat Boys", Ok),
    ("99 $math(<) 100", Ok),
  ]
)

# the database of datasets
db = ut.UTDsDb('db',
  ds=[dsParser, dsParser2, dsUnicodeTbls, dsHtmlTbls, dsLatexTbls, dsPlainTbls])

suite = ut.UTSuite('testsuite',
  subsystems=[
    # Format4Some
    ut.UTSubsys('4some', 'Test Format4Some class.',
      unittests=[
        ut4Some(dsParser2.name),
      ]
    ),

    # html
    ut.UTSubsys('hparser', 'Test html parser.',
      unittests=[
        utParser(dsParser.name, encoder=sut.html_encoder),
      ]
    ),
    ut.UTSubsys('htables', 'Print html tables in markup.',
      unittests=[
        utPrintEncodingTables(dsHtmlTbls.name, encoder=sut.html_encoder),
      ]
    ),

    # latex
    ut.UTSubsys('lparser', 'Test latex parser.',
      unittests=[
        utParser(dsParser.name, encoder=sut.latex_encoder),
      ]
    ),
    ut.UTSubsys('ltables', 'Print latex tables in markup.',
      unittests=[
        utPrintEncodingTables(dsLatexTbls.name, encoder=sut.latex_encoder),
      ]
    ),

    # plain text
    ut.UTSubsys('pparser', 'Test plain text parser.',
      unittests=[
        utParser(dsParser.name, encoder=sut.plain_encoder),
      ]
    ),
    ut.UTSubsys('ptables', 'Print plain text tables in ascii.',
      unittests=[
        utPrintEncodingTables(dsPlainTbls.name, encoder=sut.plain_encoder),
      ]
    ),

    # unicode
    ut.UTSubsys('uparser', 'Test unicoder parser.',
      unittests=[
        utParser(dsParser.name, encoder=sut.unicode_encoder),
      ]
    ),
    ut.UTSubsys('utables', 'Print unicode tables in unicode.',
      unittests=[
        utPrintEncodingTables(dsUnicodeTbls.name, encoder=sut.unicode_encoder),
      ]
    ),
    ut.UTSubsys('utables_ascii',
                'Print unicode tables in ascii representation.',
      unittests=[
        utPrintEncodingTables(dsUnicodeTbls.name, encoder=sut.unicode_encoder,
          in_ascii=True),
      ]
    ),
  ],
)

# unit test sequencer
utseq = ut.UTSequencer('format', suite, db)

# required entry point function for unittest.py script
def utmain():
  return ut.UTMainTemplate(utseq, "Unit test utils.format module.")
