"""
Unit test the prettyprint module.

\LegalBegin
  MIT
\LegalEnd
"""

import random
from enum import Enum

# import unit test framework
import aetherinstinct.testing.ut as ut

# import system under test 
import aetherinstinct.utils.prettyprint as sut

RArrow = ut.UTString.RARROW.value
IsDef = ut.UTString.IS_DEF.value
IsTrue = ut.UTString.IS_TRUE.value

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utPrint(ut.UT):
  """ Unit test print2col and print_to_str. """
  def __init__(self, dskey):
    self.indent = 6
    self.sep = ' ::='
    super().__init__(f"print2col(indent={self.indent}, sep={self.sep!r})",
        dskey)

  def begin(self, sequencer, datum):
    return (f"Lichen Genus", ut.UTState.PASS)

  def test(self, sequencer, datum):
    lines = sut.print_to_str(sut.print2cols, datum, indent=self.indent,
                             sep=self.sep)
    return (ut.UTState.PASS, [f"two columns {RArrow}"] + lines.split('\n'))

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
dsLichen = ut.UTDataset('ds_lichen',
  data = [[
    ("Ball lichen",             "Sphaerophorus"),
    ("Barnacle lichen",         "Thelotrema"),
    ("Beard lichen",            "Usnea"),
    ("Birchbark dot lichen",    "Leptorhaphis"),
    ("Blackcurly lichen",       "Pseudephebe"),
    ("Blackthread lichen",      "Placynthium"),
    ("Blemished lichen",        "Phlyctis"),
    ("Blistered navel lichen",  "Lasallia"),
    ("Blood lichen",            "Mycoblastus"),
    ("Bloodstain lichen",       "Haematomma"),
    ("Bowl lichen",             "Psoroma"),
    ("Bran lichen",             "Parmeliopsis"),
    ("Brittle lichen",          "Cornicularia"),
    ("Bullseye lichen",         "Placopsis"),
    ("Bruised lichen",          "Toninia"),
    ("Button lichen",           "Buellia"),
    ("Cap lichen",              "Baeomyces"),
    ("Cartilage lichen",        "Ramalina"),
    ("Chocolate chip lichen",   "Solorina"),
    ("Clam lichen",             "Normandina"),
    ("Club lichen",             "Multiclavula"),
    ("Cobblestone lichen",      "Acarospora"),
    ("Cockleshell lichen",      "Hypocenomyce"),
    ("Comma lichen",            "Arthonia"),
    ("Chalice lichen",          "Endocarpon"),
    ("Coral lichen",            "Sphaerophorus"),
    ("Crabseye lichen",         "Ochrolechia"),
    ("Cracked lichen",          "Acarospora"),
    ("Crater lichen",           "Diploschistes"),
    ("Cup lichen",              "Cladonia"),
  ]]
)

ColoradoWildflowers = {
  'blue flax':            'Linum lewisii',
  'sego lily':            'Calochrtus flexuosus',
  'Colorado columbine':   'Aquilegia coerulea',
  'cowboys delight':      'Sphaeralcea coccinea',
  'paintbrush':           'Castilleja integra',
  'Gaillardia':           'Gaillardia aristata',
}

dsFlowers = ut.UTDataset('ds_flowers', [ColoradoWildflowers.items()])

# the database of datasets
db = ut.UTDsDb('db', ds=[dsLichen, dsFlowers])

# test suite
suite = ut.UTSuite('testsuite',
  subsystems=[
    ut.UTSubsys('print', "Test print2cols and print_to_str functions.",
      unittests=[
        utPrint(dsLichen.name),
        utPrint(dsFlowers.name),
      ]
    ),
  ],
)

# unit test sequencer
utseq = ut.UTSequencer('prettyprint', suite, db)

# required entry point function for unittest.py script
def utmain():
  return ut.UTMainTemplate(utseq, "Unit test utils.prettyprint module.")
