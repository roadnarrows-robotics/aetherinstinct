"""
Reflexive unit test the unit testing framework.

\LegalBegin
  MIT
\LegalEnd
"""

import random

# import system under test 
import aetherinstinct.testing.ut as sut

RArrow  = sut.UTString.RARROW.value
NEq     = sut.UTString.NEQ.value

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utDsClass(sut.UT):
  """ Test UTDataset class. """
  def __init__(self, dskey):
    super().__init__('UTDataset', dskey)

  def begin(self, sequencer, datum):
    self.opcode = datum[0]
    self.opands = datum[1]

    i = self.opcode.find('.error')
    if i < 0:
      expect = sut.UTState.PASS
    else:
      self.opcode = self.opcode[:i]
      expect = sut.UTState.FAIL
    return f"{self.opcode}{self.opands}", expect

  def test(self, sequencer, datum):
    if self.opcode == 'create':
      return self.test_create(sequencer)
    elif self.opcode == 'copy':
      return self.test_copy(sequencer)
    elif self.opcode == 'add':
      return self.test_add(sequencer)
    elif self.opcode == 'iadd':
      return self.test_iadd(sequencer)
    elif self.opcode == 'append':
      return self.test_append(sequencer)
    elif self.opcode == 'pair':
      return self.test_pair(sequencer)
    elif self.opcode == 'print':
      return self.test_print(sequencer)
    else:
      return (sut.UTState.FAIL,
              sequencer.failstr(f"{self.opcode!r} unknown operator"))

  def test_create(self, sequencer):
    how  = self.opands[0] # 'random'
    name = self.opands[1]
    if how == 'random':
      dslen = 10
      ds = sut.UTDataset(name, [random.randint(1,100) for i in range(dslen)])
      if len(ds) == dslen:
        res = sut.UTState.PASS
        ans = [f"{RArrow} created", f"{ds.name}: {ds.data}"]
      else:
        res = sut.UTState.FAIL
        ans = sequencer.failstr(f"{len(ds)} {NEq} {dslen}")
    else:
      res = sut.UTState.FAIL
      ans = sequencer.failstr(f"{how!r} unknown operand")
    return (res, ans)

  def test_copy(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    ds  = ds1.copy()
    if ds.name == ds1.name and ds.data == ds1.data:
      res = sut.UTState.PASS
      ans = [f"{RArrow} copied", f"{ds.name}: {ds.data}"]
    else:
      res = sut.UTState.FAIL
      ans = [ sequencer.failstr(f"{ds.name} data {NEq} {ds1.name} data"),
              f"{ds.data}",
              f"{ds1.data}"]
    return (res, ans)

  def test_add(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    ds2 = sequencer.dsdb[self.opands[1]]
    ds = ds1 + ds2
    if len(ds) != len(ds1) + len(ds2):
      res = sut.UTState.FAIL
      ans = sequencer.failstr(f"{len(ds)} {NEq} {len(ds1)}+{len(ds2)}")
    elif ds[0] != ds1[0] or ds[-1] != ds2[-1]:
      res = sut.UTState.FAIL
      ans = sequencer.failstr(f"bad add")
    else:
      res = sut.UTState.PASS
      ans = [f"{RArrow} added", f"{ds.name}: [{ds[0]}, ..., {ds[-1]}]"]
    return (res, ans)

  def test_iadd(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    ds2 = sequencer.dsdb[self.opands[1]]
    ds = ds1.copy()
    ds += ds2
    if len(ds) != len(ds1) + len(ds2):
      res = sut.UTState.FAIL
      ans = sequencer.failstr(f"{len(ds)} {NEq} {len(ds1)}+{len(ds2)}")
    elif ds[0] != ds1[0] or ds[-1] != ds2[-1]:
      res = sut.UTState.FAIL
      ans = sequencer.failstr(f"bad add")
    else:
      res = sut.UTState.PASS
      ans = [ f"{RArrow} in-place added",
              f"{ds.name}: [{ds[0]}, ..., {ds[-1]}]"]
    return (res, ans)

  def test_append(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    datum = self.opands[1]
    ds = ds1.copy()
    ds.append(datum)
    if len(ds) != len(ds1) + 1:
      res = sut.UTState.FAIL
      ans = sequencer.failstr(f"{len(ds)} {NEq} {len(ds1)}+1")
    elif ds[0] != ds1[0] or ds[-1] != datum:
      res = sut.UTState.FAIL
      ans = [ sequencer.failstr(f"bad append"),
              f"{ds.data}",
              f"{datum}",
              f"{ds1.data}"]
    else:
      res = sut.UTState.PASS
      ans = [ f"{RArrow} appended",
              f"{ds.name}: [{ds[0]}, ..., {ds[-1]}]"]
    return (res, ans)

  def test_pair(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    ds2 = sequencer.dsdb[self.opands[1]]
    ds = ds1.pair(ds2)
    if len(ds) != len(ds1) * len(ds2):
      res = sut.UTState.FAIL
      ans = sequencer.failstr(f"{len(ds)} {NEq} {len(ds1)}x{len(ds2)}")
    else:
      res = sut.UTState.PASS
      ans = [ f"{RArrow} paired",
              f"{ds.name}: {ds.data}" ]
    return (res, ans)

  def test_print(self, sequencer):
    ds = sequencer.dsdb[self.opands[0]]
    print(f"name={ds.name}, data={ds.data}")
    return sut.UTState.PASS, f"{RArrow} printed"

class utDsDbClass(sut.UT):
  """ Test UTDsDB class. """
  def __init__(self, dskey):
    super().__init__('UTDsDb', dskey)

  def begin(self, sequencer, datum):
    self.opcode = datum[0]
    self.opands = datum[1]

    i = self.opcode.find('.error')
    if i < 0:
      expect = sut.UTState.PASS
    else:
      self.opcode = self.opcode[:i]
      expect = sut.UTState.FAIL
    return f"{self.opcode}{self.opands}", expect

  def test(self, sequencer, datum):
    if self.opcode == 'setitem':
      return self.test_setitem(sequencer)
    elif self.opcode == 'dup':
      return self.test_dup(sequencer)
    elif self.opcode == 'del':
      return self.test_del(sequencer)
    else:
      return (sut.UTState.FAIL,
              sequencer.failstr(f"{self.opcode!r} unknown operator"))

  def test_setitem(self, sequencer):
    name = self.opands[0]
    data = self.opands[1]
    try:
      sequencer.dsdb[name] = (name, data)
      ds = sequencer.dsdb[name]
      res = sut.UTState.PASS
      ans = f"{RArrow} added ds {ds.name!r}"
    except (KeyError):
      res = sut.UTState.FAILEd
      ans = sequencer.failstr(f"{RArrow} failed to add new ds")
    return (res, ans)

  def test_dup(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    name = self.opands[1]
    sequencer.dsdb[name] = ds1.copy()
    ds = sequencer.dsdb[name]
    ds[0] = 1234567890
    if len(ds) != len(ds1):
      res = sut.UTState.FAIL
      ans = sequencer.failstr(f"{len(ds)} {NEq} {len(ds1)}")
    elif ds[0] == ds1[0]:
      res = sut.UTState.FAIL
      ans = [ sequencer.failstr(f"bad dup - data to same reference"),
              f"{ds.data}",
              f"{ds1.data}"]
    else:
      res = sut.UTState.PASS
      ans = [ f"{RArrow} duped",
              f"{ds.name}: [{ds[0]}, ..., {ds[-1]}]"]
    return (res, ans)

  def test_del(self, sequencer):
    name = self.opands[0]
    try:
      del sequencer.dsdb[name]
    except (KeyError):
      return (sut.UTState.FAIL, sequencer.failstr(f"{name!r} ds not in db"))
    if name in sequencer.dsdb:
      return (sut.UTState.FAIL,
              sequencer.failstr(f"{name!r} ds did not delete from db"))
    else:
      return (sut.UTState.PASS, f"ds deleted")

class utDotProduct(sut.UT):
  """ Test operations on two datasets class. """
  uDot = '\u22c5'   # dot product operator symbol

  def __init__(self, dskey, dskey2):
    super().__init__('dotproduct', dskey, dskey2)
    self.rhs = sut.UTDsAux(self.args[0])

  def reset(self):
    super().reset()
    self.rhs.reset()

  def prep(self, sequencer):
    super().prep(sequencer)
    self.rhs.prep(sequencer)

  def begin(self, sequencer, datum):
    return  (f"{datum} {utDotProduct.uDot} {self.rhs.datum()}",
            self.expect(datum))
  
  def test(self, sequencer, datum):
    try:
      f = self.dot(datum, self.rhs.datum())
      res = sut.UTState.PASS
      ans = f"= {f}"
    except (IndexError) as e:
      res = sut.UTState.FAIL
      ans = [ sequencer.failstr(f"{RArrow}"),
              f"vectors of unequal sizes "\
              f"{len(datum)} {NEq} {len(self.rhs.datum())}" ]
    except (TypeError, ValueError) as e:
      res = sut.UTState.FAIL
      ans = [sequencer.failstr(f"{RArrow}"), e]

    return (res, ans)

  def end(self, sequencer):
    self.rhs += 1

  def expect(self, datum):
    if len(datum) == len(self.rhs.datum()):
      return sut.UTState.PASS
    else:
      return sut.UTState.FAIL

  def dot(self, v1, v2):
    f = 0
    n = len(v1)
    for i in range(n):
      f += v1[i] * v2[i]
    return f

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------

# vector 1 dataset
dsvec1 = sut.UTDataset('vec1',
                       data = [[1,2,3], [0.9, -3.2 , 3.14], [1, 0, 0],
                               [0, 0, 0], [2.18, 1.618, 0], [-108, 7, -9.2],])

# vector 2 dataset
dsvec2 = sut.UTDataset('vec2', data = [[1,1,1], [-5, 45.6], [2, 4, 8],])

# random integers dataset
dsrandi = sut.UTDataset('randint',
                        data = [random.randint(1,100) for i in range(10)])

# random floats dataset
dsrandf = sut.UTDataset('randfloat',
                        data = [10.0 * random.random() for i in range(10)])

# dataset to unit test UTDataset. Format: [opcode, (opands)]
dsds = sut.UTDataset('UTDataset',
  data = [['create',  ('random', 'numbers')],
          #['print', ('vec2', )],
          ['copy', ('vec1',)],
          ['add', ('randint', 'randfloat')],
          ['iadd', ('randfloat', 'vec2')],
          ['append', ('vec2', [3, 4, 5])],
          ['pair', ('randint', 'randfloat')],
  ]
)

# Dataset to unit test UTDsDB. Format: [opcode, (opands)]
dsdb = sut.UTDataset('UTDsDb',
  data = [['setitem', ('nums', [random.randint(50, 59) for i in range(5)],)],
          ['dup', ('randint', 'randint2')],
          ['del', ('nums', )],
          ['del.error', ('numbnuts', )],
  ]
)

# Dataset to unit test UTSuite. Format: [opcode, (opands)]
dssuite = sut.UTDataset('UTSuite',
  data = [
  ]
)

# the database of datasets
db = sut.UTDsDb('utdb',
                ds=[dsvec1, dsvec2, dsrandi, dsrandf, dsds, dsdb, dssuite])

# test suite
suite = sut.UTSuite('testsuite',
  subsystems=[
    sut.UTSubsys('integrity', 'Test UT classes.',
      unittests=[
        utDsClass('UTDataset'),
        utDsDbClass('UTDsDb'),
        #utSuiteClass('UTSuite'),
      ]
    ),
    sut.UTSubsys('vector', 'Test vector math to test UT further.',
      unittests=[utDotProduct('vec1', 'vec2')]
    )
  ],
)

# unit test sequencer
utseq = sut.UTSequencer('ut', suite, db)

# required entry point function for unittest.py script
def utmain():
  return sut.UTMainTemplate(utseq, "Unit test testing.ut framework module")
