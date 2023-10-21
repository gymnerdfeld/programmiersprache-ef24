import math


def cos(x):
    return math.sin(x + math.pi / 2)


def fact(n):
    if n < 2:
        return 1
    else:
        return n * fact(n - 1)


def abs(x):
    if x < 0:
        return -x
    else:
        return x


def fib(n):
    if n < 2:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def sqrt(x):
    def sqrt_iter(guess):
        if is_good_enough(guess):
            return guess
        else:
            return sqrt_iter(improve(guess))

    def is_good_enough(guess):
        return abs(guess * guess - x) < 0.001

    def improve(guess):
        return average(guess, x / guess)

    def average(x, y):
        return (x + y) / 2

    return sqrt_iter(1)


def cached(func):
    cache = {}

    def new_func(x):
        if x in cache:
            return cache[x]
        else:
            res = func(x)
            cache[x] = res
            return res

    return new_func


fib = cached(fib)


def make_adder(x):
    def adder(y):
        return x + y

    return adder


plus5 = make_adder(5)
