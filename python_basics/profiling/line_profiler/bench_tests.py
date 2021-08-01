
import time
import random
import numpy as np

N_SAMPLES = 10_000

class A_attribute:
    def __init__(self):
        self.height = 10

class B_property:
    def __init__(self):
        pass

    @property    
    def height(self):
        return 10

class C_method:
    def __init__(self):
        pass

    def height(self):
        return 10

@profile
def atribute_from_class():
    s = np.sum([A_attribute().height for i in range(N_SAMPLES)])
    return s

@profile
def property_from_class():
    s = np.sum([B_property().height for i in range(N_SAMPLES)])
    return s

@profile
def method_from_class():
    s = np.sum([C_method().height() for i in range(N_SAMPLES)])
    return s

@profile
def main_func():
    result = atribute_from_class()
    print(result)

    result = property_from_class()
    print(result)

    result = method_from_class()
    print(result)

main_func()
