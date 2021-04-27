from functools import wraps
from collections import namedtuple


# task 2.1
def greetings(func):
    def inner(*args):
        return "Hello " + func(*args).title()

    return inner


# task 2.2
def is_palindrome(func):
    @wraps(func)
    def inner(*args, **kwargs):
        sentence = func(*args, **kwargs)
        filtered_sentence = "".join(filter(str.isalnum, str.lower(sentence)))
        if filtered_sentence[::-1] == filtered_sentence:
            return sentence + " - is palindrome"
        else:
            return sentence + " - is not palindrome"

    return inner


# task 2.3
def format_output(*args):
    def decorator(func):
        @wraps(func)
        def wrapper(*wrapper_args, **kwargs):
            Argument = namedtuple("Argument", ["original", "split"])
            arguments = [Argument(arg, str.split(arg, sep='__'))
                         for arg in args]
            func_dict = func(*wrapper_args, **kwargs)
            result_dict = {}
            validated_arguments = [arg in func_dict for seq in arguments for arg in seq.split]
            if not all(validated_arguments):
                raise ValueError
            for arg in arguments:
                result_dict[arg.original] = " ".join([func_dict[x] for x in arg.split])
            return result_dict

        return wrapper

    return decorator


# task 2.4
def add_class_method(cls):
    def decorator(func):
        @classmethod
        @wraps(func)
        def wrapper(self):
            return func()

        setattr(cls, func.__name__, wrapper)
        return func

    return decorator


def add_instance_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self):
            return func()

        setattr(cls, func.__name__, wrapper)
        return func

    return decorator

