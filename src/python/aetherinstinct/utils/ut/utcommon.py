"""
Unit test the common module.

\LegalBegin
  MIT
\LegalEnd
"""

import random
from enum import Enum

# import unit test framework
import aetherinstinct.testing.ut as ut

# import system under test 
import aetherinstinct.utils.common as sut

RArrow = ut.UTString.RARROW.value

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------

# test of isiterable()
class Counter:
  def __init__(self, low, high):
    self.low = low
    self.high = high
    self.current = self.low
  
  def __str__(self):
    return f"Counter({self.low!r}, {self.high!r})"

  def __iter__(self):
    return self
  
  def __next__(self):
    if self.current > self.high:
      self.current = self.low
      self.high = self.high
      raise StopIteration
    else:
      n = self.current
      self.current += 1
      return n

class Quadrilateral:
  def __init__(self, a, b, c, d):
    self.a = a
    self.b = b
    self.c = c
    self.d = d

  def __str__(self):
    return f"Quadrilateral({self.a!r}, {self.b!r}, {self.c!r}, {self.d!r})"

class Rectangle(Quadrilateral):
  def __init__(self, w, h):
    Quadrilateral.__init__(self, w, h, w, h)

  def __str__(self):
    return f"Rectangle({self.a!r}, {self.b!r})"

  def area(self):
    return self.a * self.b

class Square(Rectangle):
  def __init__(self, s):
    Rectangle.__init__(self, s, s)

  def __str__(self):
    return f"Square({self.a!r})"

class OneTwoThree(Enum):
  one = 1
  two = 2
  three = 3

class OhBeauty(Enum):
  BLUE_SKY = 0
  GRAY_OCEAN = 1
  PURPLE_MOUNTAINS = 2
  AMBER_GRAIN = 5

l = [1, 1, 2, 3, 5, 8, 11]
s = "I'm a string!"
d = {'a': 'aardvark', 'b': 'baboon'} #, 'c': 'coyote'}
b = False
i = -34
f = 3.14
t = ('LSD', 'bift')

# isderived test dataset
dsIsDerived = ut.UTDataset('ds_isderived',
  data = [(d, 'dict', True),  (s, 'str', True),
          (f, 'float', True), (l, 'list', True),
          (f, float, True), (l, list, True),
          (t, 'tuple', True), (b, 'bool', True),
          (i, 'int', True),
          (Quadrilateral, 'Quadrilateral', True),
          (Quadrilateral(4, 5, 2, 3), 'Quadrilateral', True),
          (Rectangle, 'Rectangle', True),
          (Rectangle(9, 11), 'Rectangle', True),
          (Rectangle(30, 20), 'Square', False),
          (Square, 'Square', True),
          (Square(8), 'Square', True),
          (Square(88), 'Rectangle', True),
          (Square(888), 'Quadrilateral', True),
          (Square, Quadrilateral, True),
          (Square(888), 'list', False),
          ]

)

# isiterable test dataset
dsIsIterable = ut.UTDataset('ds_isiterable',
  data = [(l, True), (s, True), (d, True), (b, False),
          (i, False), (f, False), (t, True),
          (Counter(-3, 12), True),
          (Square(8), False),
         ]
)

# enumfactory dataset
dsEnumFactory = ut.UTDataset('ds_enumfactory', 
  data = [(OneTwoThree, 1, True), (OneTwoThree, 4, False),
          (OneTwoThree, 'three', True), (OneTwoThree, 'THREE', False),
          (OhBeauty, 2, True),
          (OhBeauty, 'gray ocean', True),
          (OhBeauty, OneTwoThree.three, False),
          (OhBeauty, OneTwoThree.one, True),
          (OhBeauty, 'GRAY_OCEAN', True),
          ]
)

# random whole numbers dataset
dsN = ut.UTDataset('ds_n',
    data = [0, 1, 2] + [random.randint(3,100000) for i in range(30)])

# the database of datasets
db = ut.UTDsDb('db', ds=[dsIsDerived, dsIsIterable, dsEnumFactory, dsN])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

