"""Simple calculator with a deliberate bug for CI-failure practice."""


def add(a, b):
    return a + b


def subtract(a, b):
    # INTENTIONAL BUG: should be a - b.
    return a + b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
