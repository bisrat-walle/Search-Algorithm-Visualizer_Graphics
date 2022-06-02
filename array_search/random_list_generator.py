import random

def random_list_generator(sort: bool = False, n: int = 10):
    """ Generates a random list of length <n> """

    lst = [int(random.random() * 20) for _ in range(n)]

    return sorted(lst) if sort else lst