class utIsDerived(ut.UT):
  """ Unit test isderived(). """
  def __init__(self, dskey):
    super().__init__("isderived()", dskey)

  def begin(self, sequencer, datum):
    self.obj  = datum[0]
    self.isa  = datum[1]
    self.tf   = datum[2]
    return (f"isderived({self.obj}, {self.isa!r})", ut.UTState.PASS)

  def test(self, sequencer, datum):
    tf = sut.isderived(self.obj, self.isa)
    if tf == self.tf:
      res = ut.UTState.PASS
      ans = f"{RArrow} {tf}"
    else:
      res = ut.UTState.FAIL
      ans = [f"{RArrow} {tf}",
              f"determined to be {tf} but should be {self.tf}"]
    return (res, ans)

class utIsIterable(ut.UT):
  """ Unit test isiterable(). """
  def __init__(self, dskey):
    super().__init__("isiterable()", dskey)

  def begin(self, sequencer, datum):
    self.obj  = datum[0]
    self.tf   = datum[1]
    return (f"isiterable({self.obj})", ut.UTState.PASS)

  def test(self, sequencer, datum):
    tf = sut.isiterable(self.obj)
    if tf == self.tf:
      res = ut.UTState.PASS
      ans = f"{RArrow} {tf}"
    else:
      res = ut.UTState.FAIL
      ans = [
          f"{RArrow} {tf}",
          sequencer.failstr(f"determined to be {tf} but should be {self.tf}")]
    return (res, ans)

class utEnumFactory(ut.UT):
  """ Unit test enumfactory(). """
  def __init__(self, dskey):
    super().__init__("enumfactory()", dskey)

  def begin(self, sequencer, datum):
    self.klass  = datum[0]
    self.value  = datum[1]
    self.tf     = datum[2]
    if self.tf:
      expect = ut.UTState.PASS
    else:
      expect = ut.UTState.FAIL
    return (f"enumfactory({self.klass.__name__}, {self.value!r})", expect)

  def test(self, sequencer, datum):
    try:
      enu = sut.enumfactory(self.klass, self.value)
      res = ut.UTState.PASS
      ans = f"{RArrow} {enu}"
    except (TypeError, ValueError, NameError) as e:
      res = ut.UTState.FAIL
      ans = [f"{RArrow}", sequencer.failstr(f"{e}")]
    return (res, ans)

class utPrimeFactorization(ut.UT):
  """ Unit test prime_factorization(). """
  def __init__(self, dskey):
    super().__init__("prime_factorization()", dskey)

  def begin(self, sequencer, datum):
    return (f"prime_factorization({datum})", ut.UTState.PASS)

  def test(self, sequencer, datum):
    primes = sut.prime_factorization(datum)
    m = self.validate(datum, primes)
    if m == datum:
      res = ut.UTState.PASS
      ans = [ f"{RArrow} factored into {len(primes)} primes", f"{primes}" ]
    else:
      res = ut.UTState.FAIL
      ans = [ f"{RArrow}",
              sequencer.failstr(f"{datum} {uNeq} {m}"),
              f"{primes}"
            ]
    return res, ans

  def validate(self, n, primes):
    if len(primes) == 0:
      return n
    m = 1
    for p in primes:
      m *= p
    return m

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------

# test suite
suite = ut.UTSuite('testsuite',
  subsystems=[
    ut.UTSubsys('isa', "Test 'is a' functions.",
      unittests=[
        utIsDerived(dsIsDerived.name),
        utIsIterable(dsIsIterable.name),
      ]
    ),
    ut.UTSubsys('enum', "Test enumeration functions.",
      unittests=[
        utEnumFactory(dsEnumFactory.name),
      ]
    ),
    ut.UTSubsys('numbers', "Test numbers functions.",
      unittests=[
        utPrimeFactorization(dsN.name),
      ]
    ),
  ],
)

# unit test sequencer (required name for unittest.py script)
utseq = ut.UTSequencer('common', suite, db)

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  def utmain():
    stats = ut.UTMainTemplate(utseq, "Unit test utils.common module.")
    return 0

  utmain()
