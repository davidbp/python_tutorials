from typing import Callable
import functools

ComposableFunction = Callable[[float], float]

def compose(*functions: ComposableFunction) -> ComposableFunction:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)

def call(x: int, fn: Callable):
    return fn(x)

def addThree(x):
    return x+3

def addOne(x):
    return x+1

def main():    
    x = 12
    print("Result: ", call(x, compose(addThree, addOne)))

if __name__ == "__main__":
    main()
