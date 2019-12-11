import unittest
from circles import circle_area, circle_perimeter
from math import pi


class TestCircleArea(unittest.TestCase):
    def test_area(self):
        # test areas
        self.assertAlmostEqual(circle_area(1), pi)
        self.assertAlmostEqual(circle_area(2.1), pi*2.1**2)
        self.assertAlmostEqual(circle_area(0), 0)
         
    def test_values(self):
        # Make sure errors are raised when necessary
        self.assertRaises(ValueError, circle_area, -2)

    def test_types(self):
        # Make sure type errors are raised
        self.assertRaises(TypeError, circle_area, 2+5j)
        self.assertRaises(TypeError, circle_area, True)
        self.assertRaises(TypeError, circle_area, "23")


class TestCirclePerimeter(unittest.TestCase):
    def test_area(self):
        # test areas
        self.assertAlmostEqual(circle_perimeter(1), 2* pi)
        self.assertAlmostEqual(circle_perimeter(2.1), pi*2.1*2)
        self.assertAlmostEqual(circle_perimeter(0), 0)
         
    def test_values(self):
        # Make sure errors are raised when necessary
        self.assertRaises(ValueError, circle_perimeter, -2)

    def test_types(self):
        # Make sure type errors are raised
        self.assertRaises(TypeError, circle_perimeter, 2+5j)
        self.assertRaises(TypeError, circle_perimeter, True)
        self.assertRaises(TypeError, circle_perimeter, "23")
