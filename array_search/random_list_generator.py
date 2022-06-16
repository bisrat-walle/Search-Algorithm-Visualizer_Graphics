import random
from array_search.node import *


def random_list_generator(sort: bool = False, n: int = 10):
    """ Generates a random list of length <n> """

    return [Node(int(random.random() * 9)) for _ in range(n)]
