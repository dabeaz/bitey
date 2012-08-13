import sys
sys.path.insert(0,"..")
import unittest
import bitey
import ctest
import ctypes

class TestTypes(unittest.TestCase):
    def test_char(self):
        r = ctest.add_char(4,5)
        self.assertEqual(r,9)

    def test_short(self):
        r = ctest.add_short(4,5)
        self.assertEqual(r,9)

    def test_int(self):
        r = ctest.add_int(4,5)
        self.assertEqual(r,9)

    def test_long(self):
        r = ctest.add_long(4,5)
        self.assertEqual(r,9)

    def test_longlong(self):
        r = ctest.add_longlong(4,5)
        self.assertEqual(r,9)

    def test_float(self):
        r = ctest.add_float(2.1, 4.2)
        self.assertAlmostEqual(r, 6.3, 5)

    def test_double(self):
        r = ctest.add_double(2.1, 4.2)
        self.assertEqual(r, 2.1 + 4.2)

class TestPointers(unittest.TestCase):
    def test_mutate_short(self):
        a = ctypes.c_short()
        a.value = 2
        r = ctest.mutate_short(a)
        self.assertEqual(a.value, 4)

    def test_mutate_int(self):
        a = ctypes.c_int()
        a.value = 2
        r = ctest.mutate_int(a)
        self.assertEqual(a.value, 4)

    def test_mutate_long(self):
        a = ctypes.c_long()
        a.value = 2
        r = ctest.mutate_long(a)
        self.assertEqual(a.value, 4)

    def test_mutate_longlong(self):
        a = ctypes.c_longlong()
        a.value = 2
        r = ctest.mutate_longlong(a)
        self.assertEqual(a.value, 4)

    def test_mutate_float(self):
        a = ctypes.c_float()
        a.value = 2
        r = ctest.mutate_float(a)
        self.assertEqual(a.value, 4)

    def test_mutate_double(self):
        a = ctypes.c_double()
        a.value = 2
        r = ctest.mutate_double(a)
        self.assertEqual(a.value, 4)


class TestArrays(unittest.TestCase):
    def test_int(self):
        a = (ctypes.c_int * 4)(1,2,3,4)
        r = ctest.arr_sum_int(a)
        self.assertEqual(r,10)

    def test_double(self):
        a = (ctypes.c_double *4)(1,2,3,4)
        r = ctest.arr_sum_double(a)
        self.assertEqual(r, 10.0)

class TestStructure(unittest.TestCase):
    def test_Point(self):
        a = ctest.Point(3,4)
        b = ctest.Point(6,8)
        d = ctest.distance(a,b)
        self.assertEqual(d,5.0)
        
if __name__ == '__main__':
    unittest.main()


